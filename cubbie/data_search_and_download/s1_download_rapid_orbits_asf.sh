#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Error: You must provide an output directory path."
    echo "Usage: $0 </path/to/output_directory>"
    exit 1
fi

TARGET_DIR="$1"

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

echo "Downloading rapid orbits to: $(pwd)"

wget -q -O aux_resorb https://s1qc.asf.alaska.edu/aux_resorb/

# NOTE: Syntax of date manipulation only seems to work on Linux.
# Would be different for a Mac or PC doing processing.
LIMIT_DATE=$(date -u -d "21 days ago" +%Y%m%d)
echo "Downloading files from $LIMIT_DATE up to today..."

grep -Eo 'S1[A-D]_OPER_AUX_RESORB_OPOD_[0-9]{8}T[0-9]{6}_V[0-9]{8}T[0-9]{6}_[0-9]{8}T[0-9]{6}\.EOF' aux_resorb | while read -r file; do
    FILE_DATE=$(echo "$file" | cut -d'_' -f6 | cut -c1-8)
    
    if [[ "$FILE_DATE" -ge "$LIMIT_DATE" ]]; then
        if [ ! -f "$file" ]; then
            echo "Downloading: $file"
            wget -q "https://s1qc.asf.alaska.edu/aux_resorb/$file"
        else
            echo "Already exists: $file"
        fi
    fi
done

rm aux_resorb
echo "Download complete!"
