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

# 终端中用于控制颜色的字符
# 详见：https://en.wikipedia.org/wiki/ANSI_escape_code（包括数字颜色代码）
_CSI_S = ';'
_CSI_H = '\033['
_CSI_T = 'm'

# 程序运行于 IDLE 上的标志
# 关心是否运行于 IDLE Shell 上是因为 IDLE 不支持前背景色，需要区别对待
run_on_idle = False
# 导入 IDLE 相关模块成功标志
_idle_imported = False
# 导入第三方模块 colorama 标志
_colorama_imported = False
# 运行于 windows 平台标志
_NT = os_name == 'nt'

# 尝试导入 IDLE 输出流，成功则设置 _idle_imported 为 True
try:
    from idlelib.run import StdOutputFile

    _idle_imported = True
except Exception:
    pass

# 导入成功也不代表运行 IDLE 上，要看输出流是否是上面导入的 StdOutputFile
if _idle_imported:
    run_on_idle = isinstance(sys_stdout, StdOutputFile)

# 如果程序是运行在 windows 平台上并且不是运行于 IDLE
# 那就需要 colorama 模块帮助显示字符颜色
# 其他平台直接输入终端颜色代码即可达到目的，没 windows 这么麻烦
if _NT and not run_on_idle:
    try:
        from colorama import init, Fore, Back

        # 导入 colorama 的输出流 StreamWrapper，主模块用于判断输出流是否非文件
        from colorama.ansitowin32 import StreamWrapper

        # 设置 colorama 导入标志为真
        _colorama_imported = True
        # colorama 用法，设置自动结束颜色为真
        init(autoreset=True)
    except ImportError:
        # 导入失败（没安装 colorama 模块等原因）显示提示
        from warnings import warn

        warn(
            'If you want to print in color on the windows console, '
            'please use "pip3 install colorama" to install the "colorama" module.'
        )


class MixedColors(object):
    '''
    混合色类
    与不同数据类型相加，返回不同值
    '''

    def __init__(self, *codes):
        '''
        初始化
        :param codes: list，数字颜色代码列表
        '''
        self.codes = list()
        self.codes.extend(codes)

    def __add__(self, other):
        '''
        定义两数据类型相加魔法方法
        :param other: 相加时的其他类实例，支持：MixedColors，Monochrome，str 类。
        :return: ...
        '''
        if isinstance(other, str):
            # 如果加号右边是字符串
            if not other:
                # 加号右边是空字符串则返回混合色实例自身
                return self
            if not self.codes:
                # 颜色代码列表为空则返回原字符串（不修改原字符串）
                return other
            # 生成以分号分割的数字颜色代码
            string = _CSI_S.join(str(c) for c in self.codes)
            # 生成设置颜色码，比如 \033[31;42m
            setter = ''.join((_CSI_H, string, _CSI_T))
            # 重置颜色码
            resetter = '\033[0m'
            # 返回 设置颜色码 + 字符串 + 重置颜色码 形式的字符串
            return ''.join((setter, other, resetter))
        elif isinstance(other, Monochrome):
            # 如果加号右边是单色类 Monochrome 实例，则将其数字颜色代码
            # 添加至"混合色 MixedColors"类实例的颜色码列表，返回混合色实例自身
            self.codes.append(other.code)
            return self
        elif isinstance(other, MixedColors):
            # 如果加号右边也是一个"混合色 MixedColors"类实例,则将它的颜色码取来
            # 扩展本实例的颜色码列表，并返回本实例自身
            self.codes.extend(other.codes)
            return self
        else:
            # 加号右边是其他数据类型则抛出异常，结束
            raise TypeError(
                'Unsupported operand type for +: "%s" and "%s".'
                % (type(self).__name__, type(other).__name__)
            )

    def __radd__(self, other):
        # 加号左边数据类型没有定义 __add__ 方法或不支持相加右边数据类型时
        # 会调用右边数据的 __radd__ 方法，如：字符串 + 本类实例，这里把他变成左相加，用 __add__代理
        return self + other


class Monochrome(object):
    '''
    单色类
    与不同数据类型相加，返回不同值
    '''

    def __init__(self, code):
        '''
        类初始化方法
        :param code: int，数字颜色代码
        '''
        self.code = code

    def __add__(self, other):
        '''
        定义两数据类型相加魔法方法
        :param other: 相加时的其他类实例，支持：MixedColors，Monochrome，str 类。
        :return: 与"混合色 MixedColors"类基本同理，不同的是这里返回的是 MixedColors 实例
        而不是本类实例，因为本单色类实例不能被改变，否则就"变色"了，下次取用时本类实例代表颜色就不对了
        '''
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


# 程序运行于 windows 平台上则用不到以上两个类，需要第三方模块 colorama 来支持显示颜色


class _ColorGroup(object):
    # 运行于 widdows 平台并且 colorama 模块成功导入
    # 则将本"颜色组 _ColorGroup"对应颜色属性设置为 colorama 对应的颜色属性
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
        # 运行于其他平台则用数字颜色代码来构建颜色
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
        # 访问本类不存在的属性会调用此方法，一律抛出异常
        raise ValueError('No color option like "%s".' % name)

    def __getattribute__(self, name):
        # 定义获取本类属性的魔法方法
        # 如果运行于 windows 平台且 colorama 模块没导入成功
        # 则访问本类属性时返回空字符串（主模块 ctcore 中用于与其他字符串相加）
        if _NT and not _colorama_imported:
            return ''
        # 调用父类魔法方法返回本类属性值
        obj = super().__getattribute__(name)
        # 如果本类对应名字为 name 的属性是数字，则返回"单色 Monochrome"类实例
        if isinstance(obj, int):
            return Monochrome(obj)
        # 否则返回原本属性值（也就是 colorama 模块对应的属性值）
        return obj


# 实例化颜色组，供主模块 ctcore 导入使用
_colors = _ColorGroup()
