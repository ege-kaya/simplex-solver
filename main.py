class Matrix:
    def __init__(self, m, n, rows):
        self.m = m
        self.n = n
        self.rows = rows
        self.bv =[]
        for i in range(n-m, n-1):
            self.bv.append(i)
    m = 0 # number of rows in the matrix
    n = 0 # number of columns in the matrix
    rows = []
    bv = []

# col: the index of the column to do ratio check
def ratio_check(col, matrix):
    m = matrix.m
    min = float('inf')
    min_index = -1
    for i in range(1, m):
        coef = matrix.rows[i][col]
        if coef > 0:
            ratio = matrix.rows[i][-1] / coef
            if ratio < min:
                min = ratio
                min_index = i
    return min_index

def not_solved(matrix):
    n = matrix.n
    objective = matrix.rows[0]
    for i in range(n):
        if objective[i] < 0:
            return True
    return False

def pivot(row, col, matrix):
    m = matrix.m
    bv = matrix.bv
    pivot = matrix.rows[row][col]
    c = 1 / pivot
    scalar_multiplication(matrix, row, c)
    for j in range(0, m):
        if j != row:
            coefficient = matrix.rows[j][col]
            row_addition(matrix, j, row, -coefficient)
    bv[row-1] = col

def simplex_iteration(matrix):
    n = matrix.n
    objective = matrix.rows[0]
    min = float('inf')
    min_col = -1
    for i in range(n):
        if objective[i] < min:
            min = objective[i]
            min_col = i
    pivot_row = ratio_check(min_col, matrix)
    pivot_col = min_col
    pivot(pivot_row, pivot_col, matrix)

# reads the input from a file
def get_input(filename):
    with open(filename) as file:
        l = file.read().splitlines()
    l[0] = l[0].split('\t')
    m = int(l[0][0])
    n = int(l[0][1])
    for i in range(1, m+2):
        l[i] = l[i].split('\t')
        l[i] = [float(i) for i in l[i]]
        # adding slacks
        if i == 1:
            for j in range(m+1):
                l[i].append(0)
        else:
            for j in range(m):
                if j+2 == i:
                    l[i].insert(-1, 1.0)
                else:
                    l[i].insert(-1, 0.0)

    matrix = Matrix(m+1, n+m+1, l[1:])
    return matrix

# multiplies the row at index r2 by the coefficient and adds it to row at index r1
def row_addition(matrix, r1, r2, coefficient):
    r3 = []
    n = matrix.n
    for i in range(0, n):
        r3.append(round(matrix.rows[r1][i] + matrix.rows[r2][i] * coefficient, 6))
    matrix.rows[r1] = r3


# multiplies the row at given index of a matrix by a scalar
def scalar_multiplication(matrix, r, c):
    cr = []
    n = matrix.n
    for i in range(0, n):
        cr.append(matrix.rows[r][i] * c)
    matrix.rows[r] = cr


filenames = ['Data1.txt', 'Data2.txt', 'Data3.txt']
for i in range(3):
    matrix = get_input(filenames[i])
    while not_solved(matrix):
        simplex_iteration(matrix)
    positive_result = round(matrix.rows[0][-1], 4)
    unbounded = (positive_result > 10e6)
    print("Solving for " + filenames[i] +":")
    if not unbounded:
        print("Optimal variable vector:")
        result = []
        for i in range(matrix.n-matrix.m):
            if i in matrix.bv:
                result.append(round(matrix.rows[matrix.bv.index(i)+1][-1], 4))
            else:
                result.append(0)
        print(result)
        print("Optimal result:")
        print(-round(matrix.rows[0][-1], 4))
        print()
    else:
        print("The problem is unbounded")
        print()

