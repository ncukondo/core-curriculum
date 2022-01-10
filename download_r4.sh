#!/usr/bin/env bash
set -Ceuo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

inputFile='r4_gsheets.config'

ensure_return(){ awk 1;}
skip_empty(){ sed '/^$/d';}
add_bom(){ sed -e '1s/^/\xef\xbb\xbf/';}


cat $inputFile \
| skip_empty   \
| ensure_return \
| while IFS=, read title sheetid gid; do
    url=https://docs.google.com/spreadsheets/d/${sheetid}/export?format=csv\&gid=${gid}
    output=./raw/${title}.csv
    echo Downloading... $url to $output
    curl -L $url | add_bom >| $output
  done 
