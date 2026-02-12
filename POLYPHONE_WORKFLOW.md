# Polyphone Workflow for Creating SF2 Files

**Discovery:** Polyphone doesn't auto-load samples from SFZ files. You need to manually import samples first.

## ✅ Working Workflow

### Method 1: Flat Directory (Recommended)

**Step 1: Organize Samples**
- Put ALL samples in one flat directory (no subfolders)
- Example: `tr808_flat/` contains:
  - `808_kick_c1.wav`
  - `808_snare_d1.wav`
  - etc.

**Step 2: Create SFZ**
- SFZ should reference samples by filename only
- Example: `<region> sample=808_kick_c1.wav lokey=36 hikey=36 pitch_keycenter=36`

**Step 3: Import in Polyphone**
1. Open Polyphone
2. Click **≡ menu** → **File** → **Import** → **Samples**
3. Navigate to the flat directory
4. Select **ALL WAV files** (Cmd+A)
5. Click **Open**
6. **IMPORTANT:** When asked "Replace existing samples?", click **NO**

**Step 4: Import SFZ**
1. Click **≡ menu** → **File** → **Open**
2. Select the SFZ file in the same directory
3. Samples should now be mapped correctly!

**Step 5: Export as SF2**
1. Click **≡ menu** → **File** → **Export** → **SoundFont**
2. Save as: `roland_tr808.sf2`
3. Done!

### Method 2: Subdirectories (Doesn't Work Well)

Polyphone has trouble loading samples from subdirectories when opening SFZ files.
The samples show up as "missing" unless manually imported first.

## Automation Strategy

For all 22 drum kits:

1. **Create flat directory structure**
2. **Copy all samples to flat directory** (no subfolders)
3. **Generate SFZ** with simple filename references
4. **User workflow:**
   - Import all samples (once per directory)
   - Open SFZ
   - Export as SF2

## Success

✅ **TR-808 SF2 created:** 2.3 MB with embedded samples
📍 **Location:** `piano_workshop/dist/drum_kits/roland_tr808.sf2`

## Next Steps

Option A: **Manual workflow** (2-3 hours for all 22 kits)
- Use the flat structure method
- Follow the workflow above

Option B: **Automate flat structure creation**
- Run script to flatten all directories
- Generate SFZ files
- Then just do Steps 3-5 for each kit

## Tested With

- ✅ TR-808 (22 samples, 2.3 MB SF2)
- ⏳ Remaining 21 kits
