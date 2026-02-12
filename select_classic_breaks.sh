#!/bin/bash
#
# Select 30 classic drum breaks from the_breaks collection
# and organize them for SoundFont creation
#

# Source directory
SOURCE_DIR="/Volumes/Storage/samples/the_breaks"

# Target directory
TARGET_DIR="/Users/bretbouchard/apps/schill/piano_workshop/dist/sf2_sources/drum_breaks"

# Create target directory
mkdir -p "$TARGET_DIR"

# 30 Classic Drum Breaks (most famous and widely used)
declare -a BREAKS=(
    # The most sampled breaks
    "Amen Brother - The Winstons.wav"
    "Impeach The President - Honeydrippers (ver.1).wav"
    "Funky President - James Brown.wav"
    "Funky Drummer - James Brown (ver.1).wav"
    "Cold Sweat - James Brown (ver.1).wav"
    "Good Foot - James Brown (ver.1).wav"

    # Classic funk breaks
    "Funky Mule - Ike & Tina Turner (part1).wav"
    "Funky Donkey - Bernard Purdie (part1).wav"
    "Funky Nassau - Beginning of the End.wav"
    "It's A New Day - Skull Snaps (part1).wav"
    "Ashley's Roachclip - The Soul Searchers.wav"
    "Synthetic Substitution - Melvin Bliss.wav"

    # Rare groove classics
    "Apache - Incredible Bongo Band.wav"
    "Take Me To The Mardi Gras - Bob James.wav"
    "God Made Me Funky - Headhunters (part1).wav"
    "Holy Ghost - The Jimmy Castor Bunch.wav"
    "Sport - Lightnin' Rod.wav"
    "Pleasingly Well - The Seconds.wav"

    # Hip-hop classics
    "The Breakdown - Rufus Thomas.wav"
    "Catch A Groove - Juice.wav"
    "It's Just Begun - Jimmy Castor Bunch.wav"
    "Scorpio - Dennis Coffey.wav"
    "Get Out Of My Life Woman - Allen Toussaint.wav"

    # Modern classics
    "You Know I'm No Good - Amy Winehouse.wav"
    "Funky In Jamaica - Alatac.wav"
    "Thinkin'bout The Good Times - Black Pearl (montage).wav"

    # Essential breaks
    "Long Red - Mountain (live).wav"
    "I'll Stay - Jimmy McGriff.wav"
    "Nust Thang - New Birth.wav"
    "The Big Beat - Billy Squier.wav"
    "Rock Steady - Al Green.wav"
    "Son Of Shaft - The Bar-Kays.wav"
)

echo "============================================================"
echo "Selecting 30 Classic Drum Breaks"
echo "============================================================"
echo ""

# Copy each break
copied=0
for break_name in "${BREAKS[@]}"; do
    # Try to find the file (case-insensitive)
    if find "$SOURCE_DIR" -iname "$break_name" -print -quit 2>/dev/null | while read file; do
        # Get just the filename for the target
        target_name=$(echo "$break_name" | sed 's/ (ver\.[0-9])//' | sed 's/ (part[0-9])//' | sed 's/ (cd)//' | sed 's/ (edit)//' | sed 's/ (montage)//' | sed 's/ (live)//')
        cp "$file" "$TARGET_DIR/$target_name"
        echo "✅ Copied: $break_name"
        copied=$((copied + 1))
    done; then :; fi
done

echo ""
echo "============================================================"
echo "Summary"
echo "============================================================"
echo "Copied $copied drum breaks to: $TARGET_DIR"
echo ""
echo "File sizes:"
du -sh "$TARGET_DIR"
echo ""
echo "Sample files:"
ls -lh "$TARGET_DIR" | awk '{print $9, "("$5")"}' | grep -v "^$"
