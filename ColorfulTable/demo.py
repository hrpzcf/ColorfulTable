import os, sys

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

# 以下导入分别为 表格类、风格类
# 如果对表格风格没有自定义需求，Style 也不需要导入
# 使用 from ColorfulTable import * 的方式也可以全部导入以下类别
from colorfultable import Table, Style

# 以下是修改 最大行高、最大列宽、最大列数限制
# 三项默认分别是 20，80，30，行数则没有限制
# 这些操作不是必需的，一般使用默认限制就可以了
# 这些限制设置后对所有表格实例的后续操作产生限制
Table.limit('MAX_ROW_HEIGHT', 30)
Table.limit('MAX_COLUMN_WIDTH', 100)
Table.limit('MAX_COLUMN_NUM', 50)

# 随意创建一个表格。初始标题行参数不限于列表，可迭代对象都可以，比如元组('序号',)
# 可迭代对象内的子数据类型不限于字符串，任意 Python 数据类型都可以，表格会调用其 str 方法显示
# 表格其他初始参数皆可不写，其他参数功能、用法见文档中的Table类初始化参数
mytable = Table(['序号'], fbgc={'bg_blue'})

# 表格只有一列，后悔了，想继续添加多列标题：
column_titles = '姓名', '学号', '科目', '成绩'  # 想要添加的列标题

# 循环使用 addColumn 方法添加列：
for title in column_titles:
    # 注意 addcolumn 是添加一个竖列，直接用 addColumn(column_titles) 是不对滴
    # addColumn 方法接受的两个参数分别是：插入位置索引、要添加的竖列（可迭代对象）
    # 这里我们忽略列索引参数，默认添加为最后一列。竖列 [title] 第一项当然就是标题咯
    mytable.addColumn([title])

# 使用添加行方法 addRow 添加一行，第一个参数 1 表示插入到第 1 行前面
# 这里的索引参数 1 同样可以和 addColumn 方法一样不写，会默认插入为最后一行
mytable.addRow(1, [1, '小白', '123456789', '打瞌睡', 100])
mytable.addRow((2, '小黑', '987654321', '调皮捣蛋', 100))  # 注意这里演示不带行索引
mytable.addRow((3, '小黄', '123454321', '发呆', 100))

# 现在我们给第 4 列“科目”整列设置前景色（文字颜色）和背景色
# 第一个参数是行索引，这里为 None 表示不限于特定行，所有行都包含（列索引为 None 同理）
# 第二个参数是列索引，3 表示第四列
# 也可以这样写：mytable.setColor(colindex=3, clrs={'fg.Yellow', 'bg.BrightBlack'})
# 因为 setColor 方法所有参数默认值都是 None
# 可以直接忽略 rowindex，以关键字参数方式指定 colindex 的值
# 注意，自带的颜色模块只支持 linux 等平台的终端显示表格颜色
# windows 平台终端要显示颜色则需要安装第三方模块 colorama，否则不能显示颜色
# 不管在哪两个平台上，用 IDLE 运行程序都不支持显示颜色
mytable.setColor(None, 3, clrs={'fg_green', 'bg_brightblack'})

# 对自适应列宽不满意？设置固定列宽
# setColumnWidth方法第一个参数是 列索引，第二个参数是 列宽值
# 其中 列索引可以不写，比如 mytable.setColumnWidth(30) 是设置所有列的宽度为 30
# 设置行高方法 setRowHeight 同理，只不过第一个参数是 行索引，而不是列索引
# 注意，此时的 列宽 数值指的是以一个半角字母宽度为标准 1 宽度计数的数值，不是像素值
# 行高 则指的是文字行数
mytable.setColumnWidth(3, 30)

# 设置水平和垂直对齐方式（对齐方式可用值见 README.md 文档）
mytable.setAlignment(None, 3, alignh='c')
# 想同时设置垂直对齐方式？
# mytable.setAlignment(None, 3, alignh='c', alignv='m')

# 在控制台上显示表格，具体参数见 README.md 中的 Table 类实例方法之 show 方法
mytable.show()

print('\n' * 3)

# 选择别的表格边框风格
otherstyle = Style('classic')
mytable.setStyle(otherstyle)
# 也可以在初始化表格的时候添加 style 参数
# mytable2 = Table(['序号'], fbgc={'fg.Yellow'}, style=otherstyle)
mytable.show()

print('\n' * 3)

# 想更精确地自定义？（不仅限于以下属性）
# 具体属性请查看 README.md 中的 Style 类
otherstyle.split_cross = '╳'
otherstyle.top_left = '╭'
otherstyle.top_right = '╮'
otherstyle.bottom_left = '╰'
otherstyle.bottom_right = '╯'
mytable.show()

print('\n' * 3)

# 重置风格
otherstyle.reset()

# 也可以操作当前风格实例选择新的风格
otherstyle.choose('simple')
# 或者再创建一个 Style 实例，再调用 Table 的 setStyle 方法设置风格，都可以
# style2 = Style('simple')
# mytable.setStyle(style2)

# 清空颜色设置
mytable.setColor()

mytable.show()

input('Press ENTER to exit.')

# 细节：
# 表格中中文与英文混合使用时是否对齐与字体、运行的控制台类型有关
# windows 平台上，程序输出于 cmd、PowerShell 时表格里无论中英文对齐都非常好
# 以上终端（不限）建议把自动折行关掉，否则表格超过终端屏幕宽度时自动折行会使表格凌乱
# IDLE、PyCharm等的中文对齐则非常凌乱
# 这是第一个可用版本，BUG 比较多，功能也相对简单，后续会添加新功能
