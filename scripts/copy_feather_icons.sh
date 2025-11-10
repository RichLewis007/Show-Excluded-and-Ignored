#!/usr/bin/env bash

# Copy the Feather icons required by Ghost Files Finder into the project resources
# directory. Adjust the icon list as the toolbar or UI grows.

set -euo pipefail

SRC_DIR="/Users/rich/temp/feather-icons/node_modules/feather-icons/dist/icons"
DEST_DIR="/Users/rich/dev/github/richlewis007/show-excluded-and-ignored/src/rfe/resources/icons/feather"

ICONS=(
  "play.svg"
  "refresh-ccw.svg"
  "folder.svg"
  "file-text.svg"
  "trash-2.svg"
  "download.svg"
  "x-circle.svg"
  "chevrons-down.svg"
  "chevrons-up.svg"
  "external-link.svg"
  "pause.svg"
  "square.svg"
  "tag.svg"
)

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Source directory not found: $SRC_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

for icon in "${ICONS[@]}"; do
  if [[ ! -f "$SRC_DIR/$icon" ]]; then
    echo "Missing icon in source directory: $icon" >&2
    exit 1
  fi
  cp -f "$SRC_DIR/$icon" "$DEST_DIR/$icon"
  echo "Copied $icon"
done

echo "Feather icons copied to $DEST_DIR"
