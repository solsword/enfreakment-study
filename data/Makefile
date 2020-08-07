.DEFAULT_GOAL=tables-100.tex

%-workers.lst: %.csv
	grep -v Rejected $< | cut -d'"' -f32 | tail -n+2 > $@

#batches/makeup.lst: batches/makeup-*
#	cat $^ | grep -v WorkerId | cut -d"	" -f1 > $@

#participants.lst: batches/batch-1-workers.lst batches/batch-2-workers.lst batches/batch-3-workers.lst batches/makeup.lst
participants.lst: batches/batch-1-workers.lst batches/batch-2-workers.lst batches/batch-3-workers.lst batches/pilot-1-workers.lst batches/pilot-2-workers.lst
	cat $^ | sort | uniq -c | sort > $@

# Filter out workers from the pilots and workers with multiple submissions
reject.lst: participants.lst batches/pilot-1-workers.lst batches/pilot-2-workers.lst find_holy.py
	cat batches/pilot-*-workers.lst > reject.lst
	grep -v "^ *1 " participants.lst \
		| awk '{ print $$2; }' \
		>> reject.lst
	./find_holy.py batches/batch-*.csv | cut -d'	' -f1 >> reject.lst

pids.tsv: participants.lst
	echo "id	submissions	worker_id" > pids.tsv
	awk '{ print FNR "\t" $$1 "\t" $$2; }' < participants.lst >> pids.tsv

batches/filtered-batch-%.csv: batches/batch-%.csv reject.lst
	grep -v Rejected $< \
		| grep -vf reject.lst \
		| sed "s/\\r$$//" \
		| tr "\\r" " " \
		| sed "/^$$/d" \
		| sed "s/Answer.identification_/Answer.similarity_/g" \
		> $@


#batches/full-makeup-%.tsv: batches/makeup-%.tsv
#	sed "1s/\t/\tAnswer./g" $< > $@

jump: batches/filtered-batch-1.csv batches/filtered-batch-2.csv batches/filtered-batch-3.csv
	touch jump
#jump: batches/filtered-batch-1.csv batches/filtered-batch-2.csv batches/filtered-batch-3.csv batches/full-makeup-1.tsv batches/full-makeup-2.tsv batches/full-makeup-3.tsv
#	touch jump

#efr.tsv: jump pids.tsv process.py
#	./process.py batches/filtered-batch-*.csv batches/full-makeup-*.tsv > efr.tsv

efr.tsv: jump pids.tsv process.py
	./process.py batches/filtered-batch-*.csv > efr.tsv

genders.lst: efr.tsv
	cut -d"	" -f25 efr.tsv | tail -n +2 | sort | uniq -c > genders.lst

ethnicities.lst: efr.tsv
	cut -d"	" -f27 efr.tsv | tail -n +2 | sort | uniq -c > ethnicities.lst

ethnicities.txt: ethnicities.lst ethnicities.py
	./ethnicities.py < $< > $@

nationalities.lst: efr.tsv
	cut -d"	" -f29 efr.tsv | tail -n +2 | sort | uniq -c > nationalities.lst

efr-aug.tsv: efr.tsv reprocess.py
	./reprocess.py < efr.tsv > efr-aug.tsv

efr-aug-grp.json: efr-aug.tsv group.py framedata.py properties.py
	./group.py < efr-aug.tsv > efr-aug-grp.json

tests-%.json: efr-aug-grp.json analyze.py
	./analyze.py $* < $< > initial-report-$*.txt

analysis_results-%.json: tests-%.json correct.py
	./correct.py $* < $< > corrections-report-$*.txt

tables-%.tex: analysis_results-%.json tabulate.py
	./tabulate.py < $< > $@

tables-full.tex: tables-15000.tex
	cp $< $@

.PRECIOUS: tests-%.json analysis_results-%.json

plots.log: efr-aug-grp.json plot.py
	mkdir -p plots
	./plot.py < $< > $@

plots/%.pdf: plots/%.svg plots.log
	inkscape --export-filename=$@ $<

.PHONY: figures
figures: \
	plots/constructs_by_gender.pdf \
	plots/constructs_by_skin_color.pdf \
	plots/demo-age.pdf \
	plots/demo-edu.pdf \
	plots/demo-gender.pdf \
	plots/demo-play.pdf

.PHONY: clean
clean:
	rm -f efr.tsv efr-aug.tsv efr-aug-grp.json
