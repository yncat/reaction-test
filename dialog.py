# -*- coding: utf-8 -*-
import Tkinter
import tkMessageBox

def dialog(title,message):
	root = Tkinter.Tk()
	root.withdraw()
	tkMessageBox.showinfo(title, message)
	root.quit()

