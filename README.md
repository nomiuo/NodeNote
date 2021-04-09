# 1. 使用说明

# 2. 需求分析

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
        painter.drawPixmap(self.rect(), QPixmap('Templates/snow1.png'), QRect())
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
        img_name = "Templates/girl.jpeg"
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
        img_name = "Templates/girl.jpeg"
        self.my_scene.set_background_img(img_name)
```

### 4. 新建`mainwindow_note_window.py`

1.实现主窗口基本UI配置

```python
    # 1. basic MainWindow UI setting
    def UI_MainWindow(self):
        self.setWindowIcon(QIcon('Templates/snow3.svg'))  # set icon
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
        left_btn_effect = QMovie("Templates/left_btn_effect.gif")

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
        left_btn_effect.frameChanged.connect(lambda frame_number: self.set_left_btn_beauty_down(
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

