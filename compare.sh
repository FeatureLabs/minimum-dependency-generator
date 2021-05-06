#!/bin/bash
file_1="correct-min-requirements.txt"
file_2="generated-min-reqs.txt"

if cmp -s "$file1" "$file2"; then
    printf 'The file "%s" is the same as "%s"\n' "$file1" "$file2"
    exit 0
else
    printf 'The file "%s" is different from "%s"\n' "$file1" "$file2"
    exit 1
fi