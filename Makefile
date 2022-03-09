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

draft_docx:
	${d_run}pandoc-latex-ja -N --toc --filter=pandoc-crossref ./dist/r4_draft.md -o ./dist/r4_draft.docx

docx: markdown
	${d_run}pandoc-latex-ja -N --toc --filter=pandoc-crossref ./dist/r4.md -o ./dist/r4.docx

# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --pdf-engine=lualatex --filter=pandoc-crossref ./dist/r4.md -o ./dist/r4.pdf
pdf: markdown
	${d_run}pandoc-latex-ja \
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		-N \
		--toc \
		./dist/r4.md \
		-o ./dist/r4.pdf

# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --pdf-engine=lualatex --filter=pandoc-crossref ./dist/r4_draft.md -o ./dist/r4_draft.pdf
draft_pdf: markdown
	${d_run}pandoc-latex-ja \
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		-N \
		--toc \
		./dist/r4_draft.md \
		-o ./dist/r4_draft.pdf

markdown: csv tables
	jupyter nbconvert --to python output_markdown.ipynb
	python output_markdown.py

tables: csv 
	jupyter nbconvert --to python output_tables.ipynb
	python output_tables.py

csv: 
	jupyter nbconvert --to python output_csv.ipynb
	python output_csv.py

statistics:
	jupyter nbconvert --to python output_statistics.ipynb
	python output_statistics.py


raw_csv:
	$(eval target=download_sheets)
	jupyter nbconvert --to python $(target).ipynb --output $(target).py
	python  $(target).py
