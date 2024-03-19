import numpy as np

class HashMixin:
    def __hash__(self):
        # Преобразование списка списков в NumPy массив для вычисления сингулярного разложения
        matrix_np = np.array(self.matrix)
        # Вычисление сингулярного разложения
        singular_values = np.linalg.svd(matrix_np, compute_uv=False)
        # Использование произведения сингулярных чисел как хэш-значение
        return round(np.prod(singular_values))

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

class Matrix(MatrixMixin, HashMixin):
    _cache_mul = {}

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
    # Так как хэш ищем по сингулярным числам, то для коллизии достаточно просто транспонировать матрицу, тогда сингулярные числа останутся прежними
    np_array = np.random.randint(0, 10, (10, 10))
    np_array_t = np.transpose(np_array)
    A = Matrix(np_array.tolist())
    C = Matrix(np_array_t.tolist())
    B = D = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    AB = A @ B
    CD = C @ D

    print(A.__hash__())
    print(C.__hash__())

    A.save_to_file("artifacts/A.txt")
    B.save_to_file("artifacts/B.txt")
    C.save_to_file("artifacts/C.txt")
    D.save_to_file("artifacts/D.txt")
    AB.save_to_file("artifacts/AB.txt")
    CD.save_to_file("artifacts/CD.txt")

    with open('artifacts/AB_CD_hash.txt', 'w') as file:
        file.write("AB hash: " + str(AB.__hash__()) + "; CD hash: " + str(CD.__hash__()))


