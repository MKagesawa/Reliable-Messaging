import socket
import time
import Matrix

M_UNDEF     = '0'
M_LOGIN     = '1'
M_CONNECT   = '2'
M_EXCHANGE  = '3'
M_LOGOUT    = '4'
M_DISCONNECT= '5'
M_SEARCH    = '6'
M_LIST      = '7'
M_POEM      = '8'
M_TIME      = '9'

CHAT_IP = ''    #for Mac
#CHAT_IP = socket.gethostname()  #for PC
CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\n++++ Choose one of the following commands\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n\n"

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3

SIZE_SPEC = 5

CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')
    
def mysend(s, msg):
    print('Sending original message:', msg)
    msg_matrix = Matrix.alnum2matrix(msg)
    #display original message
    print('Sending original matrix:', str(msg_matrix))
    print()
    corrupted = Matrix.randomize_one_digit(msg_matrix)
    msg = Matrix.matrix_list2matrix_string(corrupted)
    #msg is now a string for sure!
    
    #append size to message and send it
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg) :
        sent = s.send(msg[total_sent:])
        if sent==0:
            print('server disconnected')
            break
        total_sent += sent

def myrecv(s):
    
    #receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    #now receive message
    msg = ''
    while len(msg) < size:
        text = s.recv(size-len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
        
    receive_recover = Matrix.matrix_string2matrix_list(msg)
    #display the wrong message to audience
    print('Receiving corrupted matrix:', str(receive_recover))
    print('Receiving corrupted message:', Matrix.matrix2alnum(receive_recover))
    print()
    corrected = Matrix.error_correction(receive_recover)
    msg = Matrix.matrix2alnum(corrected)
    #msg is now a string for sure!
        
    print ('Corrected message:', msg)
    return (msg)
    
def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen