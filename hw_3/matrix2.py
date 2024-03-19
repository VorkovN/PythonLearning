import numpy as np

class MatrixMixin():
    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            return self.matrix[row][col]
        else:
            raise KeyError("Key must be a tuple of two integers")

    def __setitem__(self, key, value):
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            self.matrix[row][col] = value
        else:
            raise KeyError("Key must be a tuple of two integers")

    @property
    def shape(self):
        return len(self.matrix), len(self.matrix[0])

    @shape.setter
    def shape(self, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Shape must be a tuple of two integers")
        self.matrix = [[0] * value[1] for _ in range(value[0])]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for row in self.matrix:
                file.write(' '.join(map(str, row)) + '\n')

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

class Matrix(MatrixMixin):
    def __init__(self, matrix):
        self.matrix = matrix  # Здесь matrix уже лист листов

    def __add__(self, other):
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
            raise ValueError("Матрицы разных размеров не могут быть сложены")
        return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])


    def __sub__(self, other):
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
            raise ValueError("Матрицы разных размеров не могут быть сложены")
        return Matrix([[self.matrix[i][j] - other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])

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
    sub_result = m1 - m2
    mul_result = m1 * m2
    matmul_result = m1 @ m2

    add_result.save_to_file("artifacts/matrix2+.txt")
    sub_result.save_to_file("artifacts/matrix2-.txt")
    mul_result.save_to_file("artifacts/matrix2*.txt")
    matmul_result.save_to_file("artifacts/matrix2@.txt")

    add_result[3, 2] = 666

    print(add_result)
    print(add_result.shape)