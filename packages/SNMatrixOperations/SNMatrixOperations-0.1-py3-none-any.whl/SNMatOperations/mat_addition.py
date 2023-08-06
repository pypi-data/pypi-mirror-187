#MATRIX ADDITION
def matrix_addition(A,B):
    mat_addition=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B)):
            if A[i][j]==B[i][j]:
                c.append(A[i][j]+B[i][j])
        mat_addition.append(c)
    print('Matrix Addition=')
    for z in range(len(mat_addition)):
        for w in range(len(mat_addition[0])):
            print(mat_addition[z][w],end=' ')
        print()
    return mat_addition