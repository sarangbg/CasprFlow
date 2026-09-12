#!/usr/bin/env bash

# module load samtools/1.19.2-gcc-11.5.0-pdghgfh
# bc = substr(bc, 2, 5);

#bc = substr(bc, 1, bl);

echo "Counting barcodes in $1"

#bc = substr(bc, 2, bl);
barcode_length=6

samtools view $1 | awk -v bl="$barcode_length" '{
    n = split($1, a, "+");
    bc = a[n];
    if (bc ~ /[Nn]/ || length(bc) != bl) next;
    key = $3 "\t" bc;
    count[key]++
} END {
    for (k in count) print k "\t" count[k]
}' | sort -k1,1 > $2
