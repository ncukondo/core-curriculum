#!/usr/bin/env bash
set -Ceuo pipefail

# register environmental variable in .env to github secrets

inputFile=${1:-.env}
repo=`gh repo view | head -n 1 | sed -r "s/name:\s*(.+)$/\1/"`

echo Target reposigtry is \[$repo\]
echo set secret from $inputFile

ensure_return(){
  awk 1
}

skip_empty(){  
  sed '/^$/d' 
}

readline() {
  read -r "$@" || eval "[ \"\${$1}\" ]"
}

trim() {
  echo $* | sed 's/^ *| *$//' 
}

escape_backslash() {
  sed 's/\\/\\\\/g' 
}


cat $inputFile \
| escape_backslash \
| ensure_return \
| skip_empty \
| while IFS=\= read key value; do
  key=$(trim $key)
  value=$(trim $value)
  echo adding github secret\(repo:$repo\)... key="${key}", value="${value}"
  gh secret set $key -b"${value}" --repos="${repo}"
done 
