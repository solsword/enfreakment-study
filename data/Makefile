.PHONY: default
default: report.txt

efr.tsv: enfreakment_results.csv process.py
	./process.py < enfreakment_results.csv > efr.tsv

efr-aug.tsv: efr.tsv reprocess.py
	./reprocess.py < efr.tsv > efr-aug.tsv

efr-aug-grp.json: efr-aug.tsv group.py
	./group.py < efr-aug.tsv > efr-aug-grp.json

report.txt: efr-aug-grp.json analyze.py
	./analyze.py < efr-aug-grp.json > report.txt

.PHONY: clean
clean:
	rm efr.tsv efr-aug.tsv efr-aug-grp.json
