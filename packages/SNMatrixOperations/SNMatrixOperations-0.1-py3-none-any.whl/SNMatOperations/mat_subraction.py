#MATRIX SUBRACTION
def matrix_subraction(A,B):
    mat_subraction=[]
    for i in range(len(A)):
        c=[]
        for j in range(len(B)):
            if A[i][j]==B[i][j]:
                c.append(A[i][j]-B[i][j])
        mat_subraction.append(c)
    print('Matrix Subraction=')
    for i in range(len(mat_subraction)):
        for j in range(len(mat_subraction[0])):
            print(mat_subraction[i][j],end=' ')
        print()
    return mat_subraction