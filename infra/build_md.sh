#!/bin/bash

html=`github-markup $1.md`
# paste html into template with styles
template="$(<template.html)"
echo "${template/\[BODY\]/$html}" > $1.html
# convert HTML to PDF
wkhtmltopdf $1.html $1.pdf

