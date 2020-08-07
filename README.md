% Analyzing Virtual Enfreakment
% Sercan Şengün, James Bowie-Wilson, Peter Mawhorter, Yusef Audeh, Haewoon Kwak, and D. Fox Harrell

This repository contains code and data from an online study that sought
to measure some of the contours of virtual enfreakment in fighting games
(Street Fighter V and Tekken 7 specifically). You can browse all of the
files online at:
[https://github.com/solsword/enfreakment-study/](https://github.com/solsword/enfreakment-study/)

This document explains what resources are available; the details of the
survey methodology and statistical analysis are explained in [this
methodology document](methodology.html).

## Study Setup

The `turk/` folder contains the HTML templates and other data required to
construct the Amazon Mechanical Turk Human Intelligence Tasks (HITs) that
we used to carry out the study. There is code there which was used to
create randomized HITs and put together templates, etc. The `Makefile` in
that directory, although not well-documented, should give a sense of how
things fit together; it relies on the `clingo` constraint solving library
to create counterbalanced character groupings, as well as `python` for
some of the scripts.

If you want to see an example of a fully constructed HIT, the
[`turk/template-local.html`](turk/template-local.html) file shows what a
single HIT template looks like when filled out; if you are viewing it
locally you should run `make template-local.html` in the `turk/` folder
first otherwise the images will not show up.

## Data & Analysis

The `data/` folder contains both anonymized survey response data (in the
file [`efr.tsv`](data/efr.tsv)) as well as code for analyzing it based on
our hypotheses. Again, the `Makefile` shows how things fit together; note
that there are some rules there for processing the raw data, but based on
our study protocols this raw data which contains AMT user IDs cannot be
made public.

The analysis code uses the `scipy` and `krippendorf` Python packages, and
should work with Python versions roughly 3.5-5.8 at least. It uses fairly
large bootstrap samples to do statistics, and can take dozens of minutes
or more to finish, although it does print progress messages (try `tail -f
report.txt` while `make report.txt` is running).

The `Makefile` scripts assume a POSIX environment and probably a few GNU
utilities on top of that, so they're easiest to run in a Mac or Linux
environment, but you could run some of the data processing steps manually
if you wanted to, and if you're designing a similar study or if you just
want to run your own analysis of the data, you can likely simplify things
enormously.
