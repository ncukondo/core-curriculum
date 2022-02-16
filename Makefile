pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
d_run:=docker run --rm --volume "${pwd}:/data" --user ${uid}:${gid} ${repo}

deploy:
	python deploy_to_google_drive.py

docs: pdf docx

draft_docs: draft_pdf draft_docx

draft_docx: r4_draft_temp.html
	${d_run}pandoc-latex-ja ./dist/r4_draft_temp.html -o ./dist/r4_draft.docx

docx: markdown
	${d_run}pandoc-latex-ja ./dist/r4.md -o ./dist/r4.docx

pdf: markdown
	${d_run}pandoc-latex-ja \
		-V classoption="pandoc" \
		-V documentclass=bxjsarticle \
		--pdf-engine=xelatex \
		--filter=pandoc-crossref \
		./dist/r4.md \
		-o ./dist/r4.pdf

draft_pdf: r4_draft_temp.html
	${d_run}pandoc-latex-ja \
		-V classoption="pandoc" \
		-V documentclass=bxjsarticle \
		--pdf-engine=xelatex \
		--filter=pandoc-crossref \
		./dist/r4_draft_temp.html \
		-o ./dist/r4_draft.pdf

r4_draft_temp.html: 
	${d_run}pandoc-latex-ja \
		-s --self-contained \
		--from markdown+strikeout \
		-t html5 \
		./dist/r4_draft.md \
		-o ./dist/r4_draft_temp.html



raw_csv:
	python download_sheets.py

csv:
	python output_csv.py

markdown: csv
	python output_markdown.py

python_files:
	jupyter nbconvert --to python download_sheets.ipynb
	jupyter nbconvert --to python output_csv.ipynb
	jupyter nbconvert --to python output_markdown.ipynb
	jupyter nbconvert --to python deploy_to_google_drive.ipynb

draft_csv:
	bash download_r4.sh r4_draft_gsheets.csv
