from yacs.config import CfgNode as CN

_C = CN()

_C.PATH = CN()
_C.PATH.MAT_FOLDER = './RN_Only Matrices_6 June 2022'
_C.PATH.OUT_FOLDER = './output'
_C.PATH.FINAL_XLSX_FILE = 'FULL_DATA.xlsx'

_C.PARAMETERS = CN()
_C.PARAMETERS.MAT_SIZE = (39, 39)

_C.TEST_MODE = CN()
_C.TEST_MODE.MAT = 'Sub-001_a_f.mat'
_C.TEST_MODE.OUT = './test_out'

def get_cfg_defaults():
    """Get a yacs CfgNode object"""
    return _C.clone()
