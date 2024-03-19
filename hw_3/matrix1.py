import numpy as np


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix  # Здесь matrix уже лист листов

    def __add__(self, other):
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
            raise ValueError("Матрицы разных размеров не могут быть сложены")
        return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])

    def __mul__(self, other):
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
            raise ValueError("Матрицы разных размеров не могут быть умножены покомпонентно")
        return Matrix([[self.matrix[i][j] * other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])

    def __matmul__(self, other):
        if len(self.matrix[0]) != len(other.matrix):
            raise ValueError("Матрицы неподходящих размеров для матричного умножения")
        result = [[sum(a*b for a,b in zip(self_row,other_col)) for other_col in zip(*other.matrix)] for self_row in self.matrix]
        return Matrix(result)

if __name__ == "__main__":
    np.random.seed(0)

    m1 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    m2 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    add_result = m1 + m2
    mul_result = m1 * m2
    matmul_result = m1 @ m2
    print(add_result)

    np.savetxt("artifacts/matrix+.txt", add_result.matrix, fmt="%d")
    np.savetxt("artifacts/matrix*.txt", mul_result.matrix, fmt="%d")
    np.savetxt("artifacts/matrix@.txt", matmul_result.matrix, fmt="%d")

