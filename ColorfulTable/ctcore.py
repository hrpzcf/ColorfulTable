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

import sys
from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Iterator
from io import TextIOWrapper
from os import linesep as os_linesep
from os import name as os_name

from .colors import _colors, run_on_idle

try:
    from .colors import StreamWrapper
except ImportError:
    StreamWrapper = TextIOWrapper

try:
    from .colors import StdOutputFile
except ImportError:
    StdOutputFile = TextIOWrapper

_COLORFUL = True
_LNSEP = os_linesep
_NT = os_name == 'nt'

MAX_ROW_HEIGHT = 20
MAX_COLUMN_WIDTH = 80
MAX_COLUMN_NUM = 30

__ALIGNH__ = 'l left c center r right'
__ALIGNV__ = 't top m middle b bottom'
__STYLES__ = 'table simple classic table-ascii simple-ascii classic-ascii'
__EXCLUDED__ = '\b', '\r', '\t', '\v'


class Style(object):
    def __init__(self, style='table'):
        '''
        初始化方法。
        :param style: 预置风格，可用:
            1.table
            2.simple
            3.classic
            4.table-ascii
            5.simple-ascii
            6.classic-ascii
        '''
        Style._check_init(style)
        self._initialize()
        self.choose(style)

    @staticmethod
    def _check_init(style):
        '''
        检查参数是否是 6 个可用字符串之一。
        :param style: str，可用值见类初始化参数注释。
        '''
        if style not in __STYLES__.split():
            raise ValueError(
                'No style option like <%s>, available: %s.' % (style, __STYLES__)
            )

    def _initialize(self):
        '''
        给类属性赋予初始值，这些属性值就是列表边框线的组成成分。
        '''
        self.cell_pad = '  '
        self.top_left = '┌'
        self.top_cross = '┬'
        self.top_right = '┐'
        self.top_horz = '─'
        self.bottom_left = '└'
        self.bottom_cross = '┴'
        self.bottom_right = '┘'
        self.bottom_horz = '─'
        self.left_cross = '├'
        self.left_vert = '│'
        self.right_cross = '┤'
        self.right_vert = '│'
        self.center_horz = '─'
        self.center_vert = '│'
        self.center_cross = '┼'
        self.split_left = '╞'
        self.split_right = '╡'
        self.split_horz = '═'
        self.split_cross = '╪'

    def choose(self, style):
        '''
        选择预设表格边框线风格方法。
        根据字符串（style的值）批量设置不同属性值。
        :param style: str，可用值见类初始化参数注释。
        '''
        # 先检查参数 style 是否有效。
        Style._check_init(style)
        # 设置初始值，以后的修改都基于初始属性值修改。
        self._initialize()
        # style 参数值是 table 就无需更改初始属性值了，全部采用初始值。
        if style == 'table':
            pass
        # 根据 style 值修改不同属性为不同的值，以下注释掉的属性赋值就是使用初始值，不修改。
        elif style == 'simple':
            # self.cell_pad = '  '
            self.top_left = ''
            self.top_cross = ''
            self.top_right = ''
            self.top_horz = ''
            self.bottom_left = ''
            self.bottom_cross = '─'
            self.bottom_right = ''
            self.bottom_horz = '─'
            self.left_cross = ''
            self.left_vert = ''
            self.right_cross = ''
            self.right_vert = ''
            self.center_horz = ''
            self.center_vert = ' '
            self.center_cross = ''
            self.split_left = ''
            self.split_right = ''
            # self.split_horz = '═'
            self.split_cross = ' '
        elif style == 'classic':
            # self.cell_pad = '  '
            # self.top_left = '┌'
            # self.top_cross = '┬'
            # self.top_right = '┐'
            # self.top_horz = '─'
            # self.bottom_left = '└'
            # self.bottom_cross = '┴'
            # self.bottom_right = '┘'
            # self.bottom_horz = '─'
            self.left_cross = ''
            # self.left_vert = '│'
            self.right_cross = ''
            # self.right_vert = '│'
            self.center_horz = ''
            # self.center_vert = '│'
            self.center_cross = ''
            # self.split_left = '╞'
            # self.split_right = '╡'
            # self.split_horz = '═'
            # self.split_cross = '╪'
        elif style == 'table-ascii':
            # self.cell_pad = '  '
            self.top_left = '+'
            self.top_cross = '+'
            self.top_right = '+'
            self.top_horz = '-'
            self.bottom_left = '+'
            self.bottom_cross = '+'
            self.bottom_right = '+'
            self.bottom_horz = '-'
            self.left_cross = '+'
            self.left_vert = '|'
            self.right_cross = '+'
            self.right_vert = '|'
            self.center_horz = '-'
            self.center_vert = '|'
            self.center_cross = '+'
            self.split_left = '+'
            self.split_right = '+'
            self.split_horz = '='
            self.split_cross = '+'
        elif style == 'simple-ascii':
            # self.cell_pad = '  '
            self.top_left = ''
            self.top_cross = ''
            self.top_right = ''
            self.top_horz = ''
            self.bottom_left = ''
            self.bottom_cross = '-'
            self.bottom_right = ''
            self.bottom_horz = '-'
            self.left_cross = ''
            self.left_vert = ''
            self.right_cross = ''
            self.right_vert = ''
            self.center_horz = ''
            self.center_vert = ' '
            self.center_cross = ''
            self.split_left = ''
            self.split_right = ''
            self.split_horz = '='
            self.split_cross = ' '
        elif style == 'classic-ascii':
            # self.cell_pad = '  '
            self.top_left = '+'
            self.top_cross = '+'
            self.top_right = '+'
            self.top_horz = '-'
            self.bottom_left = '+'
            self.bottom_cross = '+'
            self.bottom_right = '+'
            self.bottom_horz = '-'
            self.left_cross = ''
            self.left_vert = '|'
            self.right_cross = ''
            self.right_vert = '|'
            self.center_horz = ''
            self.center_vert = '|'
            self.center_cross = ''
            self.split_left = '+'
            self.split_right = '+'
            self.split_horz = '-'
            self.split_cross = '+'

    def reset(self):
        '''
        重置表格边框线方法（设置为初始值）。
        '''
        self._initialize()

    def __setattr__(self, name, value):
        '''
        自定义设置属性值的魔法方法，增加检查要设置的属性值是否是字符串。
        如果不是字符串则抛出 TypeError 异常。
        :param name: str，属性名。
        :param value: str，属性值。
        '''
        # 要设置的值不是 str 类型则抛出异常。
        if not isinstance(value, str):
            raise TypeError('Type of attributes of <class "Style"> can only be "str".')
        # 调用父类 __setattr__ 魔法方法设置属性值。
        super().__setattr__(name, value)


class _RowObj(list):
    '''
    表格的"行"类，继承自 list。
    '''

    def __init__(self, iterable, cwhandle, rowhit, alignh, alignv, fbgc):
        '''
        初始化方法。
        :param iterable: Iterable，可迭代对象，其中的元素即一行中各单元格的元素。
        :param cwhandle: list，列宽列表，所有 _RowObj 类实例（即"行"）初始化时
        都传进同一个列宽列表，所以写 handle（句柄）。
        :param rowhit: int，行高（指的是包含多个单元格的"行"的字符行数），不小于 1。
        :param alignh: str，水平对齐方式，可用值见全局变量 __ALIGNH__。
        :param alignv: str，垂直对齐方式，可用值见全局变量 __ALIGNV__。
        :param fbgc: set[str]，前景色背景色集合，集合内字符串可用值见项目目录下 README.md。
        '''
        # 调用父类初始化方法初始化，即 list(iterable)，此时实例 self 就是一个列表。
        super().__init__(iterable)
        # 单元格水平对齐方式属性，类型为 str，可用值见 __ALIGNH__ 全局变量。
        self._alignh = alignh
        # 单元格垂直对齐方式属性，类型为 str，可用值见 __ALIGNV__ 全局变量。
        self._alignv = alignv
        # 根据"行"(_RowObj 实例，self)中单元格(列表元素)数量生成水平对齐方式列表。
        self._alignhs = [alignh] * len(self)
        # 根据"行"(_RowObj 实例，self)中单元格(列表元素)数量生成垂直对齐方式列表。
        self._alignvs = [alignv] * len(self)
        # 单元格前景色背景色集合属性，类型为 set[str]。
        self._fbgc = fbgc
        # 根据"行"(_RowObj 实例，self)中单元格(列表元素)数量生成前背景色列表:list[set[str]]。
        self._fbgcs = [fbgc.copy() for _ in self]
        # 行高属性，int。
        self._row_hit = rowhit
        # 列宽列表属性，list。
        self._col_wids = cwhandle

    def _addcol(self, index, value):
        '''
        单"行"的添加列方法，因是单行所以实际上就是添加一个单元格(元素)。
        :param index: int，要插入位置索引，即列索引。
        :param value: 要插入的值，不限数据类型。
        '''
        # 给"行"插入一个单元格（元素）。
        self.insert(index, value)
        # 同时对水平、垂直对齐方式列表同样位置插入默认对齐方式。
        self._alignhs.insert(index, self._alignh)
        self._alignvs.insert(index, self._alignv)
        # 前背景色列表也在相同位置插入默认颜色集合。
        self._fbgcs.insert(index, self._fbgc.copy())

    def _delcol(self, index):
        '''
        单"行"的删除列方法，因是单行所以实际上就是删除一个单元格（元素）。
        :param index: int，要删除的列索引。
        :return: 返回被删除的元素。
        '''
        # 水平、垂直对齐方式列表和前背景色列表也做相应的删除操作。
        del self._fbgcs[index]
        del self._alignhs[index]
        del self._alignvs[index]
        return self.pop(index)

    def _height(self, height):
        '''
        设置行高方法，即将"行"的"行高"属性设置为给出的行高。
        :param height: int，可用值为 0 和正整数。
        '''
        self._row_hit = height

    def _setclr(self, index, clrs):
        '''
        "行"的设置前背景色方法。
        :param index: int，索引参数。
        :param clrs: set[str]，颜色集合。
        '''
        self._fbgcs[index].clear()
        if not clrs:
            return
        if not isinstance(clrs, set):
            clrs = set(clrs)
        self._fbgcs[index].update(clrs)

    def _getclr(self, index):
        '''
        获取单元格颜色集合的方法。
        :param index: int，列索引参数。
        :return: set，单元格的颜色集合。
        '''
        return self._fbgcs[index]

    def _gettext(self, left_vert, center_vert, right_vert, padding):
        '''
        获取"行"的文本格式的方法，即将各单元格所存对象的字符，按对齐、颜色、垂直边框线等要求
        构建的文本格式。
        :param left_vert: str，左垂直边框线
        :param center_vert: str，中间垂直边框线
        :param right_vert: str，右垂直边框线
        :param padding: str，单元格内容两侧填充
        :return: str，构建完成的"行"的文本格式
        '''
        # 假设"行"的源数据为：['0123', 'abcdefg', 'h', '']
        # 假设列宽：[3, 3, 3, 2]，行高为 0 (自动)，水平对齐为 c，垂直对齐为 m。
        # 则 _form 方法的返回值是以下数据形式：
        # 表格行 = [
        # 小行 1：['012'， 'abc'， '   ', '  '],
        # 小行 2：[' 3 '， 'def'， ' h ', '  '],
        # 小行 3：['   '， ' g '， '   ', '  '],
        # ]
        row_fmted = self._form(padding)
        if not row_fmted:
            return
        for line in row_fmted:
            # 为每个文本行的最左、最右分别加上"左(left_vert)右(right_vert)垂直边框线"
            line[0] = ''.join((left_vert, line[0]))
            line[-1] = ''.join((line[-1], right_vert))
        # 用"中间垂直边框线(center_vert)"把"文本行"列表串成字符串形式
        # 每个"文本行"之间用换行符串起来，得到一个"表格行"的字符串形式并返回
        return _LNSEP.join(center_vert.join(line) for line in row_fmted)

    def _colcap(self, index):
        '''
        "表格行"的获取指定列最大列宽值方法。
        :param index: int，列索引
        :return: int，最大列宽值
        '''
        # 注意列宽不能为 0，所以 "..or 1"
        return _str_wid(str(self[index])) or 1

    def _colflr(self, index):
        '''
        "表格行"的获取指定列列宽下限方法。
        :param index: int，列索引
        :return: int，列宽值下限
        '''
        # 注意，列宽下限值由列中最大的单个字符宽度决定
        string = str(self[index])
        if not string:
            return 1  # 下限不能为 0
        return max(_chr_wid(c) for c in string)

    def _align(self, index, alignh, alignv):
        '''
        "表格行"设置单元格对齐方式方法。
        :param index: int，列索引
        :param alignh: str，水平对齐方式，可用值见 __ALIGNH__ 全局变量
        :param alignv: str，垂直对齐方式，可用值见 __ALIGNV__ 全局变量
        '''
        if alignh is not None:
            # 将"表格行"的水平对齐方式列表对应索引单元格水平对齐设置为 alignh
            self._alignhs[index] = alignh
        if alignv is not None:
            # 将"表格行"的垂直对齐方式列表对应索引单元格垂直对齐设置为 alignv
            self._alignvs[index] = alignv

    def _form(self, padding):
        '''
        创建一个已格式化的"表格行"的二维列表形式，最外层列表表示一个"表格行"，
        每个内层列表表示"表格行"里的每个单元格，内层列表里的元素表示单元格里不同小行的元素。
        但是以上形式的二维列表不方便把它拼接成一个表示"表格行"的大字符串，
        所以，要把它转换成另一个形式：每个内层列表表示一个小行，小行包含多个单元格，
        但只包含单元格里的一部分(一个单元格里几个小行中的一个)，
        就如 _gettext 方法中对本方法返回值的示意图所示。

        :param padding: str，单元格里左右填充字符，用于防止单元格内容过于贴近垂直边框线
        :return: list[list[str]]，已格式化的"表格行"的二维列表形式，如下：
            假设"行"的源数据为：['0123', 'abcdefg', 'h', '']
            假设列宽：[3, 3, 3, 2]，行高为 0 (自动)，水平对齐为 c，垂直对齐为 m。
            则 _form 方法的返回值是以下数据形式：
            表格行 = [
            小行 1：['012'， 'abc'， '   ', '  '],
            小行 2：[' 3 '， 'def'， ' h ', '  '],
            小行 3：['   '， ' g '， '   ', '  '],
            ]
        '''
        # 如果源数据为空(即添加的行是空行，但一般不会出现)
        if not self:
            return
        row_with_cells = _format(
            self,
            self._row_hit,
            self._col_wids,
            self._alignhs,
            self._alignvs,
            self._fbgcs,
            padding,
        )
        # 将已格式化的"表格行"的二维列表形式转换成最终形式
        row_with_lines = [list(tup) for tup in zip(*row_with_cells)]
        return row_with_lines


class Table(list):
    '''
    主表格类，继承自 list。
    '''

    def __init__(
        self,
        header,
        *,
        alignh='l',
        alignv='t',
        rowfixed=0,
        colfixed=0,
        fbgc=None,
        fill='',
        style=None
    ):
        '''
        初始化方法。
        :param header: Iterable，可迭代对象，初始化表格时的表格首行，其实与普通行并无区别，
        删除首行后第二行变首行
        :param alignh: str，水平对齐方式，单元格未指定水平对齐方式时默认使用该对齐方式，
        可用值见 __ALIGNH__ 全局变量值，参数默认值为 l
        :param alignv: str，垂直对齐方式，单元格未指定垂直对齐方式时默认使用该对齐方式，
        可用值见 __ALIGNV__ 全局变量值，参数默认值为 t
        :param rowfixed: int，行高，新添加的行默认使用的行高值，可用值为 0 或
        小于 MAX_ROW_HEIGHT 的整数，参数默认值为 0
        :param colfixed: int，列宽，新添加的行、列默认使用的列宽值，可用值为 0 或
        小于 MAX_COLUMN_WIDTH 的整数，参数默认值为 0
        :param fbgc: set[str]，包含可用代表颜色的字符串的集合，新增的单元格默认使用该前背景色，
        参数默认值为空集合，可用的颜色代表字符为同目录下 colors 模块中 _ColorGroup 类的属性名
        的字符串形式(或见 README.md 文件)
        :param fill: any，任意数据类型，当添加行或列时，添加的行或列长度短于表格现有列数或行数
        时，默认使用 fill 来补足长度，参数默认值为空字符串
        :param style: 数据类型应为 Style 实例，Style 类包含所需的各种边框线
        '''
        # 检查参数是否符合要求
        Table._check_init(header, alignh, alignv, rowfixed, colfixed, fbgc, style)
        # 调用父类初始化方法，因为继承自 list，此时本类实例(self)就是一个列表
        super(Table, self).__init__()
        # rowTexts用于储存表格中"行"的字符串形式
        self.rowTexts = list()
        # 默认水平、垂直对齐方式
        self._alignh = alignh
        self._alignv = alignv
        # 默认使用的固定列宽、行高值
        self._col_fixed = colfixed
        self._row_fixed = rowfixed
        # 默认使用的前背景色集合
        self._fbgcolors = fbgc or set()
        # 默认使用的补足对象
        self._filler = fill
        # 边框线 Style 类实例
        self._style = style or Style()
        # 最终列宽列表(固定列宽列表、列宽上限、下限列表合并，添加最终值进去)
        self._col_wids = list()
        # 可迭代对象转换为列表好计算列表长度
        headlist = list(header)
        # 本类实例添加首行 _RowObj 类实例。因为本类实例和_RowObj类实例都是列表，所以可以用
        # 访问二维列表一样的方法访问本类实例中的源数据(已添加的行、列、单元格)
        self.append(
            _RowObj(
                headlist,  # header
                self._col_wids,  # 最终列宽列表
                self._row_fixed,  # 行高
                self._alignh,  # 水平对齐方式
                'bottom',  # 垂直对齐方式
                self._fbgcolors,  # 前背景色集合
            )
        )
        self._num_rows = 1  # 行数
        self._num_cols = len(headlist)  # 列数
        str_head = _items_to_str(headlist)  # 将 header 中元素转换为字符串用于计算字符宽度等
        # 列固定宽度(用户指定)
        self._col_fixeds = [colfixed for _ in headlist]
        # 列最大宽度(字符串宽度)
        self._col_caps = [_str_wid(s) or 1 for s in str_head]
        # 列宽度下限(由列中宽度最大的单个字符决定)
        self._col_floors = [_max_char_wid(s) for s in str_head]
        # 边框线的部分组合，依次为：
        # 最顶层一行边框线(hat)、首行与主体分隔线(neck)、
        # 主体中各行直接的分隔线(belt)、最底层一行边框线(shoes)
        self._border = dict(hat='', neck='', belt='', shoes='')

    @staticmethod
    def _check_init(header, alignh, alignv, rowfixed, colfixed, fbgc, style):
        '''
        检查初始化参数是否符合要求方法，如果参数不符合要求则抛出异常，中断程序。
        '''
        if not isinstance(header, Iterable):
            raise TypeError('The <header> should be an iterable object.')
        if not header:
            raise ValueError('The <header> cannot be empty!')
        if alignh not in __ALIGNH__.split():
            raise ValueError(
                'No horizontal alignment option like <%s>, available: %s.'
                % (alignh, __ALIGNH__)
            )
        if alignv not in __ALIGNV__.split():
            raise ValueError(
                'No vertical alignment option like <%s>, available: %s.'
                % (alignv, __ALIGNV__)
            )
        if not isinstance(rowfixed, int):
            raise TypeError('Parameter <rowfixed> should be an integer.')
        if rowfixed < 0:
            raise ValueError('The value of <rowfixed> cannot be less than 0.')
        if rowfixed > MAX_ROW_HEIGHT:
            raise ValueError(
                'The fixed row height exceeds the limit(%d), '
                'please modify the value of "MAX_ROW_HEIGHT" if necessary.'
                % MAX_ROW_HEIGHT
            )
        if not isinstance(colfixed, int):
            raise TypeError('Parameter <colfixed> should be an integer.')
        if colfixed < 0:
            raise ValueError('The value of <colfixed> cannot be less than 0.')
        if colfixed > MAX_COLUMN_WIDTH:
            raise ValueError(
                'The fixed column width exceeds the limit(%d), '
                'please modify the value of "MAX_COLUMN_WIDTH" if necessary.'
                % MAX_COLUMN_WIDTH
            )
        if not isinstance(fbgc, (tuple, list, set)) and fbgc is not None:
            raise TypeError(
                'Type of parameter <fbgc> should be "tuple"、"list" or "set".'
            )
        if fbgc is not None and (not all(isinstance(s, str) for s in fbgc)):
            raise ValueError(
                'The type of the color name in the collection can only be "str".'
            )
        if not isinstance(style, Style) and style is not None:
            raise TypeError('Parameter <style> should be a "Style" object.')

    def _check_index(self, rowindex=None, colindex=None):
        '''
        检查行列索引值是否是整数及是否超出范围方法(索引值为 None 不检查)
        :param rowindex: int，要检查的行索引值
        :param colindex: int，要检查的列索引值
        '''
        if rowindex is not None:
            if not isinstance(rowindex, int):
                raise TypeError('Row index should be an integer.')
            if -self._num_rows > rowindex >= self._num_rows:
                raise IndexError('Row index out of range.')
        if colindex is not None:
            if not isinstance(colindex, int):
                raise TypeError('Column index should be an integer.')
            if -self._num_cols > colindex >= self._num_cols:
                raise IndexError('Column index out of range.')

    def __str__(self):
        '''
        重写 __str__ 魔法方法，使打印本类实例时以表格形式输出，而不是对象内存地址。
        :return: str，已构建完成的整个表格的字符串形式
        '''
        return self.getText()

    # 将 __repr__ 魔法方法指向 __str__ 方法，输出时用 __str__ 代理。
    __repr__ = __str__

    def addColumn(self, colindex, column=None):
        '''
        Table 实例对象的插入列方法。
            1.要插入的列的行数比现有行数多则截断，比现有行数少则用空字符补足；
            2.可不带索引参数 colindex，默认把列插入到所有列末尾。
        :param colindex: int, 插入位置索引
        :param column: Iterable, 要插入的列
        '''
        # 如果要插入的列 column 值是 None (column 参数默认值是 None)，
        # 则说明 addColumn 方法只接收到一个参数 colindex，而我们规定接收到的参数
        # 默认是要插入的列，所以要交换一下参数值，colindex 值给 column，column 的值赋值
        # 为 self._num_cols，按 self._num_cols 值插入就是最后一列
        if column is None:
            column, colindex = colindex, self._num_cols
        # 再检查参数类型是否符号要求，不符合则抛出异常
        if not isinstance(colindex, int):
            raise TypeError(
                'Integer parameter <colindex> expected, got %s.'
                % type(colindex).__name__
            )
        if not isinstance(column, Iterable):
            raise TypeError(
                'Iterable parameter <column> expected, got %s.' % type(column).__name__
            )
        if self._num_cols + 1 > MAX_COLUMN_NUM:
            raise ValueError(
                'The number of columns exceeds the limit(%d), '
                'please modify the value of MAX_COLUMN_NUM if necessary.'
                % MAX_COLUMN_NUM
            )
        # 如果 column 是生成器、迭代器，要转换为列表好进行索引操作
        column = list(column)
        # 枚举本类实例(self)里的行
        for row_ind, row_obj in enumerate(self):
            try:
                # 要被插入到本行的元素 obj_to_be_added，从 column
                # 抓取对应元素 column[row_ind]
                obj_to_be_added = column[row_ind]
            # 如果索引错误(超出范围)，则说明 column 元素不够多，不能一一对应所有的行
            except IndexError:
                # 则把要插入的元素指定为 self._filler(默认填充对象)
                obj_to_be_added = self._filler
            except Exception:
                # 其他未知异常
                raise Exception('Unexpected exception.')
            # 调用行 _RowObj 类实例的 _addcol 方法插入单元格
            # 因为这里仅针对一行所以不说插入列了
            row_obj._addcol(colindex, obj_to_be_added)
        # 列计数加 1
        self._num_cols += 1
        # 固定列宽列表相应列位置也要插入列宽值，插入的值使用默认列宽 self._col_fixed
        self._col_fixeds.insert(colindex, self._col_fixed)
        # 调用本类的 _find_cap、_find_floor 方法分别找出所有行相应列的列宽上限下限值
        # 并在上限、下限值列表相应插入值
        self._col_caps.insert(colindex, self._find_cap(colindex))
        self._col_floors.insert(colindex, self._find_floor(colindex))

    def addRow(self, rowindex, row=None):
        '''
        Table 实例的插入行方法。
            1.要插入的行的列数比现有列数多则截断，比现有列数少则用 filler 补足；
            2.可不带索引参数 rowindex，默认把行插入到所有行末尾。
        :param rowindex: int, 插入位置索引
        :param row: Iterable, 要插入的行
        '''
        # 同插入列方法 addColumn
        if row is None:
            row, rowindex = rowindex, self._num_rows
        if not isinstance(rowindex, int):
            raise TypeError(
                'Integer parameter <rowindex> expected, got %s.'
                % type(rowindex).__name__
            )
        if not isinstance(row, Iterable):
            raise TypeError(
                'Iterable parameter <row> expected, got %s.' % type(row).__name__
            )
        # 如果row是生成器、迭代器，要转换为列表好进行索引操作
        row_list = list(row)
        len_row = len(row_list)
        # 要添加的行的元素数量比现有表格列数多，则截断要添加的行使其长度与现有表格列数一致
        if len_row > self._num_cols:
            row_list = row_list[: self._num_cols]
        # 如果要添加的行的元素数量比现有表格的列数少，则用 fill 扩充要添加的行列表
        elif len_row < self._num_cols:
            row_list.extend([self._filler] * (self._num_cols - len_row))
        # 以要添加的行列表等为初始参数，实例化行类 _RowObj
        row_list = _RowObj(
            row_list,
            self._col_wids,
            self._row_fixed,
            self._alignh,
            self._alignv,
            self._fbgcolors,
        )
        # 将行类 _RowObj 实例添加进现有表格实例(self)相应位置
        self.insert(rowindex, row_list)
        # 行数计数加 1
        self._num_rows += 1
        # 分别调用行 _RowObj 实例 _find_cap、_find_floor 方法
        # 重新查找每列的字符宽度上限、下限，并分别更新列宽度上、下限列表
        for colind in range(self._num_cols):
            self._col_caps[colind] = self._find_cap(colind)
            self._col_floors[colind] = self._find_floor(colind)

    def getColumn(self, colindex=-1):
        '''
        获取列源数据方法。
        :param colindex: int，要获取的列的索引
        :return: list[any...]，要获取的列的列表形式
        '''
        self._check_index(colindex=colindex)
        if colindex is None:
            return
        return [row[colindex] for row in self]

    def getRow(self, rowindex=-1):
        '''
        获取行元数据方法。
        :param rowindex: int，要获取的行的索引
        :return: list[any...]，要获取的行的列表形式
        '''
        self._check_index(rowindex)
        if rowindex is None:
            return
        return list(self[rowindex])

    def getItem(self, rowindex=-1, colindex=-1):
        '''
        获取单元格源数据方法。
        :param rowindex: int，单元格行索引
        :param colindex: int，单元格列索引
        :return: any，获取的单元个源数据
        '''
        self._check_index(rowindex, colindex)
        if rowindex is None or colindex is None:
            return
        return self[rowindex][colindex]

    def getString(self, rowindex=-1, colindex=-1):
        '''
        获取单元格源数据的字符串形式。
        :param rowindex: int，单元格行索引
        :param colindex: int，单元格列索引
        :return: str，获取的单元个源数据的字符串形式
        '''
        self._check_index(rowindex, colindex)
        if rowindex is None or colindex is None:
            return
        return str(self[rowindex][colindex])

    def writeCell(self, rowindex=None, colindex=None, *, value):
        '''
        覆写单元格方法。
        :param rowindex: int，单元格行索引
        :param colindex: int，单元格列索引
        :param value: any，要写入的值，可以是任何受支持的类型
        :return: None
        '''
        self._check_index(rowindex, colindex)
        # 如果行索引和列索引都为 None 则覆写所有单元格
        if rowindex is None and colindex is None:
            for row in self:
                for colind in range(self._num_cols):
                    row[colind] = value
                    self._col_caps[colind] = self._find_cap(colind)
                    self._col_floors[colind] = self._find_floor(colind)
        # 如果行索引、列索引其中之一为 None，则覆写整列或整行
        elif rowindex is None or colindex is None:
            if rowindex is None:
                for row in self:
                    row[colindex] = value
                self._col_caps[colindex] = self._find_cap(colindex)
                self._col_floors[colindex] = self._find_floor(colindex)
            else:
                for colind in range(self._num_cols):
                    self[rowindex][colind] = value
                    self._col_caps[colind] = self._find_cap(colind)
                    self._col_floors[colind] = self._find_floor(colind)
        # 都不为 None 则只覆写指定坐标的单元格
        else:
            self[rowindex][colindex] = value
            self._col_caps[colindex] = self._find_cap(colindex)
            self._col_floors[colindex] = self._find_floor(colindex)

    def clearCell(self, rowindex=None, colindex=None):
        '''
        清除单元格内容方法。
        :param rowindex: int，单元格行索引
        :param colindex: int，单元格列索引
        :return: None
        '''
        # 用 writeCell 方法代理，写入空字符串
        self.writeCell(rowindex, colindex, value='')

    def isEmpty(self, rowindex=None, colindex=None):
        '''
        测试表格内容是否为空方法。
            1.行索引 rowindex 和列索引 colindex 都不为 None，则测试对应的单元格；
            2.行索引 rowindex 为 None，列索引 colindex 不为 None，则测试第 colindex 列整列，反之亦然；
            3.行索引 rowindex 和列索引 colindex 都为 None，则测试整个表格的所有单元格。
        :param rowindex: int，单元格行索引
        :param colindex: int，单元格列索引
        :return: bool
        '''
        self._check_index(rowindex, colindex)
        # 如果行和列索引都为 None，则测试整个表格
        if rowindex is None and colindex is None:
            return not any(
                any(bool(row[colind]) for colind in range(len(row))) for row in self
            )
        # 行和列索引其中之一为 None，则测试证列或整行
        elif rowindex is None or colindex is None:
            if rowindex is None:
                return not any(bool(row[colindex]) for row in self)
            else:
                return not any(self[rowindex])
        # 都不为 None 则测试对应单元格
        else:
            return not bool(self[rowindex][colindex])

    def isFull(self, rowindex=None, colindex=None):
        '''
        测试表格内容是否全部非空方法。
        索引参数使用方法与 isEmpty 方法相同。
        '''
        self._check_index(rowindex, colindex)
        if rowindex is None and colindex is None:
            return all(
                all(bool(row[colind]) for colind in range(len(row))) for row in self
            )
        elif rowindex is None or colindex is None:
            if rowindex is None:
                return all(bool(row[colindex]) for row in self)
            else:
                return all(self[rowindex])
        else:
            return bool(self[rowindex][colindex])

    def delColumn(self, colindex):
        '''
        Table 类实例对象的删除列方法。
            1.根据列的索引值 colindex 删除对应的列；
            2.将所删除的列以一维列表形式返回。
        :param colindex: int, 要删除的列的索引值
        :return: list, 以列表形式返回已删除的列
        '''
        # 检查输入参数类型等是否符号要求
        if not isinstance(colindex, int):
            raise TypeError(
                'Integer parameter <colindex> expected, got %s.'
                % type(colindex).__name__
            )
        if -self._num_cols > colindex >= self._num_cols:
            raise IndexError('Column index out of range.')
        # 列计数 -1
        self._num_cols -= 1
        # 相应的列固定宽度列表、列宽上限列表、列宽下限列表也要删除相应列宽度数据
        del self._col_fixeds[colindex]
        del self._col_caps[colindex]
        del self._col_floors[colindex]
        # 列表推导式中调用 _RowObj 类(行)实例的 _delcol 方法并将新列表(删除的列)返回
        return [row._delcol(colindex) for row in self]

    def delRow(self, rowindex):
        '''
        Table 类实例对象的删除行方法。
            1.根据列的索引值 rowindex 删除对应的行；
            2.将所删除的行以一维列表形式返回。
        :param rowindex: int, 要删除的行的索引值。
        :return: list, 以列表形式返回已删除的行。
        '''
        # 检查输入参数类型等是否符号要求
        if not isinstance(rowindex, int):
            raise TypeError(
                'Integer parameter <rowindex> expected, got %s.'
                % type(rowindex).__name__
            )
        if -self._num_rows > rowindex >= self._num_rows:
            raise IndexError('Row index out of range.')
        # 调用 Table 实例(列表)的 pop 方法删除指定行，得到被删除行的返回值
        rowlist = list(self.pop(rowindex))
        # 行计数 -1
        self._num_rows -= 1
        # 调用 Table 实例的 _find_cap、_find_floor 方法更新所有列的宽度上、下限数据
        for colindex in range(self._num_cols):
            self._col_caps[colindex] = self._find_cap(colindex)
            self._col_floors[colindex] = self._find_floor(colindex)
        return rowlist

    def setColumnWidth(self, colindex, width=None):
        '''
        Table 类实例对象的设置列的固定列宽方法。
            1.不带列索引参数 colindex，则设置所有列的宽度；
            2.不需要固定列宽则将列宽设置为 0 即可自适应列宽。
        :param colindex: int, 要设置宽度的列索引
        :param width: int, 要设置的列宽度
        :return: None
        '''
        # 如果 width 参数值为 None，可能只传进一个参数 colindex
        # 因为规定可以不带 colindex 参数，传进的一个参数默认为 width，所以需要将 colindex 的
        # 值交换给 width，colindex 赋值为 None
        if width is None:
            width, colindex = colindex, None
        # 检查参数类型等是否符合要求
        if not (isinstance(colindex, int) or colindex is None):
            raise TypeError(
                'Integer parameter <colindex> or "None" expected, got %s.'
                % type(colindex).__name__
            )
        if colindex is not None:
            if not (-self._num_cols <= colindex < self._num_cols):
                raise IndexError('Column index out of range.')
        if not isinstance(width, int):
            raise TypeError(
                'Integer parameter <width> expected, got %s.' % type(width).__name__
            )
        if width > MAX_COLUMN_WIDTH:
            raise ValueError(
                'The column width to be set exceeds the limit(%d), '
                'please modify the value of "MAX_COLUMN_WIDTH" if necessary.'
                % MAX_COLUMN_WIDTH
            )
        # 如果 colindex 为 None，则以 width 为列宽值重新生成一个固定列宽列表
        if colindex is None:
            self._col_fixeds = [width for _ in self._col_fixeds]
            return
        # 不为 None 则修改固定列宽列表中指定列的列宽值
        self._col_fixeds[colindex] = width

    def setRowHeight(self, rowindex, height=None):
        '''
        Table 类实例对象的设置固定行高方法。
            1.不带行索引参数 rowindex，则设置所有行的高度；
            2.不需要固定行高则将行高设置为 0 即可自适应行高。
        :param rowindex: int, 要设置高度的行索引。
        :param height: int, 要设置的行高度。
        :return: None: 无返回值。
        '''
        # 同 setColumnWidth 方法，不再重复注释了
        if height is None:
            height, rowindex = rowindex, None
        if not (isinstance(rowindex, int) or rowindex is None):
            raise TypeError(
                'Integer parameter <rowindex> or "None" expected, got %s.'
                % type(rowindex).__name__
            )
        if rowindex is not None:
            if -self._num_rows > rowindex >= self._num_rows:
                raise IndexError('Row index out of range.')
        if not isinstance(height, int):
            raise TypeError(
                'Integer parameter <height> expected, got %s.' % type(height).__name__
            )
        if height > MAX_ROW_HEIGHT:
            raise ValueError(
                'The row height to be set exceeds the limit(%d), '
                'please modify the value of "MAX_ROW_HEIGHT" if necessary.'
                % MAX_ROW_HEIGHT
            )
        if rowindex is None:
            # 调用 _RowObj （行）实例的 _height 方法设置行高
            # 因为行高属性是 _RowObj 实例属性
            # （这点做的不好，列宽是 Table 实例属性，行高是 _RowObj 实例属性，不统一）
            for row in self:
                row._height(height)
            return
        self[rowindex]._height(height)

    def setAlignment(self, rowindex=None, colindex=None, *, alignh=None, alignv=None):
        '''
        Table 类实例的设置对齐方式方法。
            1.行索引 rowindex 和列索引 colindex 参数可以自由省略或写 None；
            2.行索引 rowindex 为 None，列索引 colindex 不为 None，则表示整列，反之亦然；
            3.水平对齐方式 alignh 和垂直对齐方式 alignv 可自由省略，省略或为 None 则表示不
            设置该对齐方式；
            4.如需设置对齐方式，则对齐方式 alignh 或 alignv 需以关键字参数形式调用。
            5.alignh 和 alignv 的可用值分别为 'l','left','c','center','r','right'
            和 't','top','m','middle','b','bottom'。
        :param rowindex: int，行索引
        :param colindex: int，列索引
        :param alignh: str，水平对齐方式
        :param alignv: str，垂直对齐方式
        :return: None
        '''
        # 检查参数是否符合要求，不符合则抛出异常
        if not (isinstance(rowindex, int) or rowindex is None):
            raise TypeError(
                'Integer parameter <rowindex> or "None" expected, got %s.'
                % type(rowindex).__name__
            )
        if not (isinstance(colindex, int) or colindex is None):
            raise TypeError(
                'Integer parameter <colindex> or "None" expected, got %s.'
                % type(colindex).__name__
            )
        if alignh not in __ALIGNH__.split() and alignh is not None:
            raise ValueError(
                'No horizontal alignment option like <%s>, available: %s.'
                % (alignh, __ALIGNH__)
            )
        if alignv not in __ALIGNV__.split() and alignv is not None:
            raise ValueError(
                'No vertical alignment option like <%s>, available: %s.'
                % (alignv, __ALIGNV__)
            )
        # 如果行和列索引都为 None，则设置整个表格所有单元格的对齐方式
        if rowindex is not None and colindex is not None:
            # 行或列索引超出范围则抛出异常，以下同理
            if -self._num_rows > rowindex >= self._num_rows:
                raise IndexError('Row index out of range.')
            if -self._num_cols > colindex >= self._num_cols:
                raise IndexError('Column index out of range.')
            # 调用 _RowObj（行）实例的 _align 方法设置对齐方式，以下同理
            self[rowindex]._align(colindex, alignh, alignv)
        elif rowindex is None and colindex is None:
            for rowind in range(self._num_rows):
                for colind in range(self._num_cols):
                    self[rowind]._align(colind, alignh, alignv)
        elif rowindex is None or colindex is None:
            if rowindex is not None:
                if -self._num_rows > rowindex >= self._num_rows:
                    raise IndexError('Row index out of range.')
                for colind in range(self._num_cols):
                    self[rowindex]._align(colind, alignh, alignv)
            elif colindex is not None:
                if -self._num_cols > colindex >= self._num_cols:
                    raise IndexError('Column index out of range.')
                for row in self:
                    row._align(colindex, alignh, alignv)

    def setColor(self, rowindex=None, colindex=None, *, clrs=None):
        '''
        Table 类实例的设置颜色方法。
            1.设置颜色前会清空单元格原颜色集合；
            2.颜色代码(字符串)的可用值见 README.md 中的颜色代码表格。
        :param rowindex:  int，行索引
        :param colindex:  int，列索引
        :param clrs: list|tuple|set[str...]，颜色代码(字符串)集合
        :return: None
        '''
        if not (isinstance(rowindex, int) or rowindex is None):
            raise TypeError(
                'Integer parameter <rowindex> or "None" expected, got %s.'
                % type(rowindex).__name__
            )
        if not (isinstance(colindex, int) or colindex is None):
            raise TypeError(
                'Integer parameter <colindex> or "None" expected, got %s.'
                % type(colindex).__name__
            )
        if not isinstance(clrs, (tuple, list, set)) and clrs is not None:
            raise TypeError(
                'Type of parameter <clrs> should be "tuple"、"list" or "set".'
            )
        if clrs is not None and (not all(isinstance(s, str) for s in clrs)):
            raise ValueError(
                'The type of the color name in the collection can only be "str".'
            )
        # 调用 _RowObj 实例的 _setclr 方法设置单元格颜色
        if rowindex is not None and colindex is not None:
            if -self._num_rows > rowindex >= self._num_rows:
                raise IndexError('Row index out of range.')
            if -self._num_cols > colindex >= self._num_cols:
                raise IndexError('Column index out of range.')
            self[rowindex]._setclr(colindex, clrs)
        elif rowindex is None and colindex is None:
            for rowind in range(self._num_rows):
                for colind in range(self._num_cols):
                    self[rowind]._setclr(colind, clrs)
        elif rowindex is None or colindex is None:
            if rowindex is not None:
                if -self._num_rows > rowindex >= self._num_rows:
                    raise IndexError('Row index out of range.')
                for colind in range(self._num_cols):
                    self[rowindex]._setclr(colind, clrs)
            elif colindex is not None:
                if -self._num_cols > colindex >= self._num_cols:
                    raise IndexError('Column index out of range.')
                for row in self:
                    row._setclr(colindex, clrs)

    def getColor(self, rowindex, colindex):
        '''
        Table 类实例的获取单元格颜色集合方法。
        该方法会返回单元格的颜色代码（字符串）集合，当不想用 setColor 方法（会先清空指定单元格
        的所有颜色设置，再设置指定颜色）时，可以调用 getColor 方法取得单元格的颜色集合，再用集
        合方法对该集合内元素（颜色代码）进行增删操作，即可修改该单元格的前背景色。
        当然，该方法不限于以上用法。
        :param rowindex:  int，列索引
        :param colindex:  int，列索引
        :return: set[str...]，指定单元格的颜色集合
        '''
        self._check_index(rowindex, colindex)
        # 调用 _RowObj（行）实例的 _getclr 方法获取单元格颜色集合
        return self[rowindex]._getclr(colindex)

    def defaultClr(self, *values):
        '''
        Table 类实例的设置默认前背景色方法。
        本方法与创建 Table 类实例时的初始化参数 fbgc 修改的是同一个属性值。
        当单元格未设置前背景色时，将使用本方法设置的前背景色。
        :param values: str，接受不定长参数，参数应为可用的颜色代码（字符串）
        :return: None
        '''
        # 检查参数值是否符合要求
        if not all(isinstance(s, str) for s in values):
            raise TypeError(
                'The type of the color name in the collection can only be "str".'
            )
        # 检查 values 所有值是否符合要求
        # （是否能取到 _color 属性，即 colors 模块中的 _ColorGroup 类实例）
        for string in values:
            getattr(_colors, string)
        self._fbgcolors = set(values)

    def defaultAlign(self, *, alignh=None, alignv=None):
        '''
        Table 类实例的设置默认对齐方式（水平和垂直）方法。
        本方法与创建 Table 类实例时的初始化参数 alignh、alignv 修改的分别是同一个属性值。
        当单元格未设置水平、垂直对齐方式时，将使用本方法设置的对齐方式。
        :param alignh: str，可用的对齐方式字符串（'l','left','c','center','r','right'）
        :param alignv: str，可用的对齐方式字符串（'t','top','m','middle','b','bottom'）
        :return: None
        '''
        if alignh not in __ALIGNH__.split() and alignh is not None:
            raise ValueError(
                'No horizontal alignment option like <%s>, available: %s.'
                % (alignh, __ALIGNH__)
            )
        if alignv not in __ALIGNV__.split() and alignv is not None:
            raise ValueError(
                'No vertical alignment option like <%s>, available: %s.'
                % (alignv, __ALIGNV__)
            )
        # 如果 alignh、alignv 不为 None，则将 _RowObj 类实例的 _alignh、_alignv 属
        # 性值分别设置为 alignh、alignv
        if alignh:
            self._alignh = alignh
        if alignv:
            self._alignv = alignv

    def setStyle(self, style):
        '''
        Table 类实例的设置表格边框线风格方法。
        :param style: Style，Style 类实例
        :return: None
        '''
        if not isinstance(style, Style):
            raise TypeError('Parameter <style> should be an instance of class "Style".')
        self._style = style

    def defaultFill(self, fill=''):
        '''
        Table 类实例的设置默认填充对象方法。
        本方法与创建 Table 类实例时的初始化参数 fill 修改的是同一个属性值。
        :param fill: any，通过 addColumn、addRow 方法添加行列时，要添加的行、列不够
        现有表格行、列长时，使用 fill 填充。
        :return: None
        '''
        self._filler = fill

    @staticmethod
    def limit(item, value):
        '''
        Table 类实例的限制最大列数、列宽、行高方法。
        :param item: str，可用值：'MAX_COLUMN_NUM'、'MAX_COLUMN_WIDTH'、
        'MAX_ROW_HEIGHT'。
        :param value: int，可用值：1~300。
        :return: None
        '''
        if not isinstance(item, str):
            raise TypeError('The attribute "item" should be "str".')
        if not isinstance(value, int):
            raise TypeError('The limit value should be "int".')
        if value not in range(1, 301):
            raise ValueError('The limit value should be in range of 1 to 300.')
        if item in ('MAX_COLUMN_NUM', 'MAX_COLUMN_WIDTH', 'MAX_ROW_HEIGHT'):
            globals()[item] = value

    def show(
        self,
        start=0,
        stop=None,
        *,
        colorful=True,
        header=True,
        file=sys.stdout,
    ):
        '''
        Table 类实例的输出表格方法。
        :param start: int，要输出的起始行（不包括标题行），默认 0
        :param stop: int，要输出的结束行（不包括标题行），默认 None（末尾）
        :param colorful: bool，是否输出彩色表格，默认 True。当你不想输出彩色表格时，
        或者你的终端不支持彩色输出时，又或者你要输出到文件（file参数设定为文件对象）
        但不想携带那些杂乱的颜色代码时，这个参数会对你十分有用，你可将它设定为 False，
        这时输出的表格将不携带任何颜色控制代码（如果你之前已有设置好的颜色，它不会被清
        除，下次你仍可以将 colorful 参数设置为 True，以输出你之前设定好的彩色表格）
        :param header: bool，是否输出标题行（严格来说是第一行），默认 True
        :param file: TextIOWrapper，Python 文件对象（既可以是标准输出流，也可以是 
        open 函数返回的 Python 文件对象等）
        :return: None
        '''
        if not isinstance(start, int):
            raise TypeError('Type of parameter <start> should be "int".')
        if not isinstance(stop, int) and stop is not None:
            raise TypeError('Type of parameter <stop> should be "int" or "None".')
        if not isinstance(file, (TextIOWrapper, StdOutputFile, StreamWrapper)):
            raise TypeError('Type of <file> is not Python file object.')
        # 声名全局变量
        global _COLORFUL
        # 如果参数 colorful 为 False 则将 全局变量 _COLORFUL 设置为 False
        # （函数 _format_o 会根据 _COLORFUL 是否为 True 来决定是否给表格文本添加颜色
        # 控制代码）
        if not colorful:
            _COLORFUL = False
        # 如果程序非运行于 win 平台或运行于 IDLE 上，则调用整体一次输出方法 _out_overall
        # 来输出，原因：
        # 1. win 平台上用 colorama 模块来在终端上输出彩色表格，如果将表格所有项串成一
        # 个大字符串再一次输出（用 _out_overall 方法输出）的话，颜色会混乱（可能 colorama
        # 模块有更好的使用方法来避免这些问题，但作者未作深入研究），所以需要逐项输出（用
        # _out_itemized 方法输出）；
        # 2. 如果运行于 IDLE 上，因 IDLE 不接受前景色背景色代码控制，所以 colors 模块
        # 会反回空字符串代替颜色控制代码，所以不管是否运行于 win 平台上，都没有颜色混乱
        # 的烦恼，所以直接调用整体一次输出方法 _out_overall 来输出就行。
        if not _NT or run_on_idle:
            self._out_overall(start, stop, header, file)
        else:
            self._out_itemized(start, stop, header, file)
        # 将 _COLORFUL 标志还原为 True，否则下次输出就没有颜色了
        _COLORFUL = True
        # 如果 file 是标准输出流 sys.stdout，则不用关闭文件，直接返回
        # 当然如果用户在外部将 sys.stdout 赋值为 Python file object，那关闭文件操作
        # 也是用户应尽的义务
        if file is sys.stdout:
            return
        # 尝试关闭文件，关闭失败不作处理，直接返回
        try:
            file.close()
        except Exception:
            pass

    def _out_overall(self, start, stop, header, file):
        text = self.getText(start, stop, header)
        try:
            file.write(text)
            file.write(_LNSEP)
            file.flush()
        except Exception:
            raise IOError('Failed to write to file or print on terminal.')

    def _out_itemized(self, start, stop, header, file):
        self.refactorText()
        hat = self._border['hat']
        neck = self._border['neck']
        belt = self._border['belt']
        shoes = self._border['shoes']
        pad = self._style.cell_pad
        file.write(hat + _LNSEP)
        if header:
            headerform = self[0]._form(pad)
            for line in headerform:
                len_line = len(line)
                file.write(self._style.left_vert)
                for ind, string in enumerate(line):
                    file.write(string)
                    if ind != len_line - 1:
                        file.write(self._style.center_vert)
                file.write(self._style.right_vert + _LNSEP)
            file.write(neck + _LNSEP)
        body = self[1:][start:stop]
        len_body = len(body)
        for index, bodyrow in enumerate(body):
            rowform = bodyrow._form(pad)
            for line in rowform:
                file.write(self._style.left_vert)
                len_line = len(line)
                for ind, string in enumerate(line):
                    file.write(string)
                    if ind != len_line - 1:
                        file.write(self._style.center_vert)
                file.write(self._style.right_vert + _LNSEP)
            if (index != len_body - 1) and belt:
                file.write(belt + _LNSEP)
        file.write(shoes + _LNSEP)

    def refactorText(self):
        self._col_wids_refresh()
        widths = [wid + _str_wid(self._style.cell_pad) * 2 for wid in self._col_wids]
        hat = ''.join(
            (
                self._style.top_left,
                self._style.top_cross.join(
                    [self._style.top_horz * wid for wid in widths]
                ),
                self._style.top_right,
            )
        )
        neck = ''.join(
            (
                self._style.split_left,
                self._style.split_cross.join(
                    [self._style.split_horz * wid for wid in widths]
                ),
                self._style.split_right,
            )
        )
        belt = ''.join(
            (
                self._style.left_cross,
                self._style.center_cross.join(
                    [self._style.center_horz * wid for wid in widths]
                ),
                self._style.right_cross,
            )
        )
        shoes = ''.join(
            (
                self._style.bottom_left,
                self._style.bottom_cross.join(
                    [self._style.bottom_horz * wid for wid in widths]
                ),
                self._style.bottom_right,
            )
        )
        self._border['hat'] = hat
        self._border['neck'] = neck
        self._border['belt'] = belt
        self._border['shoes'] = shoes
        self.rowTexts.clear()
        for row_obj in self:
            self.rowTexts.append(
                row_obj._gettext(
                    self._style.left_vert,
                    self._style.center_vert,
                    self._style.right_vert,
                    self._style.cell_pad,
                )
            )

    def getText(self, start=0, stop=None, header=True):
        self.refactorText()
        hat = self._border['hat']
        neck = self._border['neck']
        belt = self._border['belt']
        shoes = self._border['shoes']
        if belt:
            belt = ''.join((_LNSEP, belt, _LNSEP))
        else:
            belt = _LNSEP
        body = belt.join(self.rowTexts[1:][start:stop])
        if not header:
            group = (hat, body, shoes)
        else:
            group = (hat, self.rowTexts[0], neck, body, shoes)
        return _LNSEP.join(group)

    def _col_wids_refresh(self):
        self._col_wids.clear()
        final_width = 1
        for ind, width in enumerate(self._col_floors):
            if self._col_fixeds[ind] != 0 and self._col_fixeds[ind] < width:
                final_width = width
            elif self._col_fixeds[ind] == 0:
                final_width = self._col_caps[ind]
            else:
                final_width = self._col_fixeds[ind]
            self._col_wids.append(final_width)

    def _find_cap(self, colindex):
        '''
        查找指定列的最大宽度值并返回该值。
        :param colindex: 指定列的索引值。
        :return: int: 该列的最大宽度值。
        '''
        return max(row._colcap(colindex) for row in self)

    def _find_floor(self, colindex):
        '''
        查找指定列的宽度下限并返回该值。
        :param colindex: 指定列的索引值。
        :return: int: 该列的宽度下限。
        '''
        return max(row._colflr(colindex) for row in self)


def _items_to_str(iterable, num=None):
    '''将可迭代对象里的元素转换成str并返回包含这些元素的列表。'''
    it = isinstance(iterable, Iterator)
    gt = isinstance(iterable, Generator)
    if (num is None) or not (it or gt):
        return [str(i) for i in iterable]
    strings = list()
    for _ in range(num):
        try:
            strings.append(str(next(iterable)))
        except StopIteration:
            break
    return strings


def _chr_wid(char):
    '''
    根据字符char的unicode码判断该字符的宽度并返回宽度值。
    :param char: str，给定的字符。
    :return: int，字符的宽度（判断并不十分准确，可能有错）。
    '''
    code = ord(char)
    # 英文字母、符号：0021-007E
    if 0x0021 <= code <= 0x007E:
        return 1
    # 韩文字母：1100-11FF
    if 0x1100 <= code <= 0x11FF:
        return 2
    # 盲文符号：2800-28FF
    if 0x2800 <= code <= 0x28FF:
        return 1
    # CJK部首补充：2E80-2EFF
    # 康熙部首：2F00-2FDF
    if 0x2E80 <= code <= 0x2FDF:
        return 2
    # 注音符号：3100-312F
    # 日文片假名：30A0-30FF
    # 日文平假名：3040-309F
    # CJK标点符号：3000-303F
    # 汉字结构描述符：2FF0-2FFF
    if 0x2FF0 <= code <= 0x312F:
        return 2
    # 韩文兼容字母：3130-318F
    if 0x3130 <= code <= 0x318F:
        return 2
    # CJK笔划：31C0-31EF
    # 日文片假名拼音扩展：31F0-31FF
    if 0x31C0 <= code <= 0x31FF:
        return 2
    # CJK字母及月份：3200-32FF
    if 0x3200 <= code <= 0x3247:
        return 2
    if 0x3248 <= code <= 0x324F:
        return 1
    if 0x3250 <= code <= 0x32FF:
        return 2
    # CJK特殊符号：3300-33FF
    if 0x3300 <= code <= 0x33FF:
        return 2
    # 扩展A	6582字	3400-4DB5
    if 0x3400 <= code <= 0x4DB5:
        return 2
    if 0x4DC0 <= code <= 0x4DFF:
        return 2
    # 基本CJK文字
    if 0x4E00 <= code <= 0x9FFF:
        return 2
    # 彝文音节：A000-A48F
    if 0xA000 <= code <= 0xA48F:
        return 2
    # 彝文部首：A490-A4CF
    if 0xA490 <= code <= 0xA4CF:
        return 2
    # 韩文拼音：AC00-D7AF
    if 0xAC00 <= code <= 0xD7AF:
        return 2
    # 兼容汉字	477字	F900-FAFF
    if 0xF900 <= code <= 0xFAFF:
        return 2
    # 全角ASCII、全角中英文标点
    # 半宽片假名、半宽平假名、半宽韩文字母：FF00-FFEF
    if 0xFF00 <= code <= 0xFF60:
        return 2
    if 0xFF61 <= code <= 0xFFDF:
        return 1
    if 0xFFE0 <= code <= 0xFFE6:
        return 2
    if 0xFFE7 <= code <= 0xFFEF:
        return 1
    # 太玄经符号：1D300-1D35F
    if 0x1D300 <= code <= 0x1D35F:
        return 2
    # 扩展B	42711字	20000-2A6D6
    if 0x20000 <= code <= 0x2A6D6:
        return 2
    # 扩展C	4149字	2A700-2B734
    if 0x2A700 <= code <= 0x2B734:
        return 2
    # 扩展D	222字	2B740-2B81D
    if 0x2B740 <= code <= 0x2B81D:
        return 2
    # 扩展E	5762字	2B820-2CEA1
    if 0x2B820 <= code <= 0x2CEA1:
        return 2
    # 扩展F	7473字	2CEB0-2EBE0
    if 0x2CEB0 <= code <= 0x2EBE0:
        return 2
    # 兼容汉字扩展	542字	2F800-2FA1D
    if 0x2F800 <= code <= 0x2FA1D:
        return 2
    # 扩展G	4939字	30000-3134A
    if 0x30000 <= code <= 0x3134A:
        return 2
    # 控制字符
    if code in (0x0000, 0x0008, 0x0009, 0x000B, 0x000D, 0x001F, 0x007F):
        return 0
    # 猜测其他 Unicode 字符宽度为 1
    return 1


def _str_wid(string):
    '''
    以半角英文字符为一个单位宽度，返回字符串的总宽度。
    如果中间有换行符，则计算换行符间的字符串宽度，返回它们之中最大的宽度。
    '''
    strings_max_width, sub_str_width = 0, 0
    for c in string:
        if c in (_LNSEP, '\n'):
            if sub_str_width > strings_max_width:
                strings_max_width = sub_str_width
            sub_str_width = 0
            continue
        sub_str_width += _chr_wid(c)
    if sub_str_width > strings_max_width:
        strings_max_width = sub_str_width
    return strings_max_width


def _max_char_wid(string):
    '''返回字符串string中宽度最大的单个字符的宽度值。'''
    if not string:
        return 1  # 列宽度下限不能为0，限制下限为1。
    return max(_chr_wid(char) for char in string)


def _format(rowfromsrc, rowhit, colwids, alignhs, alignvs, fbgcs, padding):
    row_from_src = _items_to_str(rowfromsrc)
    for ind, string in enumerate(row_from_src):
        for escc in __EXCLUDED__:
            string = string.replace(escc, '')
        row_from_src[ind] = string
    row_with_cells = list()
    for ind, string in enumerate(row_from_src):
        if alignvs[ind].lower() in ('b', 'bottom'):
            split = _rsplit
        else:
            split = _lsplit
        row_with_cells.append(split(string, colwids[ind]))
    if rowhit == 0:
        rowhit = max(len(lst) for lst in row_with_cells)
    for ind, stringlist in enumerate(row_with_cells):
        _format_v(stringlist, rowhit, alignvs[ind])
        _format_h(stringlist, colwids[ind], alignhs[ind])
        _format_o(stringlist, fbgcs[ind], padding)
    return row_with_cells


def _format_v(stringlist, rowhit, alignv):
    if len(stringlist) < rowhit:
        line_in_cell_empty = ''
        if alignv.lower() in ('b', 'bottom'):
            for _ in range(rowhit - len(stringlist)):
                stringlist.insert(0, line_in_cell_empty)
        elif alignv.lower() in ('m', 'middle'):
            total_num = rowhit - len(stringlist)
            top_num = total_num // 2
            bottom_num = total_num - top_num
            for _ in range(top_num):
                stringlist.insert(0, line_in_cell_empty)
            for _ in range(bottom_num):
                stringlist.append(line_in_cell_empty)
        elif alignv.lower() in ('t', 'top'):
            for _ in range(rowhit - len(stringlist)):
                stringlist.append(line_in_cell_empty)
        else:
            raise ValueError(
                'No vertical alignment option like <%s>, available: %s.'
                % (alignv, __ALIGNV__)
            )
    elif len(stringlist) > rowhit:
        del stringlist[rowhit:]


def _format_h(stringlist, colwid, alignh):
    def fmt(string, width, alignh):
        pad_wid = width - _str_wid(string)
        if alignh.lower() in ('l', 'left'):
            return '%s%s' % (string, pad_wid * ' ')
        elif alignh.lower() in ('c', 'center'):
            left_wid = pad_wid // 2
            right_wid = pad_wid - left_wid
            return '%s%s%s' % (left_wid * ' ', string, right_wid * ' ')
        elif alignh.lower() in ('r', 'right'):
            return '%s%s' % (pad_wid * ' ', string)
        else:
            raise ValueError(
                'No horizontal alignment option like <%s>, available: %s.'
                % (alignh, __ALIGNH__)
            )

    for ind, string in enumerate(stringlist):
        stringlist[ind] = fmt(string, colwid, alignh)


def _format_o(stringlist, fbgc, padding):
    mixed_color = ''
    if _COLORFUL:
        for color in fbgc:
            mixed_color += getattr(_colors, color)
    for index, string in enumerate(stringlist):
        stringlist[index] = mixed_color + ''.join((padding, string, padding))


def _lsplit(string, width):
    if not isinstance(string, str):
        raise TypeError('Type of value of parameter <string> should be "str".')
    if width < _max_char_wid(string):
        raise ValueError(
            'The character in the string has a width larger than '
            'the target width, which cannot be cut to the target width.'
        )
    if not string:
        return [string]
    start, stop, lenstr, substrings = 0, 1, len(string), list()
    while stop <= lenstr:
        strwid = _str_wid(string[start:stop])
        if strwid > width:
            substrings.append(string[start : stop - 1])
            start = stop - 1
        elif strwid == width:
            substrings.append(string[start:stop])
            start, stop = stop, stop + 1
        elif string[stop - 1] == _LNSEP or string[stop - 1] == '\n':
            substrings.append(string[start : stop - 1])
            start = stop
            stop += 1
        else:
            stop += 1
    if start < lenstr:
        substrings.append(string[start:])
    return substrings


def _rsplit(string, width):
    if not isinstance(string, str):
        raise TypeError('Type of value of parameter <string> should be "str".')
    if width < _max_char_wid(string):
        raise ValueError(
            'The character in the string has a width larger than '
            'the target width, which cannot be cut to the target width.'
        )
    if not string:
        return [string]
    lenstr = len(string)
    start, stop, substrings = lenstr - 1, lenstr, list()
    while start >= 0:
        strwid = _str_wid(string[start:stop])
        if strwid == width:
            substrings.insert(0, string[start:stop])
            start, stop = start - 1, start
        elif strwid > width:
            substrings.insert(0, string[start + 1 : stop])
            stop = start + 1
        elif string[start] == '\n' or string[start] == _LNSEP:
            substrings.insert(0, string[start + 1 : stop])
            stop = start
            start -= 1
        else:
            start -= 1
    if stop > 0:
        substrings.insert(0, string[:stop])
    return substrings


# TODO BUG：添加的字符串长度超过 MAX_COLUMN_WIDTH 时，
#  对应列的列宽上限会突破 MAX_COLUMN_WIDTH 的限制。
# TODO BUG: 表格不添加任何列时，打印出来的边框线有异常。
