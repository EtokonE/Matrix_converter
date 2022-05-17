import pandas as pd


class MatrixTransformer:
    def __init__(self, matrix_excel):
        self.excel_file = matrix_excel

    def _read_excel(self):
        """Читает файл"""
        return pd.read_excel(self.excel_file, index_col=0)

    def _write_excel(self, dict):
        """Сохраняет преобразованный словарь с корректными названиями в excel файл"""
        new_dataframe = pd.DataFrame({k: [v] for k, v in dict.items()})
        new_dataframe.to_excel('./transformed_matrix.xlsx')

    def _matrix2transformed_dict(self, matrix):
        """Преобразует датафрейм в словарь. Ключи в словаре соответствуют названиям строки и столбца,
        на пересечении которых находится значение"""
        transformed_dict = {}
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                transformed_dict[matrix.index[row] + '&' + matrix.columns[col]] = matrix.iloc[row][col]
        return transformed_dict

    def transform_matrix(self):
        matrix = self._read_excel()
        transformed_dict = self._matrix2transformed_dict(matrix)
        self._write_excel(transformed_dict)


transformer = MatrixTransformer('./matrix.xlsx')
transformer.transform_matrix()