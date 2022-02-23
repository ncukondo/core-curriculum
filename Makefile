pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
d_run:=docker run --rm --volume "${pwd}:/data" --user ${uid}:${gid} ${repo}

deploy:
	jupyter nbconvert --to python deploy_to_google_drive.ipynb
	python deploy_to_google_drive.py

docs: pdf docx

draft_docs: draft_pdf draft_docx

draft_docx: r4_draft_temp_html
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

draft_pdf: r4_draft_temp_html
	${d_run}pandoc-latex-ja \
		-V classoption="pandoc" \
		-V documentclass=bxjsarticle \
		--pdf-engine=xelatex \
		--filter=pandoc-crossref \
		./dist/r4_draft_temp.html \
		-o ./dist/r4_draft.pdf

r4_draft_temp_html: markdown
	${d_run}pandoc-latex-ja \
		-s --self-contained \
		--from markdown+strikeout \
		-t html5 \
		./dist/r4_draft.md \
		-o ./dist/r4_draft_temp.html

markdown: csv
	jupyter nbconvert --to python output_markdown.ipynb
	python output_markdown.py

csv: 
	jupyter nbconvert --to python output_csv.ipynb
	python output_csv.py

statistics:
	jupyter nbconvert --to python output_statistics.ipynb
	python output_statistics.py


raw_csv:
	jupyter nbconvert --to python download_sheets.ipynb
	python download_sheets.py

output_csv.py: output_csv.ipynb
	jupyter nbconvert --to python output_csv.ipynb

download_sheets.py: download_sheets.ipynb
	jupyter nbconvert --to python download_sheets.ipynb

deploy_to_google_drive.py: deploy_to_google_drive.ipynb
	jupyter nbconvert --to python deploy_to_google_drive.ipynb

output_markdown.py: output_markdown.ipynb
	jupyter nbconvert --to python output_markdown.ipynb

output_statistics.py: output_statistics.ipynb
	jupyter nbconvert --to python output_statistics.ipynb

