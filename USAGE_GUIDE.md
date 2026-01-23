# PDF/Text to Speech Reader - User Guide

## Application Interface

The application provides a clean, intuitive interface for converting documents to speech:

```
┌──────────────────────────────────────────────────────────┐
│        PDF/Text to Speech Reader                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │                                                    │  │
│  │          Drag & Drop File Here                     │  │
│  │          or click to select                        │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  File: example.pdf                                       │
│  Status: Playing                                         │
│                                                          │
│  ┌─────── Speed Control ──────┐                         │
│  │  [0.5x] [1x] [1.5x] [2x]   │                         │
│  └────────────────────────────┘                         │
│                                                          │
│    [⏮ Skip Back]  [⏸ Pause]  [⏭ Skip Forward]           │
│                                                          │
│              [■ Stop]                                    │
│                                                          │
│  ┌──────── Current Text ────────┐                       │
│  │ This is the current text     │                       │
│  │ being read aloud. The app    │                       │
│  │ displays context around the  │                       │
│  │ current position...          │                       │
│  │                              │                       │
│  └──────────────────────────────┘                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Features Explained

### 1. Drag & Drop Area
- Drag PDF, Markdown (.md), or text (.txt) files directly onto this area
- Click the area to open a file picker dialog
- Supported formats are automatically detected

### 2. File Information
- **File:** Shows the name of the currently loaded file
- **Status:** Shows current playback state (Stopped, Ready, Playing, Paused, Finished)
- Status colors:
  - Gray: Stopped
  - Green: Ready/Playing
  - Orange: Paused
  - Blue: Finished
  - Red: Error

### 3. Speed Control
- Adjust speech rate to your preference
- **0.5x:** Slow speed (75 words/minute)
- **1x:** Normal speed (150 words/minute) - Default
- **1.5x:** Fast speed (225 words/minute)
- **2x:** Very fast speed (300 words/minute)

### 4. Playback Controls

#### Skip Back (⏮)
- Jumps backward in the text by 5 sentences
- Useful for re-listening to missed sections
- Works during playback or when paused

#### Play/Pause (▶/⏸)
- **Play (▶):** Start reading from current position
- **Pause (⏸):** Pause at current position
- Button changes based on current state
- Resume from where you paused

#### Skip Forward (⏭)
- Jumps forward in the text by 5 sentences
- Useful for skipping sections
- Works during playback or when paused

#### Stop (■)
- Stops playback completely
- Returns to the beginning of the document
- Resets to initial state

### 5. Current Text Display
- Shows the text currently being read
- Displays context (previous and upcoming sentences)
- Auto-scrolls to follow playback position
- Helps you follow along while listening

## Quick Start

1. **Launch the app:**
   ```bash
   python app.py
   ```

2. **Load a file:**
   - Drag a PDF/MD/TXT file onto the drop area, OR
   - Click the drop area to select a file

3. **Adjust speed (optional):**
   - Click one of the speed buttons (0.5x, 1x, 1.5x, 2x)

4. **Start playback:**
   - Click the "▶ Play" button

5. **Control playback:**
   - Use Pause to temporarily stop
   - Use Skip buttons to navigate
   - Use Stop to return to beginning

## Tips

- **Reading long documents:** The app splits text into sentences for smooth playback
- **Following along:** Watch the Current Text display to see what's being read
- **Speed adjustment:** Try different speeds to find what's comfortable
- **Pausing:** You can pause, skip around, and resume at any time
- **Multi-format:** Works with PDFs, Markdown, and plain text files

## Keyboard Shortcuts

Currently, the app uses mouse/trackpad controls. Future versions may include:
- Space: Play/Pause
- Left Arrow: Skip Back
- Right Arrow: Skip Forward
- S: Stop
- 1-4: Speed selection

## Technical Details

- **Text Extraction:** Uses PyPDF2 for PDFs, direct reading for text/markdown
- **Speech Engine:** Uses pyttsx3 (native OS text-to-speech)
- **Threading:** Speech runs in background thread for responsive UI
- **Chunking:** Text is split by sentences for pause/resume functionality

## Troubleshooting

### No sound
- Check system volume
- Verify text-to-speech is enabled in system settings
- On macOS: Grant accessibility permissions

### App not responding
- The app uses threading to stay responsive
- Very large files may cause brief delays when loading

### Voice quality
- Uses your system's built-in text-to-speech engine
- Quality depends on your operating system
- Adjust speed for better comprehension
