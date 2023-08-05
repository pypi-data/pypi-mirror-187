"""Top-level module for wtforglib Library."""
from grp import getgrall, getgrgid
from pwd import getpwnam, getpwuid
from typing import Tuple, Union


def get_user_name(uid: int) -> str:
    """Returns the user name of the user identified by uid.

    Parameters
    ----------
    uid : int
        User id

    Returns
    -------
    str
        User name
    """
    return getpwuid(uid)[0]


def get_user_groups(user: Union[str, int]) -> Tuple[str, ...]:
    """Returns a tuple of groups user belongs to.

    Parameters
    ----------
    user : Union[str, int]
        User name or uid

    Returns
    -------
    Tuple[str,...]
        Groups user belongs to
    """
    if isinstance(user, int):
        user_nm = get_user_name(int(user))
    else:
        user_nm = user
    groups = [gg.gr_name for gg in getgrall() if user_nm in gg.gr_mem]
    gid = getpwnam(user_nm).pw_gid
    groups.append(getgrgid(gid).gr_name)
    return tuple(groups)
