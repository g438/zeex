# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:45:23 2016

MIT License

Copyright (c) 2016 Zeke Barge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
from zeex.core.compat import QtGui, QtCore


def configure_combo_box(box: QtGui.QComboBox, options, default, clear=True):
    if clear and box.count() > 0:
        box.clear()
    if not isinstance(options, list):
        options = list(options)
    box.addItems(options)
    idx = box.findText(default)
    if idx >= 0:
        box.setCurrentIndex(idx)
    return box


def create_standard_item_model(columns: list = None, editable=False, checkable=False):
        if columns is None:
            columns = []
        elif not isinstance(columns, list):
            columns = list(columns)
        model = QtGui.QStandardItemModel()
        for idx, col in enumerate(columns):
            item = create_standard_item(col, editable, checkable)
            model.appendRow(item)
        return model


def create_standard_item(name, editable=False, checkable=False):
    item = QtGui.QStandardItem(str(name))
    item.setEditable(editable)
    item.setCheckable(checkable)
    return item


def ensure_modeled(item: (str, list, QtGui.QStandardItemModel)):
    if isinstance(item, str):
        item = [item]
    if hasattr(item, "__iter__"):
        item = create_standard_item_model(item)
    elif not hasattr(item, "rowCount"):
        raise NotImplementedError("unable to convert item of type {} to QStandardItemModel".format(type(item)))
    return item


def get_ok_msg_box(parent, msg, title='Message!'):
    msgBox = QtGui.QMessageBox(parent)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    return msgBox


def shift_grid_layout_down(layout):
    # TODO: Make this legit?
    col_range = range(layout.columnCount())
    row_range = range(layout.rowCount())
    print(layout.columnCount())
    print(layout.rowCount())
    temp = []

    for row_idx in row_range:
        items = [layout.itemAtPosition(row_idx, col_idx)
                 for col_idx in col_range]
        temp.append(items)
    temp.insert(0, [i for i in temp[0]])
    print("got temp")
    for row_idx, items in enumerate(temp):
        print("working row {}".format(row_idx))
        for col_idx, item in enumerate(items):
            print("working column {}".format(col_idx))
            if item is not None:
                layout.addWidget(item)
    print("redid layout")
    print(layout.columnCount())
    print(layout.rowCount())
    return layout


def table_push_item_up(view):
    model = view.model()
    for idx in view.selectedIndexes():
        row = idx.row()
        if row > 0:
            model.insertRow(row-1)
            for i in range(model.columnCount()):
                model.setItem(row - 1, i, model.takeItem(row + 1, i))
            model.takeRow(row+1)
            view.setCurrentIndex(model.item(row - 1, 0).index())


def table_push_item_down(view):
    model = view.model()
    for idx in view.selectedIndexes():
        row = idx.row()
        if row < model.rowCount()-1:
            model.insertRow(row+2)
            for i in range(model.columnCount()):
                model.setItem(row+2, i, model.takeItem(row,i))
            model.takeRow(row)
            view.setCurrentIndex(model.item(row + 1, 0).index())


def signal_adjust(signal, newhandler=None, oldhandler=None):
    while True:
        try:
            if oldhandler is not None:
                signal.disconnect(oldhandler)
            else:
                signal.disconnect()
        except (RuntimeError, TypeError):
            break
    if newhandler is not None:
        signal.connect(newhandler)


def triggered_adjust(item, newhandler=None, oldhandler=None):
    while True:
        try:
            if oldhandler is not None:
                item.triggered.disconnect(oldhandler)
            else:
                item.triggered.disconnect()
        except (RuntimeError, TypeError):
            break
    if newhandler is not None:
        item.triggered.connect(newhandler)


def activated_adjust(item, newhandler=None, oldhandler=None):
    while True:
        try:
            if oldhandler is not None:
                item.activated.disconnect(oldhandler)
            else:
                item.activated.disconnect()
        except (RuntimeError, TypeError):
            break
    if newhandler is not None:
        item.activated.connect(newhandler)


def combo_box_append(box, value, select=True):
    value = str(value)
    match = box.findText(value)
    if match >= 0:
        if select:
            box.setCurrentIndex(match)
    else:
        box.addItem(value)
        combo_box_append(box, value, select)
    return box


