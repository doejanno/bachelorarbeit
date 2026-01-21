#!/bin/bash

# Set the parent directory (the folder that contains the three subfolders)
PARENT_DIR="/home/janno/Uni/Bingen/Semester/09_Semester/Bachelorarbeit/data/Empower-IQAir"

# Loop through each subfolder
for DIR in "$PARENT_DIR"/*/; do
    # Get folder name only
    FOLDER_NAME=$(basename "$DIR")

    # Output file in parent directory
    OUTPUT_FILE="$PARENT_DIR/${FOLDER_NAME}_combined.csv"

    echo "Combining CSVs in $FOLDER_NAME → $OUTPUT_FILE"

    # Combine all CSVs in the folder
    # - Remove header from all except the first file
    FIRST=1
    > "$OUTPUT_FILE"  # Clear or create file

    for FILE in "$DIR"/*.csv; do
        if [[ $FIRST -eq 1 ]]; then
            cat "$FILE" >> "$OUTPUT_FILE"
            FIRST=0
        else
            tail -n +2 "$FILE" >> "$OUTPUT_FILE"
        fi
    done
done

echo "Done!"
