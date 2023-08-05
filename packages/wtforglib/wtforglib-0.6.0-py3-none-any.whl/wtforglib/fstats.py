"""Top-level module for wtforglib Library."""
import platform
import re
import shutil
from grp import getgrgid
from inspect import stack
from pathlib import Path
from pwd import getpwuid
from typing import Optional, Union

from wtforglib.kinds import Fspec

OwnGrpId = Optional[Union[str, int]]

WINDOZE = "Windows"
WINDOZE_NOT_IMPLEMENTED = "{0} is not implemented on Windows"


def set_file_perms(tgt: Fspec, mode: str) -> bool:
    """Sets the owner group permissions for a posix file if needed.

    Parameters
    ----------
    tgt : Fspec
        Path to the target file
    mode : str
        Mode of the target file

    Returns
    -------
    bool : True if changes are made to the target

    Raises
    ------
    ValueError
        When mode is not valid
    NotImplementedError
        When Windows platform
    """
    target = Path(tgt)
    mode_length = len(mode)
    if mode_length > 4 or mode_length < 3:
        raise ValueError("Invalid mode string length. Must be 3 or 4 characters.")
    if not re.match("[0-7]+$", mode):
        raise ValueError("Invalid mode string. Must be 3 or 4 octal digits.")
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(stack()[0][3]),
        )  # pragma: no cover
    # convert mode to octal string right 4 chars
    cmode = str(oct(target.stat().st_mode))[-mode_length:]
    if cmode != mode:
        omode = int(mode, 8)
        target.chmod(omode)
        return True
    return False


def get_new_owner(tgt: Fspec, own: OwnGrpId) -> Optional[str]:
    """Sets the owner for a posix file in needed.

    Parameters
    ----------
    tgt : Fspec
        Path to the target file
    own : OwnGrpId
        Owner of the target file

    Returns
    -------
    Optional[str] : new_owner or None

    Raises
    ------
    NotImplementedError
        When Windows platform
    """
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(stack()[0][3]),
        )  # pragma: no cover
    new_owner: Optional[str]
    if own:
        if isinstance(own, int):
            new_owner = getpwuid(own)[0]
        else:
            new_owner = str(own)
        if Path(tgt).owner() == new_owner:
            new_owner = None
    else:
        new_owner = None
    return new_owner


def get_new_group(tgt: Fspec, grp: OwnGrpId) -> Optional[str]:
    """Sets the owner for a posix file in needed.

    Parameters
    ----------
    tgt : Fspec
        Path to the target file
    grp : OwnGrpId
        Group of the target file

    Returns
    -------
    Optional[str] : new_group or None

    Raises
    ------
    NotImplementedError
        When Windows platform
    """
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(stack()[0][3]),
        )  # pragma: no cover
    new_group: Optional[str]
    if grp:
        if isinstance(grp, int):
            new_group = getgrgid(grp)[0]
        else:
            new_group = str(grp)
        if Path(tgt).group() == new_group:
            new_group = None
    else:
        new_group = None
    return new_group


def set_owner_group(tgt: Fspec, own: OwnGrpId, grp: OwnGrpId) -> bool:
    """Sets the owner group for a posix file in needed.

    Parameters
    ----------
    tgt : Fspec
        Path to the target file
    own : str
        Owner of the target file
    grp : str
        Group of the target file

    Returns
    -------
    bool : True if changes are made to the target

    Raises
    ------
    NotImplementedError
        When Windows platform
    """
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(stack()[0][3]),
        )  # pragma: no cover
    target = Path(tgt)
    new_owner = get_new_owner(target, own)
    new_group = get_new_group(target, grp)
    if (new_group is not None) or (new_owner is not None):
        shutil.chown(target, new_owner, new_group)  # type: ignore
        return True
    return False


def set_owner_group_perms(tgt: Fspec, own: OwnGrpId, grp: OwnGrpId, mode: str) -> bool:
    """Sets the owner group permissions for a posix file if needed.

    Parameters
    ----------
    tgt : Fspec
        Path to the target file
    own : str
        Owner of the target file
    grp : str
        Group of the target file
    mode : str
        Mode of the target file

    Returns
    -------
    bool : True if changes are made to the target

    Raises
    ------
    NotImplementedError
        When Windows platform
    """
    if platform.system() == WINDOZE:
        raise NotImplementedError(
            WINDOZE_NOT_IMPLEMENTED.format(stack()[0][3]),
        )  # pragma: no cover
    og_changed = set_owner_group(tgt, own, grp)
    fp_changed = set_file_perms(tgt, mode)
    return og_changed or fp_changed
