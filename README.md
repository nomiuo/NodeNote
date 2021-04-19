# 1. 使用说明

# 2. 需求分析

## 1. 界面UI设计

## 2. 笔记功能设计

### 1. 逻辑表示的完善

#### 1. 元素的完善

`属性互相限制`

1. 逻辑定义构成
    单位是其他元素的构成
    1. 常见的物理事物  
        - 特定的晨光橡皮擦
            - 第一种复合逻辑-分类形式: 橡皮套物质以及橡皮本体物质构成于
            - 第二种复合逻辑-分类形式: 由蓝色物质以及白色物质构成于
        - etc.
    2. 常见的定义事物
        - 特定的笛卡尔直角坐标系
            - 水平箭头线
            - 垂直箭头线
        - 锐角(其逻辑定义构成的位置描述其成为锐角)
            - A线
            - B线
        - etc.
2. 逻辑定义构成于
    即构成的元素
3. 逻辑定义位置
    - 绝对位置x
        - 关于绝对位置x描述的基本方式
            - 坐标系复合逻辑
            - 方向系复合逻辑
            - etc.
4. 逻辑定义数值
    以数学数字集合为基本单位
5. 逻辑定义时间
    - 绝对时间x
        - 关于绝对时间x描述的基本方式
            - 时间的基本单位: 铯-133 原子基态的两个超精细能级间跃迁辐射振荡 9192631770 周所持续的时间
            - 根据定义的1秒时间结合历法进制描述
            - etc.
6. 逻辑真值
    - 真
    - 假

#### 2. 基本逻辑的完善

1. 元逻辑
    - 产生限制逻辑 -> 针对于元素以及其的所有属性
    - 限制于逻辑 -> 针对于元素以及其的所有属性
    - 组合内部逻辑
        - 组合内部小于 -> 针对于逻辑定义数值
        - 组合内部等于 -> 针对于元素以及其的逻辑定义数值以及逻辑定义构成
        - 组合内部大于 -> 针对于逻辑定义数值
2. 复合逻辑
    - 分类逻辑 -> 针对于元素的所有属性
        将组合内部相同的元素属性合为一体
    - etc.

#### 3. 逻辑脑图展示的完善

![](README.assets/逻辑脑图.png)

### 2. 期望的界面表示逻辑

#### 1. 表示逻辑定义的办法

>   前提条件: a. 有些属性是不需要的属性  b. 有些属性在不同逻辑中是不同的  c. 构成元素的之间有逻辑关系

-   基本元素的组成
    基本元素由三个基本属性组成: 构成, 位置, 数值
    每个属性有两个基本描述: 真值, 时间

-   对于元素的基本属性可以考虑采用一条横框容纳, 左侧按钮为真值, 右侧标签为自定义时间

    每个基本属性有不同的横框区分
    属性的内容编辑采用Markdown并且要实现跳转超链接和图片和代码功能

-   对于元素可以考虑用一个大框表示, 同理左侧有真值, 右侧有自定义时间

-   多个属性可以容纳进一个元素, 多个元素可以容纳进另一个元素, 内部的布局要求内部关系也能体现采用珊格布局 3 * 3

#### 2. 基本逻辑的表示

-   针对有些元素逻辑之间比较复杂的处理办法
    1. '将有逻辑关系的元素之间放到一个树型结构中, 通过选中的办法实现复杂逻辑展示(如果有多个复杂逻辑冲突了怎么办)'
    2. '如果复杂逻辑中一个小逻辑断裂{即属性改变以适应其他逻辑}则该框不显示, 只有在点击目标逻辑时, 自动调整属性重新显示该框'
    3. 多个构成于如何处理: 采用逻辑克隆的办法
-   对于基本逻辑的展示(尝试采用QGraphicsItemGroup)
    1. 产生限制逻辑: 一个带文字和按钮的箭头, 文字用于描述, 按钮用于确定作用的是真还是假
    2. 限制于逻辑: 一个带文字和按钮的箭头, 文字用于描述, 按钮用于确定作用的是真还是假
    3. 组合内部逻辑: 并列的上下线条
-   自身真值为假所附带的线条为灰色

#### 3.其他添加的基本功能

1. 日历中的基本功能
    1. 每日计划
        1. todo列表
        2. 每日的期待
        3. 每日学习时间统计
    2. 日记
2. 构成中代码的运行
3. 共有内容的修改
4. 画板实现自定义图形绘制
5. 分页以及超链接跳转
6. 部分展示

## 3. life功能设计

### 1. 侧边栏分为2个模块

-   本月计划以及学习时间统计
-   项目模块以及学习时间统计

### 2. 操作过程

-   本月计划可以设置每日的计划
-   每日都可以设置想要记录的有趣事情的笔记内容
-   项目模块可以设置许多项目, 每个项目内容选择性移到本周计划的今日计划

### 3. 计划内容

-   类型: 学习, 娱乐, 项目名称
-   内容: 项目内容
-   开始时间
-   完成状态: 完成(用时), 未完成, 进行中

# 3. 开发过程

## 2020/04/08

>   完成下雪小部件前景的设置

### 1. 新建`component_snow_widget.py`

实现雪花图片的绘制

```python
class SnowWidget(QWidget):
    def __init__(self, parent=None):
        super(SnowWidget, self).__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap('Resources/snow1.png'), QRect())
```

### 2. 新建`component_sky_widget.py`

实现在空中飘落雪花的控制

```python
class SkyWidget(QWidget):
    timer = QTimer()

    def __init__(self, view_widget, parent=None):
        super(SkyWidget, self).__init__(parent)
        self.view_widget = view_widget
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.path_list = list()
        self.index = 0
        self.timer.timeout.connect(self.snow_create)
        self.timer.start(1000)

    def snow_create(self):
        # DEBUG
        if DEBUG:
            print("1-Debug:    snow_create function running")
        # create snow widget and its path
        snow_widget = SnowWidget(self)
        opacity_snow = QGraphicsOpacityEffect(snow_widget)
        run_path = QPropertyAnimation(snow_widget, b"pos")
        opacity_path = QPropertyAnimation(opacity_snow, b"opacity")
        self.path_list.append(QParallelAnimationGroup())
        self.snow_falling(snow_widget, run_path, opacity_path, self.path_list[self.index])
        self.index += 1

    def snow_falling(self, snow_widget, run_path, opacity_path, path_group):
        # DEBUG
        if DEBUG:
            print("2-Debug:    snow_falling function running")
        # pos and size
        start_x = random.randint(0, int(self.width()))
        start_y = random.randint(0, int(self.height()))
        random_size = random.randint(0, 9)
        width = 24 if random_size >= 6 else (18 if random_size >= 3 else 12)
        height = 24 if random_size >= 6 else (18 if random_size >= 3 else 12)
        snow_widget.setGeometry(start_x, start_y, width, height)
        snow_widget.setVisible(True)

        # fall speed
        fall_time_run_path = random.randint(25000, 30000)
        fall_time_opacity_path = random.randint(25000, 30000)
        run_path.setStartValue(QPoint(start_x, start_y))
        run_path.setEndValue(QPoint(start_x, self.height()))
        run_path.setDuration(fall_time_run_path)
        run_path.setEasingCurve(QEasingCurve.InOutCubic)
        opacity_path.setStartValue(1)
        opacity_path.setEndValue(0)
        opacity_path.setDuration(fall_time_opacity_path)
        path_group.addAnimation(run_path)
        path_group.addAnimation(opacity_path)

        # falling
        path_group.start()
        path_group.finished.connect(lambda: self.snow_end(snow_widget, path_group))

    def snow_end(self, snow_widget, path_group):
        sip.delete(snow_widget)
        self.index -= 1
        self.path_list.remove(path_group)
        if DEBUG:
            print("3-Debug:    delete snow widget successfully")
```

## 2020/04/09

>   实现背景的绘制

### 1. 新建`scene_view_my_view.py`

1.实现视图场景的配置

```python
class MyView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyView, self).__init__(parent)

        # function1: show scene
        self.scene = Scene()
        self.set_scene()

    def set_scene(self):
        self.setScene(self.scene.my_scene)
```

2.实现视图的美化

```python
    # function2: beauty
    def set_beauty(self):
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("border:0px;")
```

### 2. 新建`scene_view_my_scene.py`

1.实现背景图的绘制

```python
    def set_my_scene_background_img(self):
        img_name = "Resources/girl.jpeg"
        self.my_scene.set_background_img(img_name)
```

2.实现设置场景大小的接口

```python
    def set_my_scene_rect(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)
```

### 3. 新建`scene_view_scene.py`

1.实现场景的创建

```python
        self.my_scene = MyScene(self)
```

2.实现场景大小的设置

```python
    self.set_my_scene_rect()
    
    # set scene size
    def set_my_scene_rect(self):
        width = 64000
        height = 64000
        self.my_scene.set_my_scene_rect(width, height)
```

3.实现背景的设置

```python
    # 2. set scene background img
    def set_my_scene_background_img(self):
        img_name = "Resources/girl.jpeg"
        self.my_scene.set_background_img(img_name)
```

### 4. 新建`mainwindow_note_window.py`

1.实现主窗口基本UI配置

```python
    # 1. basic MainWindow UI setting
    def UI_MainWindow(self):
        self.setWindowIcon(QIcon('Resources/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QDesktopWidget().screenGeometry().width() - self.geometry().width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.geometry().height()) // 2
        )
```

2.实现视图和雪花的配置

```python
    # 2. basic Widget UI setting
    def UI_Widget(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.view_widget)
        self.central_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCentralWidget(self.central_widget)

    def resizeEvent(self, a0) -> None:
        self.sky_widget.resize(self.width(), self.height())
```

### 5. 修改`scene_view_my_view.py`

实现鼠标左键点击特效

```python
   # function3: left button beauty
    def set_left_btn_beauty(self, event):
        # set widget
        effect_container = QLabel(self)
        left_btn_effect = QMovie("Resources/left_btn_effect.gif")

        # set style
        effect_container.setScaledContents(True)
        effect_container.resize(150, 150)
        effect_container.move(int(event.pos().x() - effect_container.width() / 2),
                              int(event.pos().y() - effect_container.height() / 2))

        # set function
        effect_container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        effect_container.setMovie(left_btn_effect)
        left_btn_effect.start()
        effect_container.show()

        # set done
        left_btn_effect.frameChanged.connect(lambda frame_number: self.set_left_btn_beauty_done(
                                                        frame_number=frame_number,
                                                        left_btn_effect=left_btn_effect,
                                                        effect_container=effect_container))

    @staticmethod
    def set_left_btn_beauty_down(frame_number, left_btn_effect, effect_container):
        if frame_number == left_btn_effect.frameCount() - 1:
            effect_container.close()

    def mousePressEvent(self, event) -> None:
        super(MyView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_left_btn_beauty(event)
```

## 2020/04/10

### 1. 新建`component_todolist_widget`

实现todolist原型

```python
import os
import sqlite3
from PyQt5.QtCore import Qt, QDateTime, QDate
from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel, QVBoxLayout, QTextEdit, \
    QHeaderView, QTabWidget, QApplication, QDateTimeEdit, QPushButton, QComboBox, \
    QHBoxLayout, QAbstractItemView, QTableWidgetItem


class TodolistWidget(QWidget):
    def __init__(self, parent=None):
        super(TodolistWidget, self).__init__(parent)

        # function 1: ui
        self.table_title = QLabel("It is always morning somewhere in the world")
        self.table_widget = QTableWidget()
        self.table_tab = QTabWidget()
        self.time_select = QComboBox()
        self.status_select = QComboBox()
        self.type_select = QComboBox()
        self.time_widget = QDateTimeEdit(QDateTime.currentDateTime())
        self.commit = QPushButton("Commit")
        self.delete = QPushButton("Delete")
        self.text_edit = QTextEdit()
        self.show_time = QLabel("Have Learned For:")
        self.type_widget = QComboBox()
        self.design_ui()

        # function 2: create sql
        self.create_sql()

    # function1
    def design_ui(self):
        # layout
        todo_layout = QVBoxLayout()
        todo_layout.addWidget(self.table_title)
        todo_layout.addWidget(self.table_widget)
        todo_layout.addWidget(self.table_tab)
        self.setLayout(todo_layout)

        # label
        self.table_title.setAlignment(Qt.AlignCenter)

        # table
        self.table_widget.itemChanged.connect(self.edit_sql)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAutoScroll(True)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.resizeRowsToContents()
        self.table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:brown;}")
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(("id", "Type", "Todo", "From", "To", "Status"))
        self.table_widget.setColumnHidden(0, True)

        # tab
        #   tab1
        tab_data_layout = QVBoxLayout()
        tab_data_chose_layout = QHBoxLayout()
        tab_data_show_layout = QHBoxLayout()
        tab_data_widget = QWidget()
        tab_data_widget.setLayout(tab_data_layout)

        self.time_select.addItems(("Today", "This Week", "This Month", "This Year", "All"))
        self.status_select.addItems(("Incomplete", "In Progress", "Done"))
        self.type_select.addItems(("Study", "Favourite"))
        self.time_select.currentTextChanged.connect(self.search)
        self.status_select.currentTextChanged.connect(self.search)
        self.type_select.currentTextChanged.connect(self.search)
        tab_data_chose_layout.addWidget(QLabel("Search:"))
        tab_data_chose_layout.addWidget(self.type_select)
        tab_data_chose_layout.addWidget(self.time_select)
        tab_data_chose_layout.addWidget(self.status_select)
        tab_data_layout.addLayout(tab_data_chose_layout)

        tab_data_show_layout.addWidget(self.show_time)
        tab_data_layout.addLayout(tab_data_show_layout)
        self.table_tab.addTab(tab_data_widget, "Task info")
        #   tab2
        tab_task_layout = QVBoxLayout()
        tab_task_widget = QWidget()

        tab_task_type_layout = QHBoxLayout()
        self.type_widget.addItems(("Study", "Favourite"))
        tab_task_type_layout.addWidget(QLabel("Type"))
        tab_task_type_layout.addWidget(self.type_widget)
        tab_task_layout.addLayout(tab_task_type_layout)

        tab_task_layout.addWidget(QLabel("Task Description"))
        tab_task_layout.addWidget(self.text_edit)

        tab_task_from_layout = QHBoxLayout()
        tab_task_from_layout.addWidget(QLabel("From"))
        self.time_widget.setCalendarPopup(True)
        self.time_widget.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        tab_task_from_layout.addWidget(self.time_widget)
        tab_task_layout.addLayout(tab_task_from_layout)

        self.commit.clicked.connect(self.add_sql)
        tab_task_btn_layout = QHBoxLayout()
        tab_task_btn_layout.addWidget(self.commit)
        tab_task_btn_layout.addWidget(self.delete)
        self.delete.clicked.connect(self.del_sql)
        tab_task_layout.addLayout(tab_task_btn_layout)

        tab_task_widget.setLayout(tab_task_layout)
        self.table_tab.addTab(tab_task_widget, "Add New Task")

    # function2
    def create_sql(self):
        cwd_path = os.getcwd()
        if not os.path.exists('todolist.db'):
            connect_sql = sqlite3.connect(cwd_path + r'/todolist.db')
            cursor_sql = connect_sql.cursor()
            cursor_sql.execute('''create table learntime(
                                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                `Type` varchar (1000),
                                `Time` varchar (1000)  
                                );
                                ''')

            cursor_sql.execute('''create table todolist(
                                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                                'Type'   varchar (1000),
                                'Todo'   varchar (1000),
                                'From'   INTEGER ,
                                'To'     INTEGER,
                                'Status' varchar (1000)
                                );
                                ''')

            connect_sql.commit()
            connect_sql.close()
        else:
            self.flush_table()

    # function3: flush table
    def flush_table(self, Type=None, Time=None, Status=None):
        # get data
        connect_sql = sqlite3.connect('todolist.db')
        cursor_sql = connect_sql.cursor()
        if Type is None and Time is None and Status is None:
            data = cursor_sql.execute('select * from todolist')
        else:
            today = QDate.currentDate().toString("yyyy-MM-dd")
            if self.time_select.currentText() == "Today":
                data = cursor_sql.execute("""select * from todolist where `Type`=%s and `Status`=%s and date(%s) = date('now')""" % (
                                            self.type_select.currentText(),
                                            self.status_select.currentText(),
                                            today
                                            ))
        data_list = list()
        for row in data:
            temp_list = list()
            temp_list.append(row[0])
            temp_list.append(row[1])
            temp_list.append(row[2])
            temp_list.append(row[3])
            temp_list.append(row[4])
            temp_list.append(row[5])
            data_list.append(temp_list)
        cursor_sql.close()

        self.table_widget.setRowCount(len(data_list))
        for index in range(len(data_list)):
            self.table_widget.setItem(index, 0, QTableWidgetItem(str(data_list[index][0])))
            self.table_widget.setItem(index, 1, QTableWidgetItem(str(data_list[index][1])))
            self.table_widget.setItem(index, 2, QTableWidgetItem(str(data_list[index][2])))
            self.table_widget.setItem(index, 3, QTableWidgetItem(str(data_list[index][3])))
            self.table_widget.setItem(index, 4, QTableWidgetItem(str(data_list[index][4])))
            self.table_widget.setItem(index, 5, QTableWidgetItem(str(data_list[index][5])))

    # function4: add information
    def add_sql(self):
        if self.text_edit.toPlainText() != '':
            connect_sql = sqlite3.connect("todolist.db")
            cursor_sql = connect_sql.cursor()
            time = self.time_widget.dateTime().toString(self.time_widget.displayFormat())
            cursor_sql.execute('''insert into todolist values(null,'%s', '%s', '%s', null, '%s')''' %
                               (str(self.type_widget.currentText()),
                                str(self.text_edit.toPlainText()),
                                time,
                                "Incomplete"))
            connect_sql.commit()
            connect_sql.close()

            self.type_widget.setCurrentIndex(0)
            self.text_edit.clear()
            self.time_widget.setDateTime(QDateTime.currentDateTime())
            self.flush_table()

    # function5: edit information
    def edit_sql(self, item):
        row = item.row()
        column = item.column()
        Id = self.table_widget.item(row, 0).text()
        data = self.table_widget.item(row, column).text()

        connect_sql = sqlite3.connect("todolist.db")
        cursor_sql = connect_sql.cursor()
        cursor_sql.execute("update todolist set `%s`='%s' where `id`='%s'" % (
            self.table_widget.horizontalHeaderItem(column).text(), data, Id))
        connect_sql.commit()
        connect_sql.close()

    # function6: del information
    def del_sql(self):
        selected_row = self.table_widget.selectedItems()
        if len(selected_row) == 5:
            del_row = self.table_widget.row(selected_row[0])
            Id = self.table_widget.item(del_row, 0).text()

            connect_sql = sqlite3.connect("todolist.db")
            cursor_sql = connect_sql.cursor()
            cursor_sql.execute("delete from todolist where `id`=%s" % Id)
            connect_sql.commit()
            connect_sql.close()
        self.flush_table()

    # function7: search
    def search(self):
        Type = self.type_select.currentText()
        From = self.time_select.currentText()
        Status = self.status_select.currentText()

        self.flush_table(Type, From, Status)


if __name__ == '__main__':
    app = QApplication([])
    window = TodolistWidget()
    window.show()
    app.exec_()

```

## 2020/04/11

尝试采用`QGraphicsView`实现`Todolist`, 暂时不实现

## 2020/04/12

**实现鼠标左键动态特效优化**, (参考博客水滴博客)
创建`component_water.py`

```python
class Water(QWidget):
    def __init__(self, parent=None):
        super(Water, self).__init__(parent)

        # water ui
        self.water_color = QColor("#FF6699FF")
        self.circle_big_size = 10.0
        self.circle_small_size = 0.0
        self.design_ui()

        # water animation
        self.water_animation = QVariantAnimation(self)

    def design_ui(self):
        self.setFixedSize(QSize(int(self.circle_big_size * 2), int(self.circle_big_size * 2)))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def move(self, a0) -> None:
        true_pos = a0 - QPoint(int(self.circle_big_size), int(self.circle_big_size))
        super(Water, self).move(true_pos)

    def show(self):
        super(Water, self).show()
        self.water_animation.setStartValue(0.0)
        self.water_animation.setEndValue(self.circle_big_size)
        self.water_animation.setDuration(350)
        self.water_animation.valueChanged.connect(self.circle_repaint)
        self.water_animation.finished.connect(self.close)
        self.water_animation.start()

    def circle_repaint(self, value):
        self.circle_small_size = value
        self.update()

    def paintEvent(self, a0) -> None:
        # painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.water_color))
        # paint two circle
        big_circle = QPainterPath()
        big_circle.addEllipse(QPointF(self.circle_big_size, self.circle_big_size),
                              self.circle_big_size, self.circle_big_size)
        small_circle = QPainterPath()
        small_circle.addEllipse(QPointF(self.circle_big_size, self.circle_big_size),
                                self.circle_small_size, self.circle_small_size)
        circle = big_circle - small_circle
        painter.drawPath(circle)
```

修改`mainwindow_note_window.py`鼠标左键事件实现点击特效

```python
    # 3. left button beauty
    def mousePressEvent(self, a0) -> None:
        super(NoteWindow, self).mousePressEvent(a0)
        if a0.button() == Qt.LeftButton:
            water_drop = Water(self.central_widget)
            water_drop.move(self.mapToGlobal(a0.pos()))
            water_drop.show()
```

## 2020/04/17

-   优化水滴特效将其作为代理插入场景中去除黑边框
-   在`linux-manjaro`测试下发现普通核显存在卡顿情况, 在启动`英威达MX150`后正常运行

架构研究

-   基本控件的创建
    -   节点
        -   属性节点
        -   子节点
    -   端口
    -   线条
-   程序基本框架
    -   