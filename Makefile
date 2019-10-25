noDel:
	pyuic5 GUI/GUI_2.ui > GUI/GUI_2.py
	pyuic5 GUI/ajout_source.ui > GUI/ajout_source.py
	python3 main.py

clear:
	rm mainCol.json
	pyuic5 GUI/GUI_2.ui > GUI/GUI_2.py
	pyuic5 GUI/ajout_source.ui > GUI/ajout_source.py
	python3 main.py
