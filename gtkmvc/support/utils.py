#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2007 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.

import inspect
import os

def getmembers(_object, _predicate):
    """This is an implementation of inspect.getmembers, as in some versions 
    of python it may be buggy. 
    See issue at http://bugs.python.org/issue1785"""
    # This should be:
    #return inspect.getmembers(_object, _predicate)
    
    # ... and it is re-implemented as:
    observers = []
    for key in dir(_object):
        try: m = getattr(_object, key)
        except AttributeError: continue
        if _predicate(m): observers.append((key, m))
        pass
    return observers


# ======================================================================
# This is taken from python 2.6 (os.path.relpath is supported in 2.6)
#
# Copyright (c) 2001 Python Software Foundation; All Rights Reserved
# This code about relpath is covered by the Python Software Foundation
# (PSF) Agreement. See http://docs.python.org/license.html for details.
# ======================================================================
def __posix_relpath(path, start=os.curdir):
    """Return a relative version of a path"""

    if not path: raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list: return os.curdir
    return os.path.join(*rel_list)

# This is taken from python 2.6 (os.path.relpath is supported in 2.6)
# This is for windows
def __nt_relpath(path, start=os.curdir):
    """Return a relative version of a path"""

    if not path: raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)
    if start_list[0].lower() != path_list[0].lower():
        unc_path, rest = os.path.splitunc(path)
        unc_start, rest = os.path.splitunc(start)
        if bool(unc_path) ^ bool(unc_start):
            raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)" \
                             % (path, start))
        else: raise ValueError("path is on drive %s, start on drive %s" \
                               % (path_list[0], start_list[0]))
    # Work out how much of the filepath is shared by start and path.
    for i in range(min(len(start_list), len(path_list))):
        if start_list[i].lower() != path_list[i].lower():
            break
        else: i += 1
        pass
    
    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list: return os.curdir
    return os.path.join(*rel_list)
try: 
    import os.path.relpath
    relpath = os.path.relpath
except ImportError:
    if os.name == 'nt':
        relpath = __nt_relpath
    else:
        relpath = __posix_relpath
        pass
    pass
# ======================================================================
# End of code covered by PSF License Agreement
# ======================================================================
