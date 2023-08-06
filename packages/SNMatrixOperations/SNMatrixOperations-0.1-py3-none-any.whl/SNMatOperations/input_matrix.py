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