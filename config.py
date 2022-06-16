from yacs.config import CfgNode as CN

_C = CN()

_C.PATH = CN()
# Директория с .mat файлами
_C.PATH.MAT_FOLDER = './RN_Only Matrices_6 June 2022'
# Директория для сохранения результатов
_C.PATH.OUT_FOLDER = './output'
# Название финального файла с объединеными матрицами
_C.PATH.FINAL_XLSX_FILE = 'FULL_DATA.xlsx'

_C.PARAMETERS = CN()
# Размеры матрицы
_C.PARAMETERS.MAT_SIZE = (39, 39)

# Это можно не трогать
_C.TEST_MODE = CN()
_C.TEST_MODE.MAT = 'Sub-001_a_f.mat'
_C.TEST_MODE.OUT = './test_out'

def get_cfg_defaults():
    """Get a yacs CfgNode object"""
    return _C.clone()
