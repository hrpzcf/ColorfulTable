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
        fg_reset = Fore.RESET
        fg_red = Fore.RED
        fg_green = Fore.GREEN
        fg_yellow = Fore.YELLOW
        fg_blue = Fore.BLUE
        fg_magenta = Fore.MAGENTA
        fg_cyan = Fore.CYAN
        fg_white = Fore.WHITE
        fg_brightblack = Fore.LIGHTBLACK_EX
        fg_brightred = Fore.LIGHTRED_EX
        fg_brightgreen = Fore.LIGHTGREEN_EX
        fg_brightyellow = Fore.LIGHTYELLOW_EX
        fg_brightblue = Fore.LIGHTBLUE_EX
        fg_brightmagenta = Fore.LIGHTMAGENTA_EX
        fg_brightcyan = Fore.LIGHTCYAN_EX
        fg_brightwhite = Fore.LIGHTWHITE_EX

        bg_reset = Back.RESET
        bg_red = Back.RED
        bg_green = Back.GREEN
        bg_yellow = Back.YELLOW
        bg_blue = Back.BLUE
        bg_magenta = Back.MAGENTA
        bg_cyan = Back.CYAN
        bg_white = Back.WHITE
        bg_brightblack = Back.LIGHTBLACK_EX
        bg_brightred = Back.LIGHTRED_EX
        bg_brightgreen = Back.LIGHTGREEN_EX
        bg_brightyellow = Back.LIGHTYELLOW_EX
        bg_brightblue = Back.LIGHTBLUE_EX
        bg_brightmagenta = Back.LIGHTMAGENTA_EX
        bg_brightcyan = Back.LIGHTCYAN_EX
        bg_brightwhite = Back.LIGHTWHITE_EX
    else:
        fg_reset = 0
        fg_red = 31
        fg_green = 32
        fg_yellow = 33
        fg_blue = 34
        fg_magenta = 35
        fg_cyan = 36
        fg_white = 37
        fg_brightblack = 90
        fg_brightred = 91
        fg_brightgreen = 92
        fg_brightyellow = 93
        fg_brightblue = 94
        fg_brightmagenta = 95
        fg_brightcyan = 96
        fg_brightwhite = 97

        bg_reset = 0
        bg_red = 41
        bg_green = 42
        bg_yellow = 43
        bg_blue = 44
        bg_magenta = 45
        bg_cyan = 46
        bg_white = 47
        bg_brightblack = 100
        bg_brightred = 101
        bg_brightgreen = 102
        bg_brightyellow = 103
        bg_brightblue = 104
        bg_brightmagenta = 105
        bg_brightcyan = 106
        bg_brightwhite = 107

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
