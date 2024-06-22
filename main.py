import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel, QApplication, QWidget, QGridLayout, QLineEdit,
                             QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QComboBox, QToolBar,QStatusBar)
from PyQt6.QtGui import QAction, QIcon
import sys,sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)

        file_menu_item=self.menuBar().addMenu("&File")
        help_menu_item=self.menuBar().addMenu("&Help")
        edit_menu_item=self.menuBar().addMenu("&Edit")

        add_student_action=QAction(QIcon("icons/add.png"),"Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action=QAction("About",self)
        help_menu_item.addAction(about_action)

        search_student_action=QAction(QIcon("icons/search.png"),"Search",self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar=QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        self.status_bar=QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button=QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button=QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        if len(self.findChildren(QPushButton))==0:
            self.status_bar.addWidget(edit_button)
            self.status_bar.addWidget(delete_button)
        # if children:
        #     for child in children:
        #         self.status_bar.removeWidget(child)

        # self.status_bar.addWidget(edit_button)
        # self.status_bar.addWidget(delete_button)


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

    def edit(self):
        dialog=EditDialog()
        dialog.exec()

    def delete(self):
        dialog=DeleteDialog()
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

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Records")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout()

        index=mainwindow.table.currentRow()
        student_name=mainwindow.table.item(index,1).text()

        self.student_id=mainwindow.table.item(index,0).text()
        self.student_name=QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name=mainwindow.table.item(index,2).text()
        self.course_name = QComboBox()
        self.course_name.addItems(['Physics','Math','Biology','Astronomy'])
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile=mainwindow.table.item(index,3).text()
        self.mobile=QLineEdit(mobile)
        self.mobile.setPlaceholderText("Phone")
        layout.addWidget(self.mobile)

        submit_button=QPushButton("Submit")
        submit_button.clicked.connect(self.edit_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def edit_student(self):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        mainwindow.load_data()
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout()



app=QApplication(sys.argv)
mainwindow=MainWindow()
mainwindow.show()
mainwindow.load_data()
sys.exit(app.exec())

