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