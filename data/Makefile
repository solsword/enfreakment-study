.PHONY: default
default: report.txt

combined.csv: batches/batch-2.csv batches/batch-3.csv Makefile
	cat batches/batch-2.csv > combined.csv
	echo >> combined.csv
	tail -n +2 batches/batch-3.csv >> combined.csv

filtered.csv: combined.csv reject.lst
	cat combined.csv \
		| grep -v Rejected \
		| grep -vf reject.lst \
		| sed "s/\\r$$//" \
		| tr "\\r" " " \
		| sed "/^$$/d" \
		> filtered.csv

extras.csv: batches/makeup.tsv
	sed "1s/\t/\tAnswer./g" batches/makeup.tsv \
		| sed "s/\t/\",\"/g" \
		| sed "s/^/\"/" \
		| sed "s/$$/\"/" \
		> extras.csv

efr.tsv: filtered.csv extras.csv process.py
	./process.py filtered.csv extras.csv > efr.tsv

ethnicities.lst: efr.tsv
	cut -d"	" -f24 efr.tsv | tail -n +2 | sort | uniq > ethnicities.lst

nationalities.lst: efr.tsv
	cut -d"	" -f26 efr.tsv | tail -n +2 | sort | uniq > nationalities.lst

efr-aug.tsv: efr.tsv reprocess.py
	./reprocess.py < efr.tsv > efr-aug.tsv

efr-aug-grp.json: efr-aug.tsv group.py
	./group.py < efr-aug.tsv > efr-aug-grp.json

report.txt: efr-aug-grp.json analyze.py
	./analyze.py < efr-aug-grp.json > report.txt

.PHONY: clean
clean:
	rm -f combined.csv filtered.csv extras.csv extras.tsv efr.tsv efr-aug.tsv efr-aug-grp.json
