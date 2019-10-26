noDel:
	pyuic5 GUI/GUI_2.ui > GUI/GUI_2.py
	pyuic5 GUI/ajout_source.ui > GUI/ajout_source.py
	pyuic5 GUI/NACManageDialog.ui > GUI/NACManageDialog.py
	python3 main.py

clear:
	rm mainCol.json
	rm GUI/*.py
	pyuic5 GUI/GUI_2.ui > GUI/GUI_2.py
	pyuic5 GUI/ajout_source.ui > GUI/ajout_source.py
	python3 main.py
