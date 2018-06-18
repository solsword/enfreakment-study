.PHONY: default
default: report.txt

%-workers.lst: %.csv
	grep -v Rejected $< | cut -d'"' -f32 | tail -n+2 > $@

batches/makeup.lst: batches/makeup-*
	cat $^ | grep -v WorkerId | cut -d"	" -f1 > $@

participants.lst: batches/batch-1-workers.lst batches/batch-2-workers.lst batches/batch-3-workers.lst batches/batch-4-workers.lst batches/makeup.lst
	cat $^ | sort | uniq -c | sort > $@

pids.tsv: participants.lst Makefile
	echo "id	submissions	worker_id" > pids.tsv
	awk '{ print FNR "\t" $$1 "\t" $$2; }' < participants.lst >> pids.tsv

batches/filtered-batch-%.csv: batches/batch-%.csv Makefile
	grep -v Rejected $< \
		| grep -vf reject.lst \
		| sed "s/\\r$$//" \
		| tr "\\r" " " \
		| sed "/^$$/d" \
		| sed "s/Answer.identification_/Answer.similarity_/g" \
		> $@

batches/full-makeup-%.tsv: batches/makeup-%.tsv
	sed "1s/\t/\tAnswer./g" $< > $@

.PHONY: jump
jump: batches/filtered-batch-2.csv batches/filtered-batch-3.csv batches/filtered-batch-4.csv batches/full-makeup-1.tsv batches/full-makeup-2.tsv batches/full-makeup-3.tsv batches/full-makeup-4.tsv

efr.tsv: jump batches/filtered-batch-*.csv jump batches/full-makeup-*.tsv pids.tsv process.py
	./process.py batches/filtered-batch-*.csv batches/full-makeup-*.tsv > efr.tsv

genders.lst: efr.tsv
	cut -d"	" -f23 efr.tsv | tail -n +2 | sort | uniq > genders.lst

ethnicities.lst: efr.tsv
	cut -d"	" -f25 efr.tsv | tail -n +2 | sort | uniq > ethnicities.lst

nationalities.lst: efr.tsv
	cut -d"	" -f27 efr.tsv | tail -n +2 | sort | uniq > nationalities.lst

efr-aug.tsv: efr.tsv reprocess.py
	./reprocess.py < efr.tsv > efr-aug.tsv

efr-aug-grp.json: efr-aug.tsv group.py framedata.py properties.py
	./group.py < efr-aug.tsv > efr-aug-grp.json

report.txt: efr-aug-grp.json analyze.py
	./analyze.py < efr-aug-grp.json > report.txt

.PHONY: clean
clean:
	rm -f efr.tsv efr-aug.tsv efr-aug-grp.json
