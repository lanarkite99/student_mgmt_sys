import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel, QApplication, QWidget, QGridLayout, QLineEdit,
                             QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QComboBox)
from PyQt6.QtGui import QAction
import sys,sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item=self.menuBar().addMenu("&File")
        help_menu_item=self.menuBar().addMenu("&Help")
        edit_menu_item=self.menuBar().addMenu("&Edit")

        add_student_action=QAction("Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action=QAction("About",self)
        help_menu_item.addAction(about_action)

        search_student_action=QAction("Search",self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
    def load_data(self):
        connection=sqlite3.connect("database.db")
        result=connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for col_number,data in enumerate(row_data):
                self.table.setItem(row_number,col_number,QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog=InsertDialog()
        dialog.exec()

    def search(self):
        dialog=SearchDialog()
        dialog.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout()

        self.srch_name = QLineEdit()
        self.srch_name.setPlaceholderText("Name")
        layout.addWidget(self.srch_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_records(self):
        name=self.srch_name.text()
        # connection=sqlite3.connect("database.db")
        # cursor=connection.cursor()
        # result=cursor.execute(f"SELECT * FROM students WHERE name = ?",(name,))
        mainwindow.table.clearSelection()
        items=mainwindow.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            mainwindow.table.item(item.row(),1).setSelected(True)

        # cursor.close()
        # connection.close()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout()

        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        self.course_name.addItems(['Physics','Math','Biology','Astronomy'])
        layout.addWidget(self.course_name)

        self.mobile=QLineEdit()
        self.mobile.setPlaceholderText("Phone")
        layout.addWidget(self.mobile)

        submit_button=QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def add_student(self):
        name=self.student_name.text()
        course=self.course_name.itemText(self.course_name.currentIndex())
        mobile=self.mobile.text()
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (?,?,?)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        mainwindow.load_data()

app=QApplication(sys.argv)
mainwindow=MainWindow()
mainwindow.show()
mainwindow.load_data()
sys.exit(app.exec())

