import pandas as pd
import scipy.io
from pathlib import Path
import os
from typing import NamedTuple


class Participant(NamedTuple):
    file_name: str
    age_group: str
    gender: str


class MatrixTransformer:
    def __init__(self, mat_folder, out_folder='./outputs'):
        self.mat_folder = Path(mat_folder)
        self.out_folder = out_folder
        self.full_df = pd.DataFrame()
        self.flag = 1

    @staticmethod
    def _read_mat(file_path):
        """Читает файл"""
        return scipy.io.loadmat(file_path)

    @staticmethod
    def _clear_roi_name(roi_name):
        """Убирает информацию о принадлежности к возрастной группе из
        названия ROI
        """
        splitted_roi = roi_name.split('_')
        generalized_roi = '_'.join(splitted_roi[:-1])
        return generalized_roi

    def _mat2df(self, mat_file, mat_shape=(39, 39)):
        """Преобразует .mat файл в датафрейм с необходимой информацией"""
        print(mat_file)
        mat_file = self._read_mat(self.mat_folder / mat_file)
        roi_names = [self._clear_roi_name(i[0]) for i in list(*(mat_file['names']))]
        if mat_file['Z'].shape == mat_shape:
            return pd.DataFrame(mat_file['Z'],
                                columns=roi_names,
                                index=roi_names)
        else:
            print(f'Error in file, the file was converted')
            return pd.DataFrame(mat_file['Z'][:, :mat_shape[0]],
                                columns=roi_names,
                                index=roi_names)

    def _dict2df(self, _dict):
        """Преобразует словарь в датафрейм с корректными названиями
        и добавляет запись в общую таблицу
        """
        new_dataframe = pd.DataFrame({k: [v] for k, v in _dict.items()})
        if self.flag:
            self.full_df = new_dataframe
            self.flag = 0
        else:
            self.full_df = pd.concat([self.full_df, new_dataframe])
        return new_dataframe

    def write_excel(self, df, out_filename='./transformed_matrix.xlsx'):
        """Сохраняет преобразованный датафрейм с корректными названиями в excel файл"""
        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)
            print("The output directory is created!")
        df.to_excel(Path(self.out_folder) / (Path(out_filename).stem + '.xlsx'))

    @staticmethod
    def _extract_participant_info(filename) -> Participant:
        sub_info = Path(filename).stem
        return Participant(file_name=sub_info,
                           age_group=sub_info.split('_')[-2],
                           gender=sub_info.split('_')[-1])


    def _matrix2transformed_dict(self, matrix, filename):
        """Преобразует датафрейм в словарь.
        Ключи в словаре соответствуют названиям строки и столбца,
        на пересечении которых находится значение
        """
        participant_info = self._extract_participant_info(filename)
        transformed_dict = {'sub': participant_info.file_name,
                            'age_group': participant_info.age_group,
                            'gender': participant_info.gender}

        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                transformed_dict[matrix.index[row] +
                                 '_&_' +
                                 matrix.columns[col] +
                                 f'_row:{row}_col:{col}'] = matrix.iloc[row][col]
        return transformed_dict

    def transform_matrix(self, matrix_file, mat_shape):
        """Выполняет все преобразования"""
        matrix = self._mat2df(matrix_file, mat_shape)
        transformed_dict = self._matrix2transformed_dict(matrix, filename=matrix_file)
        transformed_df = self._dict2df(transformed_dict)
        self.write_excel(transformed_df, matrix_file)


def main():
    from config import get_cfg_defaults

    # Get configuration
    cfg = get_cfg_defaults()
    # Create transformer
    transformer = MatrixTransformer(mat_folder=cfg.PATH.MAT_FOLDER,
                                    out_folder=cfg.PATH.OUT_FOLDER)
    # Transform all .mat files
    for _file in os.listdir(cfg.PATH.MAT_FOLDER):
        if _file.endswith('.mat'):
            transformer.transform_matrix(matrix_file=_file, mat_shape=cfg.PARAMETERS.MAT_SIZE)
    # Write final file with combined matrices
    transformer.write_excel(df=transformer.full_df,
                            out_filename=os.path.join(cfg.PATH.OUT_FOLDER,
                                                      cfg.PATH.FINAL_XLSX_FILE))

def test():
    from config import get_cfg_defaults

    # Get configuration
    cfg = get_cfg_defaults()


    # Create transformer
    transformer = MatrixTransformer(mat_folder=cfg.PATH.MAT_FOLDER,
                                    out_folder=cfg.TEST_MODE.OUT)
    mat = transformer._mat2df(cfg.TEST_MODE.MAT, cfg.PARAMETERS.MAT_SIZE)
    print(mat.shape)
    dict = transformer._matrix2transformed_dict(mat, cfg.TEST_MODE.MAT)
    print(dict.shape)

if __name__ == '__main__':
    #test()
    main()
