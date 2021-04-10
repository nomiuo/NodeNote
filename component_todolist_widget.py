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
