#!/usr/bin/env bash

combine_folder () {
    local DIR="$1"
    local OUTPUT="$2"

    > "$OUTPUT"
    local FIRST=1

    for file in "$DIR"/*Datensatz*.csv; do
        [ -e "$file" ] || continue

        awk -F';' -v OFS=';' -v first="$FIRST" '
$1=="Nr." {
    header_found=1
    nr=dt=ws=wr=""

    for (i=1; i<=NF; i++) {
        if ($i=="Nr.") nr=i
        else if ($i=="Datum / Uhrzeit") dt=i
        else if ($i ~ /^Windgeschw \[m\/s\]/) ws=i
        else if ($i ~ /^Windricht \[grad\]/) wr=i
    }

    if (first==1) {
        print "Nr.","Datum / Uhrzeit","Windgeschw [m/s]","Windricht [grad]"
    }
    next
}

header_found && $1 ~ /^[0-9]+$/ {
    printf "%s;%s;%s;%s\n",
        (nr!="" && nr<=NF ? $nr : ""),
        (dt!="" && dt<=NF ? $dt : ""),
        (ws!="" && ws<=NF ? $ws : ""),
        (wr!="" && wr<=NF ? $wr : "")
}
' "$file" >> "$OUTPUT"

        FIRST=0
    done
}

combine_folder "Empower-Gründach"   "windRoofCombined.csv"
combine_folder "Empower-Parkplatz" "windGroundCombined.csv"
