import random
import numpy as np

def alnum2matrix(msg):     #返回结果为matrix list
    matrix = []
    message = []
    for c in msg:
        message.append(ord(c))
 
    if len(msg)%4 == 0:            #handle the len_row exactly
        len_row = (len(message)//4)
    else:
        len_row = (len(message)//4 + 1)

    [matrix.append([]) for i in range(len_row)]

    
    for i in range(len_row):
        for a in range(4):
            try:
                matrix[i].append(message.pop(0))
            except IndexError:
                matrix[i].append(0)

    
    matrix_checksum = matrix[:]
    for i in range(len_row):
        row_total = 0
        for ele in matrix_checksum[i]:
            row_total += ele
        matrix_checksum[i].append(row_total)
        
    matrix_checksum.append([])   #add column_sum
    for i in range(5):
        colum_total = 0
        for a in range(len_row):
            colum_total += matrix_checksum[a][i]
        matrix_checksum[-1].append(colum_total)

    return matrix_checksum

def matrix_list2matrix_string(matrix):
    return str(matrix)

def matrix_string2matrix_list(mat_string):       
    mat_string = mat_string.lstrip('[[')
    mat_string = mat_string.rstrip(']]')
    matrix_list = []
    for i in mat_string.split('], ['):       #逗号后面空一格很重要？
        sublist = []
        for j in i.split(','):
            sublist.append(int(j))
        matrix_list.append(sublist)
    
    #print(matrix_list)    #debug
    return matrix_list

def randomize_one_digit(matrix):     #返回结果为matrix list!

    matrix[random.randint(0, len(matrix)-1)][random.randint(0, 4)] = random.randint(32, 126)
    return matrix


def error_correction(matrix):       #返回结果为matrix list!

    len_row = len(matrix)
    len_column = 5
    error_row = None
    error_column = None
    error_row_sum = None
    error_col_sum = None

    #Find error row
    for row in range(len_row-1):
        if np.sum(matrix[row][:4]) != matrix[row][4]:
            error_row = row
            error_row_sum = np.sum(matrix[row][:4])


    #Find error column
    for col in range(len_column-1):
        col_sum = 0
        for i in range(len_row-1):
            col_sum += matrix[i][col]
        if col_sum != matrix[-1][col]:
            error_column = col
            error_col_sum = col_sum

    #When no error or the only error is the sum of all checksums(right-bottom corner)
    if error_row == None and error_column == None:
        matrix[len_row-1][len_column-1] = (int(matrix[len_row-1][0])+int(matrix[len_row-1][1])+int(matrix[len_row-1][2])+int(matrix[len_row-1][3]))

    #When the error is checksum row
    elif error_row == None and error_column != None:
        m = 0
        for row in range(len_row-1):
            m += matrix[row][error_column]
        matrix[-1][error_column] = m

    #When the error is checksum column
    elif error_column == None and error_row != None:
        n = 0
        for col in range(len_column-1):
            n += matrix[error_row][col]
        matrix[error_row][-1] = n

    #When the error is one of the message ASCII-code
    else:
        matrix[error_row][error_column] = matrix[error_row][error_column] - (error_row_sum - matrix[error_row][-1])
    return matrix


def matrix2alnum(matrix):                #接收到的matrix为5-column的！     #返回结果为正常的string!
    matrix = np.array(matrix)
    msg = ""
    len_row = int(matrix.size/5)
    len_column = 5
    for row in range(len_row - 1):
        for column in range(len_column - 1):
            if int(matrix[row][column]) != 0:
                msg += chr(matrix[row][column])
    msg = str(msg)
    return msg
