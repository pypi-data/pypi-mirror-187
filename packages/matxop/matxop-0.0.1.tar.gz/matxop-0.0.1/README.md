#MatrixOperations

\*NOTE:This package will work only if they are compatible.

zeros_matrix(rows, cols):
Creates a matrix filled with zeros.
:param rows: the number of rows the matrix should have
:param cols: the number of columns the matrix should have

        :return: list of lists that form the matrix

def identity_matrix(n):
Creates and returns an identity matrix.
:param n: the square size of the matrix

        :return: a square identity matrix

def copy_matrix(M):
Creates and returns a copy of a matrix.
:param M: The matrix to be copied

        :return: A copy of the given matrix

def print_matrix(M, decimals=3):
Print a matrix one row at a time
:param M: The matrix to be printed

def transpose(M):
Returns a transpose of a matrix.
:param M: The matrix to be transposed

        :return: The transpose of the given matrix

def matrix_addition(A, B):
Adds two matrices and returns the sum
:param A: The first matrix
:param B: The second matrix

        :return: Matrix sum

def matrix_subtraction(A, B):
Subtracts matrix B from matrix A and returns difference
:param A: The first matrix
:param B: The second matrix

        :return: Matrix difference

def matrix_multiply(A, B):
Returns the product of the matrix A \* B
:param A: The first matrix - ORDER MATTERS!
:param B: The second matrix

        :return: The product of the two matrices

def multiply_matrices(list):
"""
Find the product of a list of matrices from first to last
:param list: The list of matrices IN ORDER

        :return: The product of the matrices

def check_matrix_equality(A, B, tol=None):
Checks the equality of two matrices.
:param A: The first matrix
:param B: The second matrix
:param tol: The decimal place tolerance of the check

        :return: The boolean result of the equality check

def unitize_vector(vector):
Find the unit vector for a vector
:param vector: The vector to find a unit vector for

        :return: A unit-vector of vector
