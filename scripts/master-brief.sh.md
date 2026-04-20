#!/bin/bash
# BridgeWorks YouTube Intelligence Pipeline
# Usage: ./youtube-pipeline.sh

BASE_DIR="$HOME/bridgeworks-workspace/youtube-extraction"
CHANNELS_DIR="$BASE_DIR/channels"
TRANSCRIPTS_DIR="$BASE_DIR/transcripts"
BRIEFS_DIR="$BASE_DIR/briefs"
OUTPUT_FILE="$BASE_DIR/master-brief.md"

# Create folder structure
mkdir -p "$CHANNELS_DIR" "$TRANSCRIPTS_DIR" "$BRIEFS_DIR"

echo "=== PHASE 1: CHANNEL SCOUTING ==="
echo ""

# Read channel list
if [ ! -f "$BASE_DIR/channel-list.txt" ]; then
  echo "ERROR: No channel-list.txt found in $BASE_DIR"
  echo "Create it first with one channel name or URL per line."
  exit 1
fi

while IFS= read -r channel; do
  [ -z "$channel" ] && continue
  slug=$(echo "$channel" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g' | sed 's/-$//')
  echo "Scouting: $channel"
  claude "Using the youtube-channel-scout skill, scout this channel: $channel" > "$CHANNELS_DIR/scout-$slug.md"
  echo "Done: scout-$slug.md"
  echo ""
done < "$BASE_DIR/channel-list.txt"

echo "=== PHASE 1 COMPLETE ==="
echo "Scout reports saved in: $CHANNELS_DIR"
echo ""
echo ">>> REVIEW THE SCOUT REPORTS NOW <<<"
echo ">>> Then create: $BASE_DIR/video-list.txt <<<"
echo ">>> One YouTube URL per line — only the videos worth extracting <<<"
echo ">>> When ready, run: ./youtube-pipeline.sh extract <<<"

# Phase 2: Extract (only runs when called with 'extract' argument)
if [ "$1" = "extract" ]; then
  echo ""
  echo "=== PHASE 2: TRANSCRIPT EXTRACTION & BRIEF GENERATION ==="

  if [ ! -f "$BASE_DIR/video-list.txt" ]; then
    echo "ERROR: No video-list.txt found in $BASE_DIR"
    exit 1
  fi

  counter=1
  while IFS= read -r url; do
    [ -z "$url" ] && continue
    padded=$(printf "%02d" $counter)
    echo "Processing video $padded: $url"
    
    # Get transcript and generate brief in one pass
    claude "Get the transcript for this YouTube video: $url — then using the youtube-offer-extraction skill, process the transcript and output the standardised brief." > "$BRIEFS_DIR/brief-$padded.md"
    
    echo "Done: brief-$padded.md"
    counter=$((counter + 1))
  done < "$BASE_DIR/video-list.txt"

  echo ""
  echo "=== PHASE 2 COMPLETE ==="

  # Combine all briefs
  echo "# BridgeWorks YouTube Intelligence Briefs" > "$OUTPUT_FILE"
  echo "# Generated: $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "---" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"

  for brief in "$BRIEFS_DIR"/brief-*.md; do
    cat "$brief" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  done

  echo "Master brief saved to: $OUTPUT_FILE"
  echo ""
  echo ">>> COPY CONTENTS OF master-brief.md TO CLAUDE.AI <<<"
fi