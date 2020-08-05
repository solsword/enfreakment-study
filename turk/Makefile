%.html: %.html.pre expand.vim
	vim -T dumb -N -n -E -s -c 'set nomore' -c 'source expand.vim' -c'wq! $@' $<

%-instantiated.html: %.html instantiate.vim hits.csv
	vim -T dumb -N -n -E -s -c 'set nomore' -c 'source instantiate.vim' -c'wq! $@' $<

batch/instance-%.html: batch/instantiate-%.vim template-likert.html hits.csv
	vim -T dumb -N -n -E -s -c 'set nomore' -c 'source $<' -c'wq! $@' template-likert.html

batch/instance-%-local.html: batch/instance-%.html
	cat $^ \
	| sed \
	  "s/web.mit.edu\/pmwh\/www\/enfreakment-images/localhost:8000/g" \
	> $@

ALL_INST=$(shell seq `expr \`wc -l hits.csv | sed "s/^ *\([0-9]*\).*$$/\1/"\` - 1` | awk '{print "batch/instance-" $$1 ".html"}')

ALL_LOCAL=$(shell seq `expr \`wc -l hits.csv | sed "s/^ *\([0-9]*\).*$$/\1/"\` - 1` | awk '{print "batch/instance-" $$1 "-local.html"}')

.PHONY: allinst
allinst: $(ALL_INST)

.PHONY: alllocal
alllocal: $(ALL_LOCAL)

batch:
	mkdir -p batch

batch/instantiate-%.vim: batch instantiate.vim
	head -n2 instantiate.vim > $@
	echo $* >> $@
	tail -n+4 instantiate.vim >> $@

.PHONY: redo
redo: template-likert-instantiated.html
	head -n -2 $< > redo-tmp.html
	cat top.html redo-tmp.html bottom.html > redo-`head -n3 instantiate.vim | tail -n1`.html

# -T dumb → don't detect terminal type; use dumb
# -N → nocompat mode
# -u NONE → don't use a vimrc
# -n → no swap file
# -E → improved ex mode
# -s → silent mode
# -c → run this command after file load

report.lp: counterbalance.lp characters.lp
	clingo --verbose=0 --quiet=1,2,2 counterbalance.lp characters.lp \
		| head -n 1 \
		| sed "s/) /)§/g" \
		| tr "§" "\n" \
		| sed "s/$$/./g" \
		> $@

.PHONY: report
report: report.lp post.lp
	clingo --verbose=0 --quiet=1,2,2 report.lp post.lp \
		| head -n 1 \
		| sed "s/$$/./g" \
		| sed "s/) /)§/g" \
		| tr "§" "\n" \
		| sort

groups.csv: report.lp post.lp shuffle_columns.py
	clingo --verbose=0 --quiet=1,2,2 report.lp post.lp \
		| head -n 1 \
		| sed "s/$$/./g" \
		| sed "s/) /)§/g" \
		| tr "§" "\n" \
		| grep group \
		| sed "s/^group(g("// \
		| sed "s/))\.$$"// \
		| tr -d ')' \
		| ./shuffle_columns.py \
		> $@

hits.csv: groups.csv all_chars.csv group_hits.py
	./group_hits.py > $@

all_urls.csv: hits.csv
	tail -n +2 hits.csv | cut -d, -f4 > $@
	tail -n +2 hits.csv | cut -d, -f5 >> $@
	tail -n +2 hits.csv | cut -d, -f6 >> $@
	tail -n +2 hits.csv | cut -d'"' -f5 | cut -d, -f5 >> $@
	tail -n +2 hits.csv | cut -d'"' -f5 | cut -d, -f6 >> $@
	tail -n +2 hits.csv | cut -d'"' -f5 | cut -d, -f7 >> $@
	tail -n +2 hits.csv | cut -d'"' -f9 | cut -d, -f5 >> $@
	tail -n +2 hits.csv | cut -d'"' -f9 | cut -d, -f6 >> $@
	tail -n +2 hits.csv | cut -d'"' -f9 | cut -d, -f7 >> $@
	tail -n +2 hits.csv | cut -d'"' -f13 | cut -d, -f5 >> $@
	tail -n +2 hits.csv | cut -d'"' -f13 | cut -d, -f6 >> $@
	tail -n +2 hits.csv | cut -d'"' -f13 | cut -d, -f7 >> $@
	tail -n +2 hits.csv | cut -d'"' -f17 | cut -d, -f5 >> $@
	tail -n +2 hits.csv | cut -d'"' -f17 | cut -d, -f6 >> $@
	tail -n +2 hits.csv | cut -d'"' -f17 | cut -d, -f7 >> $@

unique_urls.csv: all_urls.csv
	sort all_urls.csv | uniq > $@

test/missing: unique_urls.csv
	mkdir -p test; cd test; rm -f missing; touch missing; for url in `cat ../unique_urls.csv`; do wget "$$url" || echo "Missing: $$url" >> missing; done

.PHONY: default
default: template-likert-instantiated.html

.DEFAULT_TARGET := default

.PHONY: clean-images
clean-images:
	rm -Rf clean/
	mkdir -p clean
	for f in `ls images/sfv/clean`; do cp images/sfv/clean/$$f clean/; done
	for f in `ls images/tk7/clean`; do cp images/tk7/clean/$$f clean/; done

template-localhost.html: template-likert-instantiated.html clean-images
	cat template-likert-instantiated.html \
	| sed \
	  "s/web.mit.edu\/pmwh\/www\/enfreakment-images/localhost:8000/g" \
	> $@

template-local.html: template-likert-instantiated.html clean-images
	cat template-likert-instantiated.html \
	| sed \
	  "s/http:\/\/web.mit.edu\/pmwh\/www\/enfreakment-images\///g" \
	> $@
