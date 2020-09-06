# ColorfulTable

## 模块简介

ColorfulTable 是一个用于在控制台上打印漂亮表格的 Python3 模块，使用它可以方便地构建表格并选择打印到控制台上。

- 支持 Linux、Windows 平台
- 预置 6 种表格（边框）样式，也支持自定义
- 支持自定义每个单元格独立的字体颜色和背景色
- 支持单元格内换行（如果储存对象是字符串）
- 支持设置水平对齐方式和垂直对齐方式
- 支持对指定行或列设置固定行高和列宽，也支持设置自适应行高和列宽
- 按单元格储存任意受支持的 Python 数据类型（以对象的 str 方法显示单元格内容）
- 输出函数支持自定义要打印的行数范围，是否打印表格标题行，支持输出到 Python 文件对象
- 等等...

---


## 函数文档

- ### Table类

1. #### 类初始化参数

   ------
   
   > **header**
   
   **必选**位置参数，创建表格类Table类实例时的初始行（标题行），header数据类型应为可迭代对象，子数据类型则不限。
   
   例如：
   
   ```python
   mytable1 = Table(range(6))
   ```
   
   或者：
   
   ```python
   mytable2 = Table((1, 2, 3, ))
   ```
   
   或者：
   
   ```python
   mytable3 = Table(['序号', '姓名', '学号', '分数', '备注'])
   ```
   
   ---
   
   > **alignh**
   
   可选**关键字**参数，该参数是当未指定水平对齐方式时默认使用的水平对齐方式，可用值为 'l'、'left'、'c'、'center'、'r'、'right'，默认值为 'l'。
   
   ---
   
   > **alignv**
   
   可选**关键字**参数，该参数是当未指定垂直对齐方式时默认使用的垂直对齐方式，可用值为 't'、'top'、'm'、'middle'、'b'、'bottom'，默认值为 't'。
   
   ---
   
   > **rowfixed**
   
   可选**关键字**参数，该参数是表格默认行高，可用值为 0 或小于 MAX_ROW_HEIGHT（见第21条：limit）的正整数，默认值为 0（自适应行高）。
   
   ---
   
   > **colfixed**
   
   可选**关键字**参数，该参数是表格默认列宽，可用值为 0 或小于 MAX_COLUMN_WIDTH（见第21条：limit）的正整数，默认值为 0（自适应列宽）。
   
   ---
   
   > **fbgc**
   
   可选**关键字**参数，该参数是默认的单元格前景色和背景色，参数值数据类型应为包含颜色代码(字符串)的列表 "list"，默认值为空列表。可用颜色代码见下表：

   | 序号  |   颜色码(字符串) | 代表颜色               |
   | :---: | ---------------: | :--------------------- |
   |   1   |         fg.reset | 重置前景色和背景色     |
   |   2   |           fg.red | 前景红色               |
   |   3   |         fg.green | 前景绿色               |
   |   4   |        fg.yellow | 前景黄色               |
   |   5   |          fg.blue | 前景蓝色               |
   |   6   |       fg.magenta | 前景品红色（紫色）     |
   |   7   |          fg.cyan | 前景青色               |
   |   8   |         fg.white | 前景白色               |
   |   9   |   fg.brightblack | 前景亮黑色（灰色）     |
   |  10   |     fg.brightred | 前景亮红色             |
   |  11   |   fg.brightgreen | 前景亮绿色             |
   |  12   |  fg.brightyellow | 前景亮黄色             |
   |  13   |    fg.brightblue | 前景亮蓝色             |
   |  14   | fg.brightmagenta | 前景亮品红色（亮紫色） |
   |  15   |    fg.brightcyan | 前景亮青色             |
   |  16   |   fg.brightwhite | 前景亮白色             |
   |  17   |         bg.reset | 重置前景色和背景色     |
   |  18   |           bg.red | 背景红色               |
   |  19   |         bg.green | 背景绿色               |
   |  20   |        bg.yellow | 背景黄色               |
   |  21   |          bg.blue | 背景蓝色               |
   |  22   |       bg.magenta | 背景品红色（紫色）     |
   |  23   |          bg.cyan | 背景青色               |
   |  24   |         bg.white | 背景白色               |
   |  25   |   bg.brightblack | 背景亮黑色（灰色）     |
   |  26   |     bg.brightred | 背景亮红色             |
   |  27   |   bg.brightgreen | 背景亮绿色             |
   |  28   |  bg.brightyellow | 背景亮黄色             |
   |  29   |    bg.brightblue | 背景亮蓝色             |
   |  30   | bg.brightmagenta | 背景亮品红色（亮紫色） |
   |  31   |    bg.brightcyan | 背景亮青色             |
   |  32   |   bg.brightwhite | 背景亮白色             |
   
   ---
   
   > **fill**
   
   可选**关键字**参数，该参数是进行 addRow 或 addColumn 操作时，如果要添加的行或列长度不足，则用 fill 补足。参数值数据类型不限，默认值为空字符串 ''。
   
   > **style**
   
   可选**关键字**参数，该参数是默认的表格边框风格类型，参数值数据类型应为 Style 的类实例，可用值见以下 "Style 类"。





2. #### 添加列方法 - addColumn
   
   ---
   
   > 方法原型
   
   ```python
   addColumn(colindex, column)
   ```
   
   - colindex 为索引参数，表示要插入列的位置。
   - column 为要插入的列，参数值数据类型应为可迭代对象，子数据则不限类型。column 长度不足则用以上的类初始参数 fill  补足，过长则截断。
   - 可以不带 colindex 参数，默认添加列为末尾列。
   
   
   
   > 返回值
   
   - None
   
   
   
   
   > 异常

   - colindex 不是整数则触发 TypeError 异常。
   - column 不是可迭代对象则触发 TypeError 异常。
   
   
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '分数', '备注'])
   mytable.addColumn(3, ['科目', '此行会被截断'])
   ```
   
   或者：
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '分数', '备注'])
   mytable.addColumn(['分数等级', '此行会被截断'])
   ```





3. #### 添加行方法 - addRow
   
   ---
   
   > 方法原型
   
   ```python
   addRow(rowindex, row)
   ```
   
   - colindex 为索引参数，表示要插入行的位置。
   
   - row 为要插入的行，数据类型应为可迭代对象，子数据则不限类型。row 长度不足则用以上的类初始参数 fill 补足，过长则截断。
   
   - 可以不带 rowindex 参数，默认添加列为末尾列。
   
     

   > 返回值
   
   - None
   
     
   
   > 异常
   
   - rowindex 不是整数则触发 TypeError 异常。
   
   - row 不是可迭代对象则触发 TypeError 异常。
   
     
   
   > 示例：
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
   mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
   ```





4. #### 获取列方法 - getColumn
   
   ---
   
   > 方法原型
   
   ```python
   getColumn(colindex)
   ```
   
   - colindex 为索引参数，表示要获取的列的位置。
   - 可以不带 colindex 参数，默认获取最后一列。
   
     
   
   > 返回值
   
   - 包含列数据的列表。
   
     
   
   > 异常
   
   - colindex 不是整数则触发 TypeError 异常；
   - colindex 超出范围则触发 IndexError异常。
   
     
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
   mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
   col = mytable.getColumn(3)
   print(col)
   # ['科目', '打瞌睡']
   ```





5. #### 获取行方法 - getRow
   
   ---
   
   > 方法原型
   
   ```python
   getRow(rowindex)
   ```
   
   - rowindex 为索引参数，表示要获取的行的位置。
   - 可以不带 rowindex 参数，默认获取最后一行。
   
     
   
   > 返回值
   
   - 包含行数据的列表。
   
     
   
   > 异常
   
   - rowindex 不是整数则触发 TypeError 异常。
   - rowindex 超出范围则触发 IndexError异常。
   
     
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
   mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
   row = mytable.getRow(0)
   print(row)
   # ['序号', '姓名', '学号', '科目', '分数', '备注']
   ```





6. #### 获取单元格数据方法 - getItem
   
   ---
   
   > 方法原型
   
   ```python
   getItem(rowindex, colindex)
   ````
   
   - rowindex 为索引参数，表示行索引。
   - colindex 为索引参数，表示列索引。
   - 可以不带 rowindex 、colindex 参数之一或全部，不带的参数默认为 -1（最后一行或列）。
   
     
   
   > 返回值
   
   - 单元格里的数据。
   
     
   
   > 异常
   
   - rowindex 、colindex 不是整数则触发 TypeError 异常。
   - rowindex 、colindex 超出范围则触发 IndexError异常。
   
     
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
   mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
   item = mytable.getItem(1, 4)
   print(item)
   # 100
   ```





7. #### 获取单元格字符串方法 - getString
   
   ---
   
   - 与 getItem 大致相同，返回值为单元格里的数据的字符串形式。
   
     
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
   mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
   string = mytable.getString(1, 4)
   print(string)
   # '100'
   ```





8. #### 覆写单元格数据方法 - writeCell
   
   ---
   
   > 方法原型
   
   ```python
   writeCell(rowindex, colindex, *, value)
   ```
   
   - rowindex 为索引参数，表示行索引。
   - colindex 为索引参数，表示列索引。
   - 索引参数可以为 None 或整数。
   - value 为**必选**参数，为要写入的值，不限数据类型，必须以关键字参数方式调用。
   - 可以不带 rowindex 、colindex 参数之一或全部，不带的参数默认为 None。
   - rowindex  和 colindex 参数可用值为 None 或整数，当 rowindex  为 None，colindex 不为 None 时，以 value 覆写 colindex 所代表的整列数据，反之亦然。两个参数都为 None 时，以 value 覆写表格全部数据。
   - 当不带 rowindex 参数时，colindex 应以关键字参数方式调用，反之则不用。
   
     
   
   > 返回值
   
   - None
   
     
   
   > 异常
   
   - rowindex 、colindex 不是整数则触发 TypeError 异常。
   - rowindex 、colindex 超出范围则触发 IndexError异常。
   
     
   
   > 示例
   
   ```python
   mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
    mytable.writeCell(colindex=4, value=8) # 以 8 覆写第 5 列所有数据
    mytable.writeCell(1, value=8) # 以 8 覆写第 2 行所有数据
    mytable.writeCell(value=8) # 以 8 覆写整个表格所有数据
    mytable.writeCell(1, 2, value=8) # 以 8 覆写第2行第3列单元格的数据
   ```





9. #### 清空单元格方法 - clearCell
   
   ---
   
   > 方法原型
   
   ```python
   clearCell(rowindex, colindex)
   ```
   
   - 调用方法大致与 writeCell 方法相同，只是没有 value 参数。





10. #### 测试单元格是否为空方法 -  isEmpty
    
    ---
    
    > 方法原型
    
    ```python
    isEmpty(rowindex, colindex)
    ```
    
    - 索引参数使用方法与 overwrite 方法相同。






11. #### 测试单元格是否全部非空方法 - isFull
    
    ---
    
    > 方法原型
    
    ```python
    isFull(rowindex, colindex)
    ```
    
    - 索引参数使用方法与 writeCell 方法大致相同。





12. #### 删除列方法 - delColumn
    
    ---
    
    > 方法原型
    
    ```python
    delColumn(colindex)
    ```
    
    - 参数 colindex 为要删除的列索引。
    
      
    
    > 返回值
    
    - 包含删除的列元素的列表。
    
      
    
    > 异常
    
    - colindex 不是整数时触发 TypeError 异常。
    - colindex 超出范围时触发 IndexError 异常。
    
      
    
    > 示例
    
    ```python
    mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
    column = mytable.delColumn(5) # 删除第5列
    print(column)
    # ['备注', '']
    ```





13. #### 删除行方法 - delRow
    
    ---
    
    > 方法原型
    
    ```python
    delRow(rowindex)
    ```
    
    - 参数 rowindex 为要删除的行的索引值。
    
      
    
    > 返回值
    
    - 包含已删除的行的元素的列表。
    
      
    
    > 异常
    
    - rowindex 不是整数时触发 TypeError 异常。
    - rowindex 超出范围时触发 IndexError 异常。
    
      
    
    > 示例
    
    ```python
    mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
    row = mytable.delRow(0) # 删除第一行
    print(row)
    # ['序号', '姓名', '学号', '科目', '分数', '备注']
    ```





14. #### 设置列宽方法 - setColumnWidth
    
    ---
    
    > 方法原型
    
    ```python
    setColumnWidth(colindex, width)
    ```
    
    - 参数 colindex 为要设置列宽的列索引；width 为要设置的宽度，可用值为 0 或小于 MAX_COLUMN_WIDTH（见第21条：limit）的正整数，0 代表自适应列宽。
    - 当只填一个参数时，该参数默认为 width，意为将所有列的列宽设置为 width。
    
      
    
    > 返回值
    
    - None
    
      
    
    > 异常
    
    - 当 colindex 不为整数时触发 TypeError 异常。
    - colindex 超出范围时触发 IndexError 异常。
    - width 大于 MAX_COLUMN_WIDTH 时触发 ValueError 异常。
    
      
    
    > 示例
    
    ```python
    mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.setColumnWidth(0, 0) # 将第一列的列宽设置为自适应宽度
    mytable.setColumnWidth(10) # 将所有列的列宽设置为 10
    ```





15. #### 设置行高方法 - setRowHeight
    
    ---
    
    > 方法原型
    
    ```python
    setRowHeight(rowindex, height)
    ```
    
    - 参数 rowindex 为要设置行高的行索引；height 为要设置的行高，可用值为 0 或小于 MAX_ROW_HEIGHT（见第21条：limit）的正整数，0 代表自适应行高。
    - 参数使用方法与 setColumnWidth 方法相同，只是索引参数变为行索引值。





16. #### 设置单元格对齐方式方法 -  setAlignment
    
    ---
    
    > 方法原型
    
    ```python
    setAlignment(rowindex=None, colindex=None, *, alignh=None, alignv=None)
    ```
    
    - 参数 rowindex 为行索引，可用值为 None 或整数；colindex 为列索引，可用值为 None 或整数。
    - 参数 alignh 为水平对齐方式，alignv 为垂直对齐方式，它们的可用值见前面的“类初始参数”。
    - 对于行索引 rowindex 和列索引 colindex，都不为 None 则表示设置对应单元格对齐方式；其中一个为 None 则表示设置整行或整列的对齐方式；都为 None 则设置整个表格所有的单元格对齐方式。
    - 对于 水平对齐方式 alignh 和 垂直对齐方式 alignv，可以只调用其中一个，调用哪个就设置什么对齐方式，但都必须以关键字参数方式调用。
    
      
    
    > 返回值
    
    - None
    
      
    
    > 异常
    
    - rowindex 和 colindex 不为整数时触发 TypeError 异常，超出范围则触发 IndexError 异常。
    - alignh 和 alignv 不是有效选项时触发 ValueError 异常。
    
      
    
    > 示例
    
    ```python
    mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
    
    mytable.setAlignment(0, 1, alignh='c')
    # 设置第一行第二列所指单元格的水平对齐方式为居中对齐。
    
    mytable.setAlignmemt(alignv='m')
    mytable.setAlignment(None, None, alignv='m')
    #以上两种方法都是设置所有单元格的垂直对齐方式为居中对齐，但明显前面一种方法更方便，后面一种方法是没有必要的，因为行列索引参数的默认值就是 None，没必要再填一次。
    
    mytable.setAlignment(1, alignh='c', alignv='b')
    # 设置第一行所有单元格的水平对齐方式为居中，垂直对齐方式为底端对齐。此方法忽略的索引参数其实是 colindex，而不是 rowindex。
    
    mytable.setAlignment(colindex=2, alignh='r', alignv='m')
    mytable.setAlignment(None, 2, alignh='r', alignv='m')
    # 以上两种方法都是将第三列所有单元格的水平、垂直对齐方式分别设置为 右对齐、居中对齐。要省略 rowindex，则 colindex 就需以关键字参数方式调用，否则就不能省略 rowindex 的值 None。
    ```





17. #### 设置单元格前景色和背景色方法 - setColor
    
    ---
    
    > 方法原型
    
    ```python
    setColor(rowindex=None, colindex=None, *, clrs=None)
    ```
    
    - 索引 rowindex、colindex 使用方法与 setAlignment 方法相同。
    - 颜色参数 clrs 数据类型应为集合、元组或列表，集合里包含颜色码。可用颜色码见“类初始参数”中的表格。
    
      
    
    > 示例
    
    ```python
    mytable = Table(['序号', '姓名', '学号', '科目', '分数', '备注'])
    mytable.addRow(1, (1, '小明', '123', '打瞌睡', 100))
    
    mytable.setColor(clrs={'fg.yellow', 'bg.red'})
    # 设置所有单元格的颜色为 {'fg.yellow', 'bg.red'}，即前景色：黄，背景色：红。
    
    mytable.setColor(None, 0, clrs={'fg.red'})
    # 设置第一列所有单元格的前景色为红色（注：此时单元格的原有颜色会被清空，如果想要单元格的颜色不被清空，请用 getColor 方法获取单元格的颜色集合，再用集合的方法对获取到的颜色集合进行更改）
    ```





18. #### 设置表格边框风格方法 - setStyle
    
    ---
    
    > 方法原型
    
    ```python
    setStyle(style)
    ```
    
    - 参数 style 的值应为 Style 类的实例，详细用法见末尾的“Style类”。





19. #### 设置填充对象方法 - defaultFill
    
    ---
    
    > 方法原型
    
    ```python
    defaultFill(fill='')
    ```
    
    - 用于设置默认的填充对象，即添加行或列时，要添加的行或列的长度比原表格行或列的长度短时，使用 fill 填充至等长。
    - 参数 fill, 数据类型不限，默认值为空字符串 ''。





20. #### 输出表格方法 - show

    ---

    > 方法原型

    ```python
    show(start=0, stop=None, *, colorful=True, header=True, file=sys.stdout, refresh=True)
    ```

    - start 和 stop 为要输出的表格的起始行和结束行（不包括标题行），数据类型应为整数。
    - colorful 为是否要按设置的颜色将表格打印到终端上，值为 False 将按默认颜色打印（设置的颜色不会被清除，下次 colorful 为 True 时仍然可以按已经设置的颜色打印），数据类型应为布尔值。
    - header 为是否显示标题行，数据类型应为布尔值。
    - file 为 Python 文件对象，默认为标准输出流 sys.stdout。
    - refresh 为是否刷新表格显示文本(Table 实例调用过 show 方法后，再对实例进行添加行列等操作，再次调用 show 方法时，如果参数 refresh 为 False，则表格文本不会更新，输出与上次一样)，参数默认为 True。
    - 以上参数可以自由选择调用，也可以全部使用默认；后 4 个参数只能以关键字参数方式调用。





21. #### 最大行高列宽列数限制方法 - limit

    ---

    > 方法原型
    
    ```python
    limit(item, value)
    ```

    - 参数 item 只接受以下字符串：

        `MAX_ROW_HEIGHT`
    
        `MAX_COLUMN_NUM`
    
        `MAX_COLUMN_WIDTH`

    - 参数 value 只接受大于 1 小于 300 的整数。
    - 当 item 值为 MAX_ROW_HEIGHT 时，设置行高最大限制为 value。
    - 当 item 值为 MAX_COLUMN_NUM 时，设置列数最大限制为 value。
    - 当 item 值为 MAX_COLUMN_WIDTH 时，设置列宽最大限制为 value。





22. #### 设置默认颜色方法 - defaultClr

    ------

    > 方法原型

    ```python
    defaultClr(value)
    ```

    - 参数 value 值类型应为列表(list)、元组(tuple)、集合(set)之一
    - value 里包含的字符串应为可用的颜色码（见 Table 类初始化参数 fbgc 的可用颜色码表格）

    
    
    > 异常

    - 当 value 类型不符合要求时触发 TypeError 异常
    - 当 value 所包含的值不是可用颜色码时触发 ValueError 异常





23. #### 设置默认对齐方式方法 - defaultAlign

    ------
    
    > 方法原型
    
    ```python
    defaultAlign(*, alignh=None, alignv=None)
    ```
    
    - 参数 alignh 为默认使用的水平对齐方式
    - 参数 alignv 为默认使用的垂直对齐方式
    - 两个参数都需要以关键字参数方式调用，不需要设置的对齐方式可以不写

    
    
    > 异常
    
    - 当 alignh 为无效的值时触发 ValueError 异常
    - 当 alignv 为无效的值时触发 ValueError 异常





24. #### 设置默认填充的值方法 - defaultFill

    ------
    
    > 方法原型
    
    ```python
    defaultFill(fill='')
    ```
    
    - 参数 fill 默认值为空字符串，也就是直接调用不填参数时将会把默认填充的值设置为空字符串








- ### Style类
  

1. #### 类实例属性

    ------

    > 等号左边为属性，等号右边为默认值。
    
    - `cell_pad = ' '` 单元格内容左右两边的填充字符
    - `top_left = '┌'` 表格边框左上角字符
    - `top_cross = '┬'`  边框顶部三交叉点字符
    - `top_right = '┐'` 边框右上角字符
    - `top_horz = '─'` 顶部边框水平线字符
    - `bottom_left = '└'` 边框左下角字符
    - `bottom_cross = '┴'` 边框底部三交叉点字符
    - `bottom_right = '┘'` 边框右下角字符
    - `bottom_horz = '─'` 底部边框水平线字符
    - `left_cross = '├'` 左边框三交叉点字符
    - `left_vert = '│'` 左边框垂直线字符
    - `right_cross = '┤'` 右边框三交叉点字符
    - `right_vert = '│'` 右边框三交叉点字符
    - `center_horz = '─'` 中间水平线字符
    - `center_vert = '│'` 中间垂直线字符
    - `center_cross = '┼'` 中间十字交叉点字符
    - `split_left = '╞'` 标题行与主体分隔线左边框三交叉点字符
    - `split_right = '╡'` 标题行与主体分隔线右边框三交叉点字符
    - `split_horz = '═'` 标题行与主体分隔线水平线字符
    - `split_cross = '╪'` 标题行与主体分隔线十字交叉点字符





2. #### 类初始化参数

    ------

   > style

    例：
   
    ```python
    mystyle = Style(style)
    ```

   - 参数 style 可用值为以下字符串：

      `table`
      `simple`
      `classic`
      `table-ascii`
      `simple-ascii`
      `classic-ascii`
      
   - 通过选择不同的初始化参数，自动给类实例属性赋予不同的预设值，以此来达到不同的表格边框风格的目的。






3. #### 重置边框风格方法 - reset

    ------

    > 方法原型

     `reset()`

    - 将 Style 实例属性重置至默认属性。

    

    > 示例
    
    ```python
    mystyle = Style('simple')
    mystyle.reset()
    # 重置至默认的 table 风格。
    ```
    






4. #### 选择预置表格边框风格方法 - choose

    ------

    > 方法原型

    `choose(style)`

    - 选择预置的边框风格，参数 style 可用值与 Style 类初始化参数可用值一致。

    

    > 异常
    
    - 当 style 值不是有效值时触发 ValueError 异常。
    
    
    
    > 示例：
    
    ```python
    mystyle = Style('table')
    mystyle.choose('classic')
    # 将 mystyle 实例的边框风格属于改变为预置的 classic 风格。
    ```





5. #### 其他

    ------

    - 除了使用 choose 方法或选择不同的初始化参数来选择预置的表格边框风格外，还可以直接对类实例属性进行更改，以期达到更精确的定制化需求。
    - 直接修改类实例属性时值得注意的事项：a) 类实例属性值仅接受字符串类型数据；b) 类实例属性值并不限制字符数量，不限制字符宽度（例如字母和汉字的字符宽度就不一样），所以设置类实例属性时就需要用户自行注意不同属性需要同样的总字符宽度以实现表格边框的对齐，否则就会出现表格边框错位的情况。例如：当`center_cross`被设置为两个字母`oo`时，作为同一垂直方向线上的其他属性`top_cross`、`center_vert`、`bottom_cross`也都应该设置属性值为两个字母宽度的字符串；或某些属性设置为空字符串时，其他一些属性也要设置为空字符串，其他属性同理。
    - 后续可能会增加对属性值的自动限制。
    - 见目录下的 demo.py 文件。







- ### 最后
    ```
    # 表格中中文与英文混合使用时是否对齐与字体、运行的控制台类型有关
    # windows 平台上，程序输出于 cmd、PowerShell 时表格里无论中英文对齐都非常好
    # 以上终端（不限）建议把自动折行关掉，否则表格超过终端屏幕宽度时自动折行会使表格变成一团糟
    # IDLE、PyCharm 等 IDE 的自带终端中，中文基本上无法对齐
    # 这是第一个可用版本，BUG 比较多，功能也相对简单，后续会添加新功能
    # 文档写的也比较匆忙，可能错漏比较多，后续会不断修正
    # 因为源码经过好几次重构，所以函数文档基本都丢了还没有来得及重新写（已经写了的函数文档可能也有跟源码不对应的情况），后续提交会不断补上。
    ```
