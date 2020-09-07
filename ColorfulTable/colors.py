# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2020 hrpzcf / hrp < hrpzcf@foxmail.com >

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import name as os_name
from sys import stdout as sys_stdout

_CSI_S = ';'
_CSI_H = '\033['
_CSI_T = 'm'

run_on_idle = False

_idle_imported = False
_colorama_imported = False
_NT = os_name == 'nt'

try:
    from idlelib.run import StdOutputFile

    _idle_imported = True
except Exception:
    pass

if _idle_imported:
    run_on_idle = isinstance(sys_stdout, StdOutputFile)

if _NT and not run_on_idle:
    try:
        from colorama import init, Fore, Back
        from colorama.ansitowin32 import StreamWrapper

        _colorama_imported = True
        init(autoreset=True)
    except ImportError:
        from warnings import warn

        warn(
            'If you want to print in color on the windows console, please use "pip3 install colorama" to install the "colorama" module.'
        )


class MixedColors(object):
    def __init__(self, *codes):
        self.codes = list()
        self.codes.extend(codes)

    def __add__(self, other):
        if isinstance(other, str):
            if not other:
                return self
            if not self.codes:
                return ''
            string = _CSI_S.join(str(c) for c in self.codes)
            setter = ''.join((_CSI_H, string, _CSI_T))
            resetter = '\033[0m'
            return ''.join((setter, other, resetter))
        elif isinstance(other, Monochrome):
            self.codes.append(other.code)
            return self
        elif isinstance(other, MixedColors):
            self.codes.extend(other.codes)
            return self
        else:
            raise TypeError(
                'Unsupported operand type for +: "%s" and "%s".'
                % (type(self).__name__, type(other).__name__)
            )

    def __radd__(self, other):
        return self + other


class Monochrome(object):
    def __init__(self, code):
        self.code = code

    def __add__(self, other):
        if isinstance(other, str):
            if not other:
                return MixedColors(self.code)
            setter = ''.join((_CSI_H, str(self.code), _CSI_T))
            resetter = '\033[0m'
            return ''.join((setter, other, resetter))
        elif isinstance(other, Monochrome):
            return MixedColors(self.code, other.code)
        elif isinstance(other, MixedColors):
            other.codes.append(self.code)
            return other
        else:
            raise TypeError(
                'Unsupported operand type for +: "%s" and "%s".'
                % (type(self).__name__, type(other).__name__)
            )

    def __radd__(self, other):
        return self + other


class _ColorGroup(object):
    if _NT and _colorama_imported:
        fg_Reset = Fore.RESET
        fg_Red = Fore.RED
        fg_Green = Fore.GREEN
        fg_Yellow = Fore.YELLOW
        fg_Blue = Fore.BLUE
        fg_Magenta = Fore.MAGENTA
        fg_Cyan = Fore.CYAN
        fg_White = Fore.WHITE
        fg_BrightBlack = Fore.LIGHTBLACK_EX
        fg_BrightRed = Fore.LIGHTRED_EX
        fg_BrightGreen = Fore.LIGHTGREEN_EX
        fg_BrightYellow = Fore.LIGHTYELLOW_EX
        fg_BrightBlue = Fore.LIGHTBLUE_EX
        fg_BrightMagenta = Fore.LIGHTMAGENTA_EX
        fg_BrightCyan = Fore.LIGHTCYAN_EX
        fg_BrightWhite = Fore.LIGHTWHITE_EX

        bg_Reset = Back.RESET
        bg_Red = Back.RED
        bg_Green = Back.GREEN
        bg_Yellow = Back.YELLOW
        bg_Blue = Back.BLUE
        bg_Magenta = Back.MAGENTA
        bg_Cyan = Back.CYAN
        bg_White = Back.WHITE
        bg_BrightBlack = Back.LIGHTBLACK_EX
        bg_BrightRed = Back.LIGHTRED_EX
        bg_BrightGreen = Back.LIGHTGREEN_EX
        bg_BrightYellow = Back.LIGHTYELLOW_EX
        bg_BrightBlue = Back.LIGHTBLUE_EX
        bg_BrightMagenta = Back.LIGHTMAGENTA_EX
        bg_BrightCyan = Back.LIGHTCYAN_EX
        bg_BrightWhite = Back.LIGHTWHITE_EX
    else:
        fg_Reset = 0
        fg_Red = 31
        fg_Green = 32
        fg_Yellow = 33
        fg_Blue = 34
        fg_Magenta = 35
        fg_Cyan = 36
        fg_White = 37
        fg_BrightBlack = 90
        fg_BrightRed = 91
        fg_BrightGreen = 92
        fg_BrightYellow = 93
        fg_BrightBlue = 94
        fg_BrightMagenta = 95
        fg_BrightCyan = 96
        fg_BrightWhite = 97

        bg_Reset = 0
        bg_Red = 41
        bg_Green = 42
        bg_Yellow = 43
        bg_Blue = 44
        bg_Magenta = 45
        bg_Cyan = 46
        bg_White = 47
        bg_BrightBlack = 100
        bg_BrightRed = 101
        bg_BrightGreen = 102
        bg_BrightYellow = 103
        bg_BrightBlue = 104
        bg_BrightMagenta = 105
        bg_BrightCyan = 106
        bg_BrightWhite = 107

    def __getattr__(self, name):
        raise AttributeError('No color option like "%s".' % name)

    def __getattribute__(self, name):
        if _NT and not _colorama_imported:
            return ''
        obj = super().__getattribute__(name)
        if isinstance(obj, int):
            return Monochrome(obj)
        return obj


_colors = _ColorGroup()
