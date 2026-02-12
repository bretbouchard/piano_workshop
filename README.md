# Piano Workshop

Audio sample library containing piano, orchestra, and drum machine samples for the White Room Box ecosystem.

## Contents

### Piano Samples
- **Salamander Grand Piano V1** (581 MB)
  - Location: `dist/sam_sampler_piano/piano/salamander_grand_v1.sf2`
  - Format: SoundFont 2 (.sf2)
  - License: See `dist/sam_sampler_piano/piano/attribution.txt`

### Drum Kits
- Location: `dist/drum_kits/`
- Various drum machine samples and breaks
- REX sliced drum breaks

### Orchestral Samples
- Coming soon

## Usage

These samples are used as a git submodule in the White Room Box project.

### As a Submodule

```bash
# In white_room_box repository
git submodule add https://github.com/bretbouchard/piano_workshop.git third_party/piano_workshop
git submodule update --init --recursive
```

### Direct Access

Samples can be loaded directly from the `dist/` directory:
- Piano: `dist/sam_sampler_piano/piano/salamander_grand_v1.sf2`
- Drums: `dist/drum_kits/`

## Scripts

- `create_sf2_from_samples.py` - Create SoundFont files from samples
- `create_drum_breaks_sf2.py` - Create drum break SoundFonts
- `slice_drum_breaks.py` - Slice drum breaks into individual samples
- `copy_breaks.py` - Copy and organize drum breaks

## License

See individual `attribution.txt` files for licensing information for each sample collection.

## Repository Structure

```
piano_workshop/
├── dist/                   # Built sample libraries
│   ├── sam_sampler_piano/  # Piano samples
│   ├── drum_kits/          # Drum machine samples
│   └── sf2_sources/        # Source samples for SoundFont creation
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── src/                    # Source code
```

## Related Repositories

- [white_room_box](https://github.com/bretbouchard/white_room_box.git) - Main White Room repository
- [audio_agent_juce](https://github.com/bretbouchard/audio_agent_juce.git) - JUCE audio backend
