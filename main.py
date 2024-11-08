import math
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication,QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont
from decimal import Decimal
from qt_material import apply_stylesheet


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        apply_stylesheet(app, theme='light_purple.xml')
        self.history_list = []
        self.num1 = 0
        self.num2 = 0
        self.oldAction = None
        self.actionBeforeAction = False
        self.actionBeforeAction2 = False
        self.Equally_bool = False
        self.setStyleSheet("background: #e3e3e3")
        self.setWindowTitle("Калькулятор")
        self.setBaseSize(430,530)
        self.labelHistory = QtWidgets.QLabel()

        self.labelHistory.setStyleSheet("color: #696969; font-size:23px;")
        # self.labelHistory.setFixedSize(420,50)
        self.textBox = QtWidgets.QLineEdit()
        self.textBox.setReadOnly(True)
        self.textBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textBox.setText('0')
        self.textBox.setAlignment(QtCore.Qt.AlignRight)
        self.textBox.setBaseSize(405, 70)
        self.textBox.setStyleSheet("color: black; font-size:40px;")
        self.btn_proc = QtWidgets.QPushButton("%")
        self.btn_CE = QtWidgets.QPushButton("CE")
        self.btn_C = QtWidgets.QPushButton("C")
        self.btn_del = QtWidgets.QPushButton("del")
        self.btn0 = QtWidgets.QPushButton("0")
        self.btn1 = QtWidgets.QPushButton("1")
        self.name = self.btn1.text()
        self.btn2 = QtWidgets.QPushButton("2")
        self.btn3 = QtWidgets.QPushButton("3")
        self.btn4 = QtWidgets.QPushButton("4")
        self.btn5 = QtWidgets.QPushButton("5")
        self.btn6 = QtWidgets.QPushButton("6")
        self.btn7 = QtWidgets.QPushButton("7")
        self.btn8 = QtWidgets.QPushButton("8")
        self.btn9 = QtWidgets.QPushButton("9")
        self.btn_plus = QtWidgets.QPushButton("+")
        self.btn_minus = QtWidgets.QPushButton("-")
        self.btn_umn = QtWidgets.QPushButton("*")
        self.btn_div = QtWidgets.QPushButton("/")
        self.btn_power = QtWidgets.QPushButton("x2")
        self.btn_sqrt = QtWidgets.QPushButton("√x")
        self.btn_dot = QtWidgets.QPushButton(",")
        self.btn_1_del_x = QtWidgets.QPushButton("1/x")
        self.btn_ravno = QtWidgets.QPushButton("=")
        self.btn_change = QtWidgets.QPushButton("+/-")
        self.btn_history = QtWidgets.QPushButton("i")
        self.buttons = [self.btn_proc, self.btn_CE, self.btn_C,self.btn_del,
                   self.btn_1_del_x, self.btn_power,self.btn_sqrt,self.btn_div,
                   self.btn7, self.btn8,self.btn9,self.btn_umn,
                   self.btn4,self.btn5,self.btn6,self.btn_minus,
                   self.btn1,self.btn2,self.btn3, self.btn_plus,
                   self.btn_change,self.btn0,self.btn_dot,self.btn_ravno]
        self.buttonsAllAction = [self.btn_plus,self.btn_minus,self.btn_div,self.btn_umn, self.btn_power,self.btn_sqrt, self.btn_dot, self.btn_ravno, self.btn_change,self.btn_1_del_x,self.btn_proc]
        buttonsNums = [self.btn0,self.btn1,self.btn2,self.btn3,self.btn4,self.btn5,self.btn6,
                       self.btn7,self.btn8,self.btn9]
        buttonsEasyActions =[self.btn_plus,self.btn_minus,self.btn_div,self.btn_umn]
        self.numbers_dict = {self.btn1: "1", self.btn2: "2", self.btn3: "3", self.btn4: "4", self.btn5: "5",
                             self.btn6: "6", self.btn7: "7", self.btn8: "8", self.btn9: "9", self.btn0: "0"}
        self.znaki_dict = {self.btn_plus: "+", self.btn_minus: "-", self.btn_umn: "*", self.btn_div: "/"}


        self.grid_tools = QtWidgets.QGridLayout()
        self.grid_tools.addWidget(self.labelHistory, 0,0,1,4)
        self.btn_history.setFixedSize(40,40)
        self.btn_history.clicked.connect(self.show_info_messagebox)
        self.grid_tools.addWidget(self.btn_history, 0,0,1,1)
        self.labelHistory.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.grid_tools.addWidget(self.textBox, 1,0,1,4)
        count_row = 2;
        count_column = 0
        for i in self.buttons:
            if count_column == 4:
                count_column = 0
                count_row+=1
            i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            i.setBaseSize(97, 60)
            i.setStyleSheet("font-size: 16pt;")
            self.grid_tools.addWidget(i,count_row,count_column)
            count_column+=1

        main_vbox = QtWidgets.QVBoxLayout()
        main_vbox.addLayout(self.grid_tools)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_vbox)
        self.setCentralWidget(main_widget)
        for i in buttonsNums:
            i.clicked.connect(self.addNum)
        for i in buttonsEasyActions:
            i.clicked.connect(self.addHistory)
        self.btn_C.clicked.connect(self.clear_all)
        self.btn_CE.clicked.connect(self.clear_tb)
        self.btn_dot.clicked.connect(self.addDot)
        self.btn_power.clicked.connect(self.Pow)
        self.btn_sqrt.clicked.connect(self.Sqrt)
        self.btn_1_del_x.clicked.connect(self.oneDivNum)
        self.btn_ravno.clicked.connect(self.Equally)
        self.btn_proc.clicked.connect(self.Percentage)
        self.btn_change.clicked.connect(self.ChangeSign)
        self.btn_del.clicked.connect(self.DeleteLastChar)
    def DeleteLastChar(self) -> None:
        self.actionBeforeAction = False
        self.textBox.setText(self.textBox.text()[:-1])
        if self.textBox.text() == "" or  self.textBox.text() == "-":
            self.textBox.setText("0")
    def ChangeSign(self)-> None:
        self.actionBeforeAction2 = False
        self.actionBeforeAction = False

        if self.textBox.text().__contains__('-'):
            self.textBox.setText(self.textBox.text()[1:])
        elif self.textBox.text()!= '0':
            self.textBox.setText('-'+self.textBox.text())
        if self.Equally_bool is True:
            self.num1 = self.getNum(self.textBox.text())

    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        text=''
        for i in self.history_list:
            text += i+"\n"
            msg.setText(text)
        msg.setWindowTitle("История действий")
        retval = msg.exec_()
    def Percentage(self) -> None:
        if not self.labelHistory.text():
            self.textBox.setText('0')
            return
        self.Equally_bool = False
        self.actionBeforeAction = False
        self.actionBeforeAction2 = True
        self.num1 = self.getNum(self.labelHistory.text().split(' ')[0])
        self.num2 = self.getNum(self.textBox.text())
        self.num2 = self.num1*self.num2/100
        self.num2 = self.zeroTrimming(self.num2)
        self.textBox.setText(str(self.num2))

    def Equally(self):

        if not self.labelHistory.text() or self.labelHistory.text().split(' ')[-1] == "=":
            self.labelHistory.setText(self.textBox.text() + " =")
            return
        lastznak = self.labelHistory.text().split(' ')[1]
        if lastznak == "=":
            return
        if self.Equally_bool is False:
            self.num1 = self.getNum(self.labelHistory.text().split(' ')[0])
            self.num2 = self.getNum(self.textBox.text())
        self.Equally_bool = True
        self.labelHistory.setText(str(self.num1)+" "+lastznak + " " + str(self.num2)+" = ")
        self.Calculation()
        self.actionBeforeAction = True
        self.actionBeforeAction2 = True


    def oneDivNum(self) -> None:
        self.Equally_bool = False
        self.actionBeforeAction = False
        self.num1 = self.getNum(self.textBox.text())
        self.actionBeforeAction2 = True
        if self.num1 == 0:
            self.textBox.setText("Ошибка")
            self.labelHistory.setText('')
            for i in self.buttonsAllAction:
                i.setEnabled(False)
            self.num1 = 0
            self.num2 = 0
            return
        self.num1 = 1/self.num1
        self.num1 = Decimal(str(self.num1))
        self.num1 = self.zeroTrimming(self.num1)
        self.textBox.setText(str(self.num1))

    def Sqrt(self) -> None:
        self.Equally_bool = False
        self.actionBeforeAction = False

        self.num1 = self.getNum(self.textBox.text())
        self.num1 = math.sqrt(self.num1)
        self.num1 = Decimal(str(self.num1))
        self.num1 = self.zeroTrimming(self.num1)
        self.textBox.setText(str(self.num1))
        self.actionBeforeAction2 = True
        if self.textBox.text().lower() == "infinity":
            for i in self.buttonsAllAction:
                i.setEnabled(False)

    def Pow(self) -> None:
        self.Equally_bool = False
        self.actionBeforeAction = False
        self.num1 = self.getNum(self.textBox.text())
        try:
            self.num1 = math.pow(self.num1,2)
            self.num1 = Decimal(str(self.num1))
            self.num1 = self.zeroTrimming(self.num1)
            self.textBox.setText(str(self.num1))

            self.actionBeforeAction2 = True
        except OverflowError:
            self.textBox.setText("Переполнение")
            for i in self.buttonsAllAction:
                i.setEnabled(False)

    def addHistory(self) -> None:
        newAction = self.sender()
        if self.actionBeforeAction == True or not self.labelHistory.text():
            self.labelHistory.setText(self.textBox.text() + " " + newAction.text())
        else:
            self.Calculation()
            self.labelHistory.setText(str(self.num1)+" "+newAction.text())
        self.actionBeforeAction = True
    def Calculation(self) -> None:
        self.actionBeforeAction = False
        self.actionBeforeAction2 = False
        if self.Equally_bool is False:
            self.num1 = self.getNum(self.labelHistory.text().split(' ')[0])
            self.num2 = self.getNum(self.textBox.text())

        action = self.labelHistory.text().split(' ')[1]
        text = str(self.num1) + f" {action} " + str(self.num2) + " = "
        if action == '+':
            self.num1 = self.num1+self.num2
        elif action == '-':
            self.num1 = self.num1-self.num2
        elif action == '*':
            self.num1 = self.num1*self.num2
        elif action == '/':
            if self.num2==0:
                self.textBox.setText("Ошибка")
                self.labelHistory.setText('')
                for i in self.buttonsAllAction:
                    i.setEnabled(False)
                self.num1 = 0
                self.num2 = 0
                return
            self.num1 = self.num1/self.num2

        self.num1 = self.zeroTrimming(self.num1)
        self.textBox.setText(str(self.num1))
        text +=str(self.num1)
        self.history_list.append(text)

    def zeroTrimming(self, num:int | Decimal) -> int|Decimal:
        if str(num).endswith('.0'):
            return int(num)
        else:
            return Decimal(str(num))

    def getNum(self, num: str)-> int|Decimal:
        if "." in num:
            return Decimal(num)
        else:
            return int(num)


    @QtCore.pyqtSlot()
    def addNum(self):
        for i in self.buttonsAllAction:
            i.setEnabled(True)
        num = self.sender()
        self.Equally_bool = False
        if self.textBox.text() == '0' or self.textBox.text() == "Ошибка" or self.textBox.text() == "Переполнение" or self.textBox.text().lower() == "infinity":

            self.textBox.setText(num.text())
        else:
            if self.actionBeforeAction == True or self.actionBeforeAction2 == True:
                self.textBox.setText("")
                self.actionBeforeAction = False
                self.actionBeforeAction2 = False
                self.textBox.setText(self.textBox.text() + num.text())
            else:
                self.textBox.setText(self.textBox.text() + num.text())

    def clear_all(self):
        for i in self.buttonsAllAction:
            i.setEnabled(True)
        self.num1 = 0
        self.num2 = 0
        self.textBox.setText("0")
        self.labelHistory.clear()
        self.actionBeforeAction = False
        self.actionBeforeAction2 = False
        self.Equally_bool = False

    def clear_tb(self):
        self.num1 = 0;
        for i in self.buttonsAllAction:
            i.setEnabled(True)
        self.textBox.setText("0")
    def addDot(self):
        self.actionBeforeAction =  False
        if "." not in self.textBox.text() :
            self.actionBeforeAction2 = False
            self.textBox.setText(self.textBox.text()+'.')
    def resizeEvent(self, event):
        fontSizeText = self.height() // 12
        fontSizeButton = self.height() // 22
        for i in self.buttons:
            i.setStyleSheet(f"font-size: {fontSizeButton}pt;")
        self.textBox.setStyleSheet(f"font-size: {fontSizeText}pt;")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Calculator()
    window.show()
    app.exec()
