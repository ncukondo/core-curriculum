#!/usr/bin/env bash
set -Ceuo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

inputFile=${1:-'r4_gsheets.csv'}

skip_first(){ sed '1d'; }
ensure_return(){ awk 1;}
skip_blank(){ sed '/^$/d';}
add_bom(){ sed -e '1s/^/\xef\xbb\xbf/';}


cat $inputFile \
| skip_first   \
| skip_blank   \
| ensure_return \
| while IFS=, read output sheetid gid; do
    url=https://docs.google.com/spreadsheets/d/${sheetid}/export?format=csv\&gid=${gid}
    echo Downloading... $url to $output
    curl -L $url | add_bom >| $output
  done 
