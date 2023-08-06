#MATRIX ADDITION
def matrix_addition(A,B):
    mat_addition=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B[0])):
            c.append(A[i][j]+B[i][j])
        mat_addition.append(c)
    print('Matrix Addition=')
    print(mat_addition)
A=[[1,2],[3,5]]
B=[[2,1],[3,4]]
V=matrix_addition(A,B)

#MATRIX SUBRACTION
def matrix_subraction(A,B):
    mat_subraction=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B)):
            c.append(A[i][j]-B[i][j])
        mat_subraction.append(c)
    print('Matrix Subraction=')
    for i in range(len(mat_subraction)):
        for j in range(len(mat_subraction[0])):
            print(mat_subraction[i][j],end=' ')
        print()

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
    for r in range (len(mul_result)):
        for j in range(len(mul_result[0])):
            print(mul_result[r][j],end=' ')
        print()
    return mul_result

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
    for i in range(rows):
        for j in range(columns):
            print(A[i][j],end=' ')
        print()
    return A