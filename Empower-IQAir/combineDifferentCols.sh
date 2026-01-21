#!/bin/bash

BASE="/home/janno/Uni/Bingen/Semester/09_Semester/Bachelorarbeit/data/Empower-IQAir"
OUT="$BASE/combined_differentCols"
mkdir -p "$OUT"

for DIR in "$BASE"/*/; do
  echo "Processing $DIR"

  # group by column count
  for N in $(for f in "$DIR"/*.csv; do awk -F',' 'NR==1{print NF; exit}' "$f"; done | sort -u); do

    FILES=$(for f in "$DIR"/*.csv; do
      if [ "$(awk -F',' 'NR==1{print NF; exit}' "$f")" = "$N" ]; then
        echo "$f"
      fi
    done)

    OUTFILE="$OUT/$(basename "$DIR")_${N}cols.csv"
    FIRST=1
    > "$OUTFILE"

    for f in $FILES; do
      if [ $FIRST -eq 1 ]; then
        cat "$f" >> "$OUTFILE"
        FIRST=0
      else
        tail -n +2 "$f" >> "$OUTFILE"
      fi
    done

    echo "  → $OUTFILE"
  done
done
