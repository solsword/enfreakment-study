%.html: %.html.pre expand.vim
	vim -T dumb -N -n -E -s -c 'set nomore' -c 'source expand.vim' -c'wq! $@' $<

%-instantiated.html: %.html instantiate.vim test.csv
	vim -T dumb -N -n -E -s -c 'set nomore' -c 'source instantiate.vim' -c'wq! $@' $<

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
		| sed "s/$$/./g" \
		| sed "s/) /).\n/g" \
		> $@

.PHONY: report
report: report.lp post.lp
	clingo --verbose=0 --quiet=1,2,2 report.lp post.lp \
		| head -n 1 \
		| sed "s/$$/./g" \
		| sed "s/) /).\n/g" \
		| sort

groups.csv: report.lp post.lp shuffle_columns.py
	clingo --verbose=0 --quiet=1,2,2 report.lp post.lp \
		| head -n 1 \
		| sed "s/$$/./g" \
		| sed "s/) /).\n/g" \
		| grep group \
		| sed "s/^group(g("// \
		| sed "s/))\.$$"// \
		| ./shuffle_columns.py \
		> $@

hits.csv: groups.csv all_chars.csv group_hits.py
	./group_hits.py > $@

test.csv: hits.csv
	head -n 3 hits.csv > $@

.PHONY: default
default: template-likert-instantiated.html
