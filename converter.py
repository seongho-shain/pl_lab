import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import zipfile
import os
import shutil
import time

from Test.ReadFile import ReadFile
#from Test.JsonManager import JsonManager

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        path = []
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                path.extend(search(full_filename))
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.h':
                    print(full_filename)
                    path.append(full_filename.replace("\\", "/"))


    except PermissionError:
        pass

    return path

class MyWindow(QWidget):
    libPath = ""
    readFile = ReadFile()
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 400, 250)
        self.setWindowTitle("Arduino to mBlock Library Convertor v0.1")

        palette = QPalette()
        #palette.setColor(QPalette.Background, QColor(229, 68, 31))
        palette.setColor(QPalette.Background, QColor(255, 255, 255))

        self.setPalette(palette)

        self.openButton = QPushButton(self)
        self.openButton.clicked.connect(self.openButtonClicked)

        self.openButton.resize(398,100)
        self.openButton.move(1, 100)
        self.openButton.setIcon(QIcon('./image/zip.gif'))
        self.openButton.setIconSize(QSize(50, 50))
        self.openButton.setStyleSheet('background:#ffffff; border-style: outset; border-width: 2px; border-color: gray')

        self.title = QLabel("Arduino - Block library \n            System")
        self.title.resize(400, 70)
        self.title.move(50, 10)
        self.title.setStyleSheet("Color : black")
        self.title.setFont(QFont("Aerial", 20, QFont.Bold))

        self.label = QLabel()
        self.label.move(1, 100)
        self.label.resize(320, 100)
        self.label.setStyleSheet('background:#ffffff; border-style: outset; border-width: 2px; border-color: gray')
        self.label.setFont(QFont("Aerial", 10, QFont.Bold))
        self.label.setVisible(False)

        self.convertButton = QPushButton("Convert \nand\nSave")
        self.convertButton.clicked.connect(self.convertButtonClicked)
        self.convertButton.resize(80, 100)
        self.convertButton.move(320, 100)
        self.convertButton.setStyleSheet('background:#3d99f5; color: white; border-style: outset; border-width: 2px; border-color: gray')
        self.convertButton.setFont(QFont("Aerial", 11, QFont.Bold))
        self.convertButton.setVisible(False)



        ##

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.label)
        self.button_layout.addWidget(self.openButton)
        self.button_layout.addWidget(self.convertButton)
        self.button_layout.addWidget(self.title)

        self.button_layout.addStretch()

        self.grid = QGridLayout(self)

        self.grid.addLayout(self.button_layout, 0, 0)

        ##


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.openButton)
        layout.addWidget(self.convertButton)

        layout.addWidget(self.title)

        self.setLayout(layout)

    def openButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.openButton.setVisible(False)
        self.label.setVisible(True)
        self.convertButton.setVisible(True)
        self.label.setText("                변환할 아두이노  라이브러리 \n" + fname[0])

        archive = zipfile.ZipFile(fname[0], 'r')
        archive.extractall("./")
        archive.close()
        self.libPath = fname[0]


    def convertButtonClicked(self):
        filedir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # filename = QFileDialog.getSaveFileName(self, "Save File", "zip", "Zip File (*)")

        print("file : ", filedir)
        mlibDir = filedir + '/' + self.getLibFolderName() + "_m"
        print(self.getLibFolderName())
        headers = search('./' + self.getLibFolderName())
        for header in headers:
            self.readFile.setFile(header)
            self.readFile.run()
#여기부터 수정
            #mlibDir = filedir + '/' + self.getHeaderName(header) + "_m"
            self.makeDir(mlibDir)
            self.makeDir(mlibDir + '/' + 'src')
            self.makeDir(mlibDir + '/' + 'js')

            headerFileName = mlibDir + '/src/' + self.getHeaderName(header) + '.h'
            shutil.copy2(header, headerFileName)

            cppFileNameSrc = header[:-1]+"cpp"
            print("cpp : ", cppFileNameSrc)
            cppFileName = mlibDir + '/src/' + self.getHeaderName(header) + '.cpp'
            if os.path.isfile(cppFileNameSrc):
                shutil.copy2(cppFileNameSrc, cppFileName)

        #s2eFileName = mlibDir + '/' + self.getHeaderName(header) + '.s2e'
        s2eFileName = mlibDir + '/' + self.getLibFolderName() + '.s2e'

#추가
        jsFileName = mlibDir + '/js/' + 'sample.js'

        self.readFile.jsonManager.setExtensionName(self.getLibFolderName())

        self.readFile.save(s2eFileName, jsFileName)

        self.makeZip(mlibDir,mlibDir+'.zip')

        print("done")
        self.label.setText("변환 성공")
        shutil.rmtree(r""+mlibDir)

        #print(self.getLibFolderName())
        #shutil.rmtree(r"./"+self.getLibFolderName())

    def getHeaderName(self, str):
        return str.split('/')[-1].split('.')[0]

    def getLibFolderName(self):
        return self.libPath.split('/')[-1].split('.')[0]

    def makeDir(self, name):
        try:
            if not (os.path.isdir(name)):
                os.makedirs(os.path.join(name))
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                print("Failed to create directory!!!!!")
                self.label.setText("변환 실패")
                raise

    def makeZip(self, src_path, dest_file):
        with zipfile.ZipFile(dest_file, 'w') as zf:
            rootpath = src_path
            for (path, dir, files) in os.walk(src_path):
                for file in files:
                    fullpath = os.path.join(path, file)
                    relpath = os.path.relpath(fullpath, rootpath);
                    zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
            zf.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
