row=int(input("Enter number of rows of matrix 1 : "))
col=int(input("Enter number of column of matrix1 / number of row of matrix2  : "))
col1=int(input("Enter number of column of matrix 2 : "))


#input for matrix 1

matrix1=[]
for i in range(row):
    c=[]
    for j in range(col):
        input1=int(input("Enter elements of matrix 1 : "))
        c.append(input1)
    matrix1.append(c)
    print()

#input for matrix 2

matrix2=[]
for i in range(col):
    d=[]
    for j in range(col1):
        input2=int(input("Enter elements of matrix 2 : "))
        d.append(input2)
    matrix2.append(d)
    print()


    
#printing matrixes
print("Matrix 1 is : ")
for i in range(row):
    for j in range(col):
        print(matrix1[i][j],end=" ")
    print()
    
print("Matrix 2 is : ")
for i in range(col):
    for j in range(col1):
        print(matrix2[i][j],end=" ")
    print()
    
    

     
     
#multiplicating matrixes
result=[[0 for i in range(col1)] for j in range(row)]
for i in range(row):
    for j in range(col1):
        for k in range(col):
            result[i][j]=result[i][j]+matrix1[i][k]*matrix2[k][j]
            
  

#printing result
print("Multiplied matrix is : ")
for i in range(row):
    for j in range(col1):
        print(result[i][j],end=" ")
    print()
