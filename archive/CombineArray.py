# Initialize lists A, B, and C with sample values
A = list(range(1, 21))  # 20 members
B = list(range(21, 51))  # 30 members
C = list(range(51, 91))  # 40 members

# Create an empty 2D list D with 12 rows and 10 columns
D = [[None for _ in range(10)] for _ in range(12)]

# Combine lists A, B, and C into one list

# Track the current index in the combined list
index = 0
max = 120
col_A = len(A)//12 + 1
# Iterate over the columns and rows to fill D
for col in range(col_A):
    if col % 2 == 0:
        for row in range(max//10):
            if index < len(A):
                D[row][col] = A[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11,-1,-1):
            if index < len(A):
                D[row][col] = A[index]
                index += 1
            else:
                break
print("Col A", col_A)
index=0
for col in range(col_A,len(B)//12+1+col_A,1):
    if col % 2 == 0:
        for row in range(max//10):
            if index < len(B):
                D[row][col] = B[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11,-1,-1):
            if index < len(B):
                D[row][col] = B[index]
                index += 1
            else:
                break

index=0
col_B = len(B)//12+1+col_A
for col in range(col_B,len(C)//12+1+col_B,1):
    if col % 2 == 0:
        for row in range(max//10):
            if index < len(C):
                D[row][col] = C[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11,-1,-1):
            if index < len(C):
                D[row][col] = C[index]
                index += 1
            else:
                break


# Print the resulting list D
for row in D:
    print(row)
