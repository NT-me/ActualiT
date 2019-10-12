all:
	rm mainCol.json
	pyuic5 GUI/mainwindow.ui > GUI/mainwindow.py
	python3 main.py
noDel:
	pyuic5 GUI/mainwindow.ui > GUI/mainwindow.py
	python3 main.py
