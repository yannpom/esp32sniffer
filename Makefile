all:
	(unset IDF_PATH; source ~/esp/idf-master/export.sh; idf.py build | sed 's@\.\./@@')
