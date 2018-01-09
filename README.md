# Reliable-Messaging
Implemented two-dimensional parity check algorithm on chat server & client skeleton.

### Steps
1. alnum2matrix(msg): Every message sent from a client is broken down to characters and then converted to a 4 column matrix confirming to the ASCII code.

2. matrix_list2matrix_string(matrix): Turn the matrix to a string type for sending

3. randomize_one_digit(matrix): Intentionally modify one of the number in the matrix

4. matrix_string2matrix_list(mat_string): Turn the string type back to matrix for receiving and error correction.

5. matrix2alnum(matrix): Convert the matrix back to string message


### Next Step
Use binary number instead of ASCII code to reflect better how the algorithm works in reality.
