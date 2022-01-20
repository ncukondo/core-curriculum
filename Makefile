pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
d_run:=docker run --rm --volume "${pwd}:/data" --user ${uid}:${gid} ${repo}

docs: pdf docx

csv_and_md:
	${d_run}python-science-ja python r4_processor.py

pdf: csv_and_md
	${d_run}pandoc-latex-ja \
	    -V classoption="pandoc" \
		-V documentclass=bxjsarticle \
		--pdf-engine=xelatex \
		--filter=pandoc-crossref \
		./dist/r4.md \
		-o ./dist/r4.pdf

docx: csv_and_md
	${d_run}pandoc-latex-ja ./dist/r4_to_edit.md -o ./dist/r4_to_edit.docx

raw_csv:
	bash download_r4.sh

draft_csv:
	bash download_r4.sh r4_draft_gsheets.csv
