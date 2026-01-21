import pyttsx3
from PyPDF2 import PdfReader
import sys

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb+") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def text_to_speech(text, output_file=None):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    if output_file:
        engine.save_to_file(text, output_file)
        engine.runAndWait()
    else:
        engine.say(text)
        engine.runAndWait()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_file> [output_audio_file]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    text = extract_text_from_pdf(pdf_path)
    text_to_speech(text, output_file)

    print("Done!")

if __name__ == "__main__":
    main()
