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
        :param style: 预置风格，可用:
            1.table
            2.simple
            3.classic
            4.table-ascii
            5.simple-ascii
            6.classic-ascii
        '''
        Style._check_parameter(style)
        self._initialize()
        self.choose(style)

    @staticmethod
    def _check_parameter(style):
        if style not in __STYLES__.split():
            raise ValueError(
                'No style option like <%s>, available: %s.' % (style, __STYLES__)
            )
        return True

    def _initialize(self):
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
        Style._check_parameter(style)
        self._initialize()
        if style == 'table':
            pass
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
        self._initialize()

    def __setattr__(self, name, value):
        if not isinstance(value, str):
            raise TypeError('Type of attributes of <class "Style"> can only be "str".')
        super().__setattr__(name, value)


class _RowObj(list):
    def __init__(self, iterable, cwhandle, rowhit, alignh, alignv, fbgc):
        super().__init__(iterable)
        self._alignh = alignh
        self._alignv = alignv
        self._alignhs = [alignh] * len(self)
        self._alignvs = [alignv] * len(self)
        self._fbgc = fbgc
        self._fbgcs = [fbgc.copy() for _ in self]
        self._row_hit = rowhit
        self._col_wids = cwhandle

    def _addcol(self, index, value):
        self.insert(index, value)
        self._alignhs.insert(index, self._alignh)
        self._alignvs.insert(index, self._alignv)
        self._fbgcs.insert(index, self._fbgc.copy())

    def _delcol(self, index):
        del self._fbgcs[index]
        del self._alignhs[index]
        del self._alignvs[index]
        return self.pop(index)

    def _height(self, width):
        self._row_hit = width

    def _setclr(self, index, clrs):
        if not clrs:
            self._fbgcs[index].clear()
            return
        if not isinstance(clrs, set):
            clrs = set(clrs)
        self._fbgcs[index].clear()
        self._fbgcs[index].update(clrs)

    def _getclr(self, index):
        return self._fbgcs[index]

    def _gettext(self, left_vert, center_vert, right_vert, padding):
        row_fmted = self._form(padding)
        if not row_fmted:
            return
        for line in row_fmted:
            line[0] = ''.join((left_vert, line[0]))
            line[-1] = ''.join((line[-1], right_vert))
        lines = (center_vert.join(line) for line in row_fmted)
        row_text = _LNSEP.join(lines)
        return row_text

    def _colcap(self, index):
        return _str_wid(str(self[index])) or 1

    def _colflr(self, index):
        string = str(self[index])
        if not string:
            return 1
        return max(_chr_wid(c) for c in string)

    def _align(self, index, alignh, alignv):
        if alignh is not None:
            self._alignhs[index] = alignh
        if alignv is not None:
            self._alignvs[index] = alignv

    def _form(self, padding):
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
        row_with_lines = [list(tup) for tup in zip(*row_with_cells)]
        return row_with_lines


class Table(list):
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
        Table._check_parameter(
            header, alignh, alignv, rowfixed, colfixed, fbgc, fill, style
        )
        super(Table, self).__init__()
        self.rowsText = list()
        self._alignh = alignh
        self._alignv = alignv
        self._col_fixed = colfixed
        self._row_fixed = rowfixed
        self._fbgcolors = fbgc or set()
        self._filler = fill
        self._style = style or Style()
        self._col_wids = list()
        headlist = list(header)
        self.append(
            _RowObj(
                headlist,
                self._col_wids,
                self._row_fixed,
                self._alignh,
                'bottom',
                self._fbgcolors,
            )
        )
        self._num_rows = 1
        self._num_cols = len(headlist)
        str_head = _items_to_str(headlist)
        # 列固定宽度(用户指定)
        self._col_fixeds = [colfixed for _ in headlist]
        # 列最大宽度(字符串宽度)
        self._col_caps = [_str_wid(s) or 1 for s in str_head]
        # 列宽度下限(由列中宽度最大的单个字符决定)
        self._col_floors = [_max_char_wid(s) for s in str_head]
        self._border = dict(hat='', neck='', belt='', shoes='')

    @staticmethod
    def _check_parameter(header, alignh, alignv, rowfixed, colfixed, fbgc, fill, style):
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
                'The fixed row height exceeds the limit(%d), please modify the value \
of "MAX_ROW_HEIGHT" if necessary.'
                % MAX_ROW_HEIGHT
            )
        if not isinstance(colfixed, int):
            raise TypeError('Parameter <colfixed> should be an integer.')
        if colfixed < 0:
            raise ValueError('The value of <colfixed> cannot be less than 0.')
        if colfixed > MAX_COLUMN_WIDTH:
            raise ValueError(
                'The fixed column width exceeds the limit(%d), please modify the value \
of "MAX_COLUMN_WIDTH" if necessary.'
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
        self._text_refresh()
        return self._text()

    __repr__ = __str__

    def addColumn(self, colindex, column=None):
        '''Table 实例对象的插入列的方法。
            1.要插入的列的行数比现有行数多则截断，比现有行数少则用空字符补足；
            2.可不带索引参数 colindex，默认把列插入到所有列末尾。
        :param colindex: int, 插入位置索引。
        :param column: Iterable, 要插入的列。
        :return: None: 无返回值。
        '''
        if column is None:
            column, colindex = colindex, self._num_cols
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
                'The number of columns exceeds the limit(%d), please modify the value \
of MAX_COLUMN_NUM if necessary.'
                % MAX_COLUMN_NUM
            )
        # 如果 column 是生成器、迭代器
        column = list(column)
        for row_ind, row_obj in enumerate(self):
            try:
                obj_to_be_added = column[row_ind]
            except IndexError:
                obj_to_be_added = self._filler
            except Exception:
                raise Exception('Unexpected exception.')
            row_obj._addcol(colindex, obj_to_be_added)
        self._num_cols += 1
        self._col_fixeds.insert(colindex, self._col_fixed)
        self._col_caps.insert(colindex, self._find_cap(colindex))
        self._col_floors.insert(colindex, self._find_floor(colindex))

    def addRow(self, rowindex, row=None):
        '''
        Table 实例的插入行的方法。
            1.要插入的行的列数比现有列数多则截断，比现有列数少则用 filler 补足；
            2.可不带索引参数 rowindex，默认把行插入到所有行末尾。
        :param rowindex: int, 插入位置索引。
        :param row: Iterable, 要插入的行。
        :return: None: 无返回值。
        '''
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
        # 如果row是生成器、迭代器
        row_list = list(row)
        len_lgt, len_row = self._num_cols, len(row_list)
        if len_row > len_lgt:
            row_list = row_list[:len_lgt]
        elif len_row < len_lgt:
            row_list.extend([self._filler] * (len_lgt - len_row))
        row_list = _RowObj(
            row_list,
            self._col_wids,
            self._row_fixed,
            self._alignh,
            self._alignv,
            self._fbgcolors,
        )
        self.insert(rowindex, row_list)
        self._num_rows += 1
        for colind in range(self._num_cols):
            self._col_caps[colind] = self._find_cap(colind)
            self._col_floors[colind] = self._find_floor(colind)

    def getColumn(self, colindex=-1):
        self._check_index(colindex=colindex)
        if colindex is None:
            return
        return [row[colindex] for row in self]

    def getRow(self, rowindex=-1):
        self._check_index(rowindex)
        if rowindex is None:
            return
        return list(self[rowindex])

    def getItem(self, rowindex=-1, colindex=-1):
        self._check_index(rowindex, colindex)
        if rowindex is None or colindex is None:
            return
        return self[rowindex][colindex]

    def getString(self, rowindex=-1, colindex=-1):
        self._check_index(rowindex, colindex)
        if rowindex is None or colindex is None:
            return
        return str(self[rowindex][colindex])

    def writeCell(self, rowindex=None, colindex=None, *, value):
        self._check_index(rowindex, colindex)
        if rowindex is None and colindex is None:
            for row in self:
                for colind in range(len(row)):
                    row[colind] = value
                    self._col_caps[colind] = self._find_cap(colind)
                    self._col_floors[colind] = self._find_floor(colind)
        elif rowindex is None or colindex is None:
            if rowindex is None:
                for row in self:
                    row[colindex] = value
                self._col_caps[colindex] = self._find_cap(colindex)
                self._col_floors[colindex] = self._find_floor(colindex)
            else:
                for colind in range(len(self[rowindex])):
                    self[rowindex][colind] = value
                    self._col_caps[colind] = self._find_cap(colind)
                    self._col_floors[colind] = self._find_floor(colind)
        else:
            self[rowindex][colindex] = value
            self._col_caps[colindex] = self._find_cap(colindex)
            self._col_floors[colindex] = self._find_floor(colindex)

    def clearCell(self, rowindex=None, colindex=None):
        self.writeCell(rowindex, colindex, value='')

    def isEmpty(self, rowindex=None, colindex=None):
        self._check_index(rowindex, colindex)
        if rowindex is None and colindex is None:
            return not any(
                any(bool(row[colind]) for colind in range(len(row))) for row in self
            )
        elif rowindex is None or colindex is None:
            if rowindex is None:
                return not any(bool(row[colindex]) for row in self)
            else:
                return not any(self[rowindex])
        else:
            return not bool(self[rowindex][colindex])

    def isFull(self, rowindex, colindex):
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
        Table 实例对象的删除列方法。
            1.根据列的索引值 colindex 删除对应的列；
            2.将所删除的列以一维列表形式返回。
        :param colindex: int, 要删除的列的索引值。
        :return: list, 以列表形式返回已删除的列。
        '''
        if not isinstance(colindex, int):
            raise TypeError(
                'Integer parameter <colindex> expected, got %s.'
                % type(colindex).__name__
            )
        if -self._num_cols > colindex >= self._num_cols:
            raise IndexError('Column index out of range.')
        columnlist = list()
        for row in self:
            columnlist.append(row._delcol(colindex))
        self._num_cols -= 1
        del self._col_fixeds[colindex]
        del self._col_caps[colindex]
        del self._col_floors[colindex]
        return columnlist

    def delRow(self, rowindex):
        '''
        Table 实例对象的删除行方法。
            1.根据列的索引值 rowindex 删除对应的行；
            2.将所删除的行以一维列表形式返回。
        :param rowindex: int, 要删除的行的索引值。
        :return: list, 以列表形式返回已删除的行。
        '''
        if not isinstance(rowindex, int):
            raise TypeError(
                'Integer parameter <rowindex> expected, got %s.'
                % type(rowindex).__name__
            )
        if -self._num_rows > rowindex >= self._num_rows:
            raise IndexError('Row index out of range.')
        rowlist = list(self.pop(rowindex))
        self._num_rows -= 1
        for colindex in range(self._num_cols):
            self._col_caps[colindex] = self._find_cap(colindex)
            self._col_floors[colindex] = self._find_floor(colindex)
        return rowlist

    def setColumnWidth(self, colindex, width=None):
        '''
        Table 实例对象的设置列宽方法。
            不带列索引参数 colindex，则设置所有列的宽度。
        :param colindex: int, 要设置宽度的列索引。
        :param width: int, 要设置的列宽度。
        :return: None: 无返回值。
        '''
        if width is None:
            width, colindex = colindex, None
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
                'The column width to be set exceeds the limit(%d), please modify the \
value of "MAX_COLUMN_WIDTH" if necessary.'
                % MAX_COLUMN_WIDTH
            )
        if colindex is None:
            self._col_fixeds = [width for _ in self._col_fixeds]
            return
        self._col_fixeds[colindex] = width

    def setRowHeight(self, rowindex, height=None):
        '''
        Table 实例对象的设置行高方法。
            不带行索引参数 rowindex，则设置所有行的高度。
        :param rowindex: int, 要设置高度的行索引。
        :param height: int, 要设置的行高度。
        :return: None: 无返回值。
        '''
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
                'The row height to be set exceeds the limit(%d), please modify the \
value of "MAX_ROW_HEIGHT" if necessary.'
                % MAX_ROW_HEIGHT
            )
        if rowindex is None:
            for row in self:
                row._height(height)
            return
        self[rowindex]._height(height)

    def setAlignment(self, rowindex=None, colindex=None, *, alignh=None, alignv=None):
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
        if rowindex is not None and colindex is not None:
            if -self._num_rows > rowindex >= self._num_rows:
                raise IndexError('Row index out of range.')
            if -self._num_cols > colindex >= self._num_cols:
                raise IndexError('Column index out of range.')
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
        self._check_index(rowindex, colindex)
        return self[rowindex]._getclr(colindex)

    def defaultClr(self, value):
        if not isinstance(value, (list, tuple, set)):
            raise TypeError(
                'Type of parameter <fbgc> should be "tuple"、"list" or "set".'
            )
        if not all(isinstance(s, str) for s in value):
            raise ValueError(
                'The type of the color name in the collection can only be "str".'
            )
        self._fbgcolors = value

    def defaultAlign(self, *, alignh=None, alignv=None):
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
        if alignh:
            self._alignh = alignh
        if alignv:
            self._alignv = alignv

    def setStyle(self, style):
        if not isinstance(style, Style):
            raise TypeError('Type of parameter <style> should be a "Style" object.')
        self._style = style

    def defaultFill(self, fill=''):
        self._filler = fill

    @staticmethod
    def limit(item, value):
        global MAX_COLUMN_NUM, MAX_COLUMN_WIDTH, MAX_ROW_HEIGHT
        if not isinstance(item, str):
            raise TypeError('The attribute "item" should be "str".')
        if not isinstance(value, int):
            raise TypeError('The limit value should be "int".')
        if value not in range(1, 301):
            raise ValueError('The limit value should be in range of 1 to 300.')
        if item == 'MAX_COLUMN_NUM':
            MAX_COLUMN_NUM = value
        elif item == 'MAX_COLUMN_WIDTH':
            MAX_COLUMN_WIDTH = value
        elif item == 'MAX_ROW_HEIGHT':
            MAX_ROW_HEIGHT = value

    def show(
        self,
        start=0,
        stop=None,
        *,
        colorful=True,
        header=True,
        file=sys.stdout,
        refresh=True
    ):
        if not isinstance(start, int):
            raise TypeError('Type of parameter <start> should be "int".')
        if not isinstance(stop, int) and stop is not None:
            raise TypeError('Type of parameter <stop> should be "int" or "None".')
        if not isinstance(file, (TextIOWrapper, StdOutputFile, StreamWrapper)):
            raise TypeError('Type of <file> is not Python file object.')
        global _COLORFUL
        if not colorful:
            _COLORFUL = False
        if refresh or not self:
            self._text_refresh()
        if _NT and not run_on_idle and (file is sys.stdout):
            self._print_win(start, stop, header)
        else:
            text = self._text(start, stop, header)
            try:
                file.write(text)
                file.write(_LNSEP)
                file.flush()
            except Exception:
                raise IOError('Failed to write to file or print on the console.')
        _COLORFUL = True
        if file is sys.stdout:
            return
        try:
            file.close()
        except Exception:
            pass

    def _print_win(self, start, stop, header):
        self._col_wids_refresh()
        hat = self._border['hat']
        neck = self._border['neck']
        belt = self._border['belt']
        shoes = self._border['shoes']
        pad = self._style.cell_pad
        sys.stdout.write(hat + _LNSEP)
        if header:
            headerform = self[0]._form(pad)
            for line in headerform:
                len_line = len(line)
                sys.stdout.write(self._style.left_vert)
                for ind, string in enumerate(line):
                    sys.stdout.write(string)
                    if ind != len_line - 1:
                        sys.stdout.write(self._style.center_vert)
                sys.stdout.write(self._style.right_vert + _LNSEP)
            sys.stdout.write(neck + _LNSEP)
        body = self[1:][start:stop]
        len_body = len(body)
        for index, bodyrow in enumerate(body):
            rowform = bodyrow._form(pad)
            for line in rowform:
                sys.stdout.write(self._style.left_vert)
                len_line = len(line)
                for ind, string in enumerate(line):
                    sys.stdout.write(string)
                    if ind != len_line - 1:
                        sys.stdout.write(self._style.center_vert)
                sys.stdout.write(self._style.right_vert + _LNSEP)
            if (index != len_body - 1) and belt:
                sys.stdout.write(belt + _LNSEP)
        sys.stdout.write(shoes + _LNSEP)

    def _text_refresh(self):
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
        self.rowsText.clear()
        for row_obj in self:
            self.rowsText.append(
                row_obj._gettext(
                    self._style.left_vert,
                    self._style.center_vert,
                    self._style.right_vert,
                    self._style.cell_pad,
                )
            )

    def _text(self, start=0, stop=None, header=True):
        hat = self._border['hat']
        neck = self._border['neck']
        belt = self._border['belt']
        shoes = self._border['shoes']
        if belt:
            belt = ''.join((_LNSEP, belt, _LNSEP))
        else:
            belt = _LNSEP
        body = belt.join(self.rowsText[1:][start:stop])
        if not header:
            group = (hat, body, shoes)
        else:
            group = (hat, self.rowsText[0], neck, body, shoes)
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
    if code in (0x0000, 0x0008, 0x0009, 0x000B, 0x000D, 0x001F, 0x007F):
        return 0
    # 猜测其他 Unicode 字符宽度为 1
    return 1


def _str_wid(string):
    '''返回字符串的总宽度。(以半角英文字符占一个单位宽度为基准)'''
    return sum(_chr_wid(char) for char in string)


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
            'The character in the string has a width \
larger than the target width, which cannot be cut to the target width.'
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
            'The character in the string has a width \
larger than the target width, which cannot be cut to the target width.'
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


# TODO 隐含BUG：添加的字符串长度超过 MAX_COLUMN_WIDTH 时，对应列的列宽上限会突破 MAX_COLUMN_WIDTH 的限制。
