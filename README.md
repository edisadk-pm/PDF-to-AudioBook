# PDF-to-AudioBook

A macOS desktop application that converts PDF, Markdown, and text files into speech using text-to-speech technology. Features a modern graphical user interface with playback controls.

## Features

- 📄 **Multiple File Format Support**: PDF, Markdown (.md), and plain text (.txt) files
- 🎯 **Drag & Drop**: Simply drag files onto the app window
- 🎮 **Playback Controls**: Play, pause, stop, skip forward/backward
- ⚡ **Adjustable Speed**: Control speech rate (0.5x, 1x, 1.5x, 2x)
- 👁️ **Visual Feedback**: See current file, playback status, and text being read
- 🔄 **Responsive UI**: Threading keeps the interface smooth during playback

## Screenshots

![App Interface](docs/screenshot.png)

## Installation

### Prerequisites

- Python 3.7 or higher
- macOS (primary target), but also works on Windows and Linux

### Setup

1. Clone the repository:
```bash
git clone https://github.com/edisadk-pm/PDF-to-AudioBook.git
cd PDF-to-AudioBook
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### macOS-specific Setup

On macOS, you may need to grant accessibility permissions for text-to-speech to work properly:
1. Go to System Preferences > Security & Privacy > Privacy
2. Select "Accessibility" from the list
3. Add Terminal or your Python executable to the allowed apps

## Usage

### Running the GUI Application (Recommended)

Launch the desktop application:
```bash
python app.py
```

The application window will open with:
1. **Drag & Drop Area**: Drag a PDF, Markdown, or text file onto this area, or click it to open a file picker
2. **File Information**: Shows the currently loaded file and playback status
3. **Speed Control**: Buttons to adjust speech rate (0.5x to 2x speed)
4. **Playback Controls**:
   - **⏮ Skip Back**: Jump backward in the text
   - **▶ Play / ⏸ Pause**: Start or pause the reading
   - **⏭ Skip Forward**: Jump forward in the text
   - **■ Stop**: Stop playback and return to the beginning
5. **Text Display**: Shows the current section of text being read

### Running the CLI Tool (Legacy)

The original command-line interface is still available:
```bash
python main.py <pdf_file> [output_audio_file]
```

Examples:
```bash
# Read a PDF aloud
python main.py document.pdf

# Save speech to an audio file
python main.py document.pdf output.mp3
```

## Supported File Formats

- **PDF (.pdf)**: Extracts text from PDF documents using PyPDF2
- **Markdown (.md)**: Reads Markdown files (preserves raw text)
- **Text (.txt)**: Reads plain text files

## How It Works

1. **Text Extraction**: The app extracts text content based on the file type
2. **Chunking**: Text is split into sentences for smoother playback and pause/resume functionality
3. **Speech Synthesis**: Uses pyttsx3 (which uses native OS text-to-speech engines)
4. **Threading**: Speech runs in a background thread to keep the UI responsive

## Technology Stack

- **GUI Framework**: tkinter (built-in with Python) + tkinterdnd2 (drag & drop support)
- **Text-to-Speech**: pyttsx3 (cross-platform TTS library)
- **PDF Processing**: PyPDF2
- **Threading**: Python's built-in threading module

## Troubleshooting

### No sound on macOS
Make sure you've granted accessibility permissions as described in the installation section.

### Voice sounds robotic
This is normal - the app uses the system's built-in text-to-speech engine. You can adjust the speed to make it sound more natural.

### App freezes during playback
The app uses threading to prevent freezing, but very large files may cause brief delays. Try splitting large documents into smaller sections.

## Development

### Project Structure
```
PDF-to-AudioBook/
├── app.py              # GUI application (main entry point)
├── main.py             # CLI tool (legacy)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- pyttsx3 for cross-platform text-to-speech
- PyPDF2 for PDF text extraction
- tkinterdnd2 for drag-and-drop functionality
