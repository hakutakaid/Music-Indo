#!/bin/bash

echo -n "Masukkan nilai lama: "
read lama

echo -n "Masukkan nilai baru: "
read baru

lama_esc=$(printf '%s\n' "$lama" | sed -e 's/[\/&]/\\&/g')
baru_esc=$(printf '%s\n' "$baru" | sed -e 's/[\/&]/\\&/g')

find . -type d -name '.git' -prune -o -type f -exec sed -i "s#$lama_esc#$baru_esc#g" {} +
