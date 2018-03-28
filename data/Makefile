.PHONY: default
default: efr-aug-grp.json

efr.tsv: enfreakment_results.csv
	./process.py < enfreakment_results.csv > efr.tsv

efr-aug.tsv: efr.tsv
	./reprocess.py < efr.tsv > efr-aug.tsv

efr-aug-grp.json: efr-aug.tsv
	./group.py < efr-aug.tsv > efr-aug-grp.json

.PHONY: clean
clean:
	rm efr.tsv efr-aug.tsv efr-aug-grp.json
