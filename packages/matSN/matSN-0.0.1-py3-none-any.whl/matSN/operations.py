def matrix_addition(A,B):
    mat_addition=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B[0])):
            c.append(A[i][j]+B[i][j])
        mat_addition.append(c)
    print('Matrix Addition=')
    print(mat_addition)

#MATRIX SUBRACTION
def matrix_subraction(A,B):
    mat_subraction=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B)):
            c.append(A[i][j]-B[i][j])
        mat_subraction.append(c)
    print('Matrix Subraction=')
    print(mat_subraction)

#MATRIX MULTIPLICATION
def matrix_multiplication(A,B):
    mul_result=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B[0])):
            result=0
            for k in range(len(B)):
                result+=A[i][k]*B[k][j]
            c.append(result)
        mul_result.append(c)
    print('Matrix Multiplication=')
    print(mul_result)

#INPUT MATRIX
def input_matrix(rows,columns): 
    A=[]
    print('Enter the entries row wise:')
    a=[]
    for i in range(rows):
        a=[]
        for j in range(columns):
            a.append(int(input()))
        A.append(a)
    print('Input Matrix=')
    print(A)