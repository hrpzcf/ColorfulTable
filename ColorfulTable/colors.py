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
            'If you want to print in color on the windows \
console, please use "pip3 install colorama" to install the "colorama" module.'
        )

_CSI_S = ';'
_CSI_H = '\033['
_CSI_T = 'm'


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


class _ForegroundGroup(object):
    if _NT and _colorama_imported:
        Reset = Fore.RESET
        Red = Fore.RED
        Green = Fore.GREEN
        Yellow = Fore.YELLOW
        Blue = Fore.BLUE
        Magenta = Fore.MAGENTA
        Cyan = Fore.CYAN
        White = Fore.WHITE
        BrightBlack = Fore.LIGHTBLACK_EX
        BrightRed = Fore.LIGHTRED_EX
        BrightGreen = Fore.LIGHTGREEN_EX
        BrightYellow = Fore.LIGHTYELLOW_EX
        BrightBlue = Fore.LIGHTBLUE_EX
        BrightMagenta = Fore.LIGHTMAGENTA_EX
        BrightCyan = Fore.LIGHTCYAN_EX
        BrightWhite = Fore.LIGHTWHITE_EX
    else:
        Reset = 0
        Red = 31
        Green = 32
        Yellow = 33
        Blue = 34
        Magenta = 35
        Cyan = 36
        White = 37
        BrightBlack = 90
        BrightRed = 91
        BrightGreen = 92
        BrightYellow = 93
        BrightBlue = 94
        BrightMagenta = 95
        BrightCyan = 96
        BrightWhite = 97

    def __getattr__(self, name):
        raise AttributeError('No color option like "%s".' % name)

    def __getattribute__(self, name):
        if _NT and not _colorama_imported:
            return ''
        obj = super().__getattribute__(name)
        if isinstance(obj, int):
            return Monochrome(obj)
        return obj


class _BackgroundGroup(object):
    if _NT and _colorama_imported:
        Reset = Back.RESET
        Red = Back.RED
        Green = Back.GREEN
        Yellow = Back.YELLOW
        Blue = Back.BLUE
        Magenta = Back.MAGENTA
        Cyan = Back.CYAN
        White = Back.WHITE
        BrightBlack = Back.LIGHTBLACK_EX
        BrightRed = Back.LIGHTRED_EX
        BrightGreen = Back.LIGHTGREEN_EX
        BrightYellow = Back.LIGHTYELLOW_EX
        BrightBlue = Back.LIGHTBLUE_EX
        BrightMagenta = Back.LIGHTMAGENTA_EX
        BrightCyan = Back.LIGHTCYAN_EX
        BrightWhite = Back.LIGHTWHITE_EX
    else:
        Reset = 0
        Red = 41
        Green = 42
        Yellow = 43
        Blue = 44
        Magenta = 45
        Cyan = 46
        White = 47
        BrightBlack = 100
        BrightRed = 101
        BrightGreen = 102
        BrightYellow = 103
        BrightBlue = 104
        BrightMagenta = 105
        BrightCyan = 106
        BrightWhite = 107

    def __getattr__(self, name):
        raise AttributeError('No color option like "%s".' % name)

    def __getattribute__(self, name):
        if _NT and not _colorama_imported:
            return ''
        obj = super().__getattribute__(name)
        if isinstance(obj, int):
            return Monochrome(obj)
        return obj


fg = _ForegroundGroup()
bg = _BackgroundGroup()

COLORS = {
    'fg.Reset': fg.Reset,
    'fg.Red': fg.Red,
    'fg.Green': fg.Green,
    'fg.Yellow': fg.Yellow,
    'fg.Blue': fg.Blue,
    'fg.Magenta': fg.Magenta,
    'fg.Cyan': fg.Cyan,
    'fg.White': fg.White,
    'fg.BrightBlack': fg.BrightBlack,
    'fg.BrightRed': fg.BrightRed,
    'fg.BrightGreen': fg.BrightGreen,
    'fg.BrightYellow': fg.BrightYellow,
    'fg.BrightBlue': fg.BrightBlue,
    'fg.BrightMagenta': fg.BrightMagenta,
    'fg.BrightCyan': fg.BrightCyan,
    'fg.BrightWhite': fg.BrightWhite,
    'bg.Reset': bg.Reset,
    'bg.Red': bg.Red,
    'bg.Green': bg.Green,
    'bg.Yellow': bg.Yellow,
    'bg.Blue': bg.Blue,
    'bg.Magenta': bg.Magenta,
    'bg.Cyan': bg.Cyan,
    'bg.White': bg.White,
    'bg.BrightBlack': bg.BrightBlack,
    'bg.BrightRed': bg.BrightRed,
    'bg.BrightGreen': bg.BrightGreen,
    'bg.BrightYellow': bg.BrightYellow,
    'bg.BrightBlue': bg.BrightBlue,
    'bg.BrightMagenta': bg.BrightMagenta,
    'bg.BrightCyan': bg.BrightCyan,
    'bg.BrightWhite': bg.BrightWhite,
}
