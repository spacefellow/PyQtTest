import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QDir
import sys


class Widget(QtWidgets.QWidget):
    def __init__(self, dir_path, parent=None):
        super(Widget, self).__init__(parent)
        le = QtWidgets.QLineEdit(textChanged=self.on_textChanged)
        self._dirpath = dir_path

        self.file_model = QtWidgets.QFileSystemModel()
        self.file_model.setRootPath(self._dirpath)
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files | QDir.Hidden)
        self.proxy_model = QtCore.QSortFilterProxyModel(
            recursiveFilteringEnabled=True,
            filterRole=QtWidgets.QFileSystemModel.FileNameRole)
        self.proxy_model.setSourceModel(self.file_model)
        
        self.tree =  QtWidgets.QTreeView()
        self.tree.setModel(self.proxy_model)
        self.tree.setColumnWidth(500, 250)
        self.set_root_index()

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(le)
        lay.addWidget(self.tree)

    @QtCore.pyqtSlot(str)
    def on_textChanged(self, text):
        self.proxy_model.setFilterWildcard("*{}*".format(text))
        self.set_root_index()

    def set_root_index(self):
        root_index = self.file_model.index(self._dirpath)
        proxy_index = self.proxy_model.mapFromSource(root_index)
        self.tree.setRootIndex(proxy_index)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dirPath = os.path.expanduser('~')
    w = Widget(dirPath)
    w.show()
    sys.exit(app.exec_())
