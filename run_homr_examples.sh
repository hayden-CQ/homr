#!/bin/bash

# Script to run homr on all images in /Users/markokostiv/Downloads/examples

EXAMPLES_DIR="/Users/markokostiv/Downloads/Photos New"

# Function to convert HEIC to JPEG and return the path
convert_heic_if_needed() {
    local image="$1"
    local ext="${image##*.}"
    local ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    
    # Check if it's a HEIC file (case insensitive)
    if [[ "$ext_lower" == "heic" || "$ext_lower" == "heif" ]]; then
        local jpeg_path="${image%.*}.jpg"
        echo "Converting HEIC to JPEG: $image -> $jpeg_path" >&2
        sips -s format jpeg "$image" --out "$jpeg_path" >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$jpeg_path"
            return 0
        else
            echo "Failed to convert HEIC: $image" >&2
            echo ""
            return 1
        fi
    else
        echo "$image"
        return 0
    fi
}

# Find all image files including HEIC and process them
find "$EXAMPLES_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" -o -iname "*.heic" -o -iname "*.heif" \) | while read -r image; do
    echo "=========================================="
    echo "Processing: $image"
    echo "=========================================="
    
    # Convert HEIC if needed, otherwise use original
    processed_image=$(convert_heic_if_needed "$image")
    
    if [[ -n "$processed_image" ]]; then
        poetry run homr "$processed_image"
    else
        echo "Skipping due to conversion error"
    fi
    
    echo ""
done

echo "Done processing all images!"
