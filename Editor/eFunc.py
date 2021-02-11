__author__ = "Tooraj_Jahangiri"
__email__ = "toorajjahangiri@gmail.com"

from PySide6.QtCore import Slot
from typing import Union


@Slot(tuple)
def talk(*args: str) -> tuple:
    """
    talk function is slot for signal

    argument args: signals you send
    type args: str

    return tuple
    """
    
    return args

def fileFormat(uFormat: Union[str, list, tuple, set] = None) -> str:
    """
    fileFormat function return format file for Open and Save

    argument uFormat: signals you send
    type uFormat: str

    return str
    """

    dec = {"Normal Text (*.txt)","All File (*.*)"}

    if uFormat is None:
        _formats = ';;'.join(dec)
        return _formats

    if isinstance(uFormat, str):
        uFormat = uFormat.split(';;')
    
    dec.update(uFormat)

    return ';;'.join(dec)


def hshTrans(hsh: str) -> str:
    """
    Hash String to Alphabet
    Alphabet to Hash String
    """
    
    t_tbl = {
    '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E',
    '5': 'F', '6': 'G', '7':'H', '8': 'I', '9': 'J',
    }

    if hsh.isdigit():
        trn = str.maketrans(''.join(t_tbl.keys()), ''.join(t_tbl.values()))
    
    elif hsh.isupper():
        trn = str.maketrans(''.join(t_tbl.values()), ''.join(t_tbl.keys()))
    
    else:
        raise ValueError(f"Hash String or hshTrans input. Support\n{t_tbl.items()}")

    return hsh.translate(trn)