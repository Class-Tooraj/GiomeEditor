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