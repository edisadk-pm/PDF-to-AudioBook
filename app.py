import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pyttsx3
from PyPDF2 import PdfReader
import threading
import re
import os


class AudioBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF/Text to Speech Reader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # State variables
        self.current_file = None
        self.text_content = ""
        self.text_chunks = []
        self.current_chunk_index = 0
        self.is_playing = False
        self.is_paused = False
        self.speech_rate = 150
        self.engine = None
        self.speech_thread = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF/Text to Speech Reader", 
                                font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Drag and drop area
        self.drop_frame = tk.Frame(main_frame, bg='#e8e8e8', relief=tk.SUNKEN, 
                                    borderwidth=2, height=120)
        self.drop_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), 
                             pady=(0, 10))
        self.drop_frame.grid_propagate(False)
        
        drop_label = tk.Label(self.drop_frame, text="Drag & Drop File Here\nor click to select", 
                              bg='#e8e8e8', font=('Helvetica', 12))
        drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Enable drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.bind('<Button-1>', lambda e: self.select_file())
        drop_label.bind('<Button-1>', lambda e: self.select_file())
        
        # File info
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), 
                        pady=(0, 10))
        
        ttk.Label(file_frame, text="File:").grid(row=0, column=0, sticky=tk.W)
        self.file_label = ttk.Label(file_frame, text="No file loaded", 
                                     foreground='gray')
        self.file_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(file_frame, text="Status:").grid(row=1, column=0, sticky=tk.W)
        self.status_label = ttk.Label(file_frame, text="Stopped", 
                                       foreground='gray')
        self.status_label.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # Speed control
        speed_frame = ttk.LabelFrame(main_frame, text="Speed Control", padding="10")
        speed_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), 
                         pady=(0, 10))
        
        self.speed_buttons = []
        speeds = [("0.5x", 75), ("1x", 150), ("1.5x", 225), ("2x", 300)]
        for i, (label, rate) in enumerate(speeds):
            btn = ttk.Button(speed_frame, text=label, width=8,
                            command=lambda r=rate: self.set_speed(r))
            btn.grid(row=0, column=i, padx=5)
            self.speed_buttons.append(btn)
        
        # Playback controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=4, pady=(0, 10))
        
        self.skip_back_btn = ttk.Button(control_frame, text="⏮ Skip Back", 
                                        command=self.skip_backward)
        self.skip_back_btn.grid(row=0, column=0, padx=5)
        
        self.play_pause_btn = ttk.Button(control_frame, text="▶ Play", 
                                          command=self.toggle_play_pause)
        self.play_pause_btn.grid(row=0, column=1, padx=5)
        
        self.skip_fwd_btn = ttk.Button(control_frame, text="⏭ Skip Forward", 
                                        command=self.skip_forward)
        self.skip_fwd_btn.grid(row=0, column=2, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="■ Stop", 
                                    command=self.stop_playback)
        self.stop_btn.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # Current text display (optional)
        text_frame = ttk.LabelFrame(main_frame, text="Current Text", padding="10")
        text_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(5, weight=1)
        
        self.text_display = tk.Text(text_frame, height=8, wrap=tk.WORD, 
                                     state='disabled')
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                  command=self.text_display.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        # Disable controls initially
        self.update_control_states()
        
    def on_drop(self, event):
        """Handle file drop event"""
        # Get the file path from the event
        file_path = event.data
        # Remove curly braces if present
        file_path = file_path.strip('{}')
        self.load_file(file_path)
        
    def select_file(self):
        """Open file dialog to select a file"""
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All supported files", "*.pdf *.md *.txt"),
                ("PDF files", "*.pdf"),
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path)
            
    def load_file(self, file_path):
        """Load and extract text from the selected file"""
        try:
            if not os.path.exists(file_path):
                self.show_error(f"File not found: {file_path}")
                return
                
            # Stop any current playback
            if self.is_playing:
                self.stop_playback()
                
            # Extract text based on file type
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                self.text_content = self.extract_text_from_pdf(file_path)
            elif ext == '.md':
                self.text_content = self.extract_text_from_markdown(file_path)
            elif ext == '.txt':
                self.text_content = self.extract_text_from_text(file_path)
            else:
                self.show_error(f"Unsupported file type: {ext}")
                return
                
            # Update state
            self.current_file = file_path
            self.file_label.config(text=os.path.basename(file_path), 
                                   foreground='black')
            
            # Split text into chunks (sentences)
            self.text_chunks = self.split_into_chunks(self.text_content)
            self.current_chunk_index = 0
            
            # Display first chunk
            self.display_current_text()
            
            # Enable controls
            self.update_control_states()
            
            self.status_label.config(text="Ready", foreground='green')
            
        except Exception as e:
            self.show_error(f"Error loading file: {str(e)}")
            
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
        
    def extract_text_from_markdown(self, md_path):
        """Extract text from Markdown file"""
        with open(md_path, "r", encoding='utf-8') as file:
            text = file.read()
        # Optionally strip markdown formatting
        # For now, keep raw text
        return text
        
    def extract_text_from_text(self, txt_path):
        """Extract text from plain text file"""
        with open(txt_path, "r", encoding='utf-8') as file:
            text = file.read()
        return text
        
    def split_into_chunks(self, text):
        """Split text into sentences for chunked reading"""
        # Split by sentence endings
        chunks = re.split(r'(?<=[.!?])\s+', text)
        # Filter out empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        return chunks
        
    def display_current_text(self):
        """Display the current text chunk in the text widget"""
        if not self.text_chunks:
            return
            
        # Get current and next few chunks for context
        start_idx = max(0, self.current_chunk_index - 1)
        end_idx = min(len(self.text_chunks), self.current_chunk_index + 5)
        display_text = " ".join(self.text_chunks[start_idx:end_idx])
        
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, display_text)
        self.text_display.config(state='disabled')
        
    def set_speed(self, rate):
        """Set speech rate"""
        self.speech_rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
            
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if not self.text_chunks:
            self.show_error("No file loaded")
            return
            
        if self.is_playing:
            # Pause
            self.pause_playback()
        else:
            # Play or Resume
            self.start_playback()
            
    def start_playback(self):
        """Start or resume playback"""
        if not self.text_chunks:
            return
            
        self.is_playing = True
        self.is_paused = False
        self.status_label.config(text="Playing", foreground='green')
        self.play_pause_btn.config(text="⏸ Pause")
        
        # Start speech thread if not running
        if self.speech_thread is None or not self.speech_thread.is_alive():
            self.speech_thread = threading.Thread(target=self.speech_worker, 
                                                   daemon=True)
            self.speech_thread.start()
            
    def pause_playback(self):
        """Pause playback"""
        self.is_playing = False
        self.is_paused = True
        self.status_label.config(text="Paused", foreground='orange')
        self.play_pause_btn.config(text="▶ Play")
        
    def stop_playback(self):
        """Stop playback completely"""
        self.is_playing = False
        self.is_paused = False
        self.current_chunk_index = 0
        self.status_label.config(text="Stopped", foreground='gray')
        self.play_pause_btn.config(text="▶ Play")
        self.display_current_text()
        
        # Stop the engine
        if self.engine:
            try:
                self.engine.stop()
            except RuntimeError:
                # Engine may already be stopped or in an invalid state
                pass
                
    def skip_forward(self):
        """Skip forward in text"""
        if not self.text_chunks:
            return
            
        # Skip 5 chunks forward
        self.current_chunk_index = min(len(self.text_chunks) - 1, 
                                       self.current_chunk_index + 5)
        self.display_current_text()
        
    def skip_backward(self):
        """Skip backward in text"""
        if not self.text_chunks:
            return
            
        # Skip 5 chunks backward
        self.current_chunk_index = max(0, self.current_chunk_index - 5)
        self.display_current_text()
        
    def speech_worker(self):
        """Worker thread for speech synthesis"""
        try:
            # Initialize engine in this thread
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.speech_rate)
            
            while self.current_chunk_index < len(self.text_chunks):
                if not self.is_playing:
                    # Paused or stopped
                    break
                    
                # Get current chunk
                chunk = self.text_chunks[self.current_chunk_index]
                
                # Update display on main thread
                self.root.after(0, self.display_current_text)
                
                # Speak the chunk
                self.engine.say(chunk)
                self.engine.runAndWait()
                
                # Move to next chunk
                self.current_chunk_index += 1
                
            # Playback finished
            if self.current_chunk_index >= len(self.text_chunks):
                self.root.after(0, self.playback_finished)
                
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Speech error: {str(e)}"))
            
    def playback_finished(self):
        """Called when playback finishes"""
        self.is_playing = False
        self.is_paused = False
        self.current_chunk_index = 0
        self.status_label.config(text="Finished", foreground='blue')
        self.play_pause_btn.config(text="▶ Play")
        self.display_current_text()
        
    def update_control_states(self):
        """Update the state of control buttons"""
        has_file = self.current_file is not None
        
        state = 'normal' if has_file else 'disabled'
        self.play_pause_btn.config(state=state)
        self.stop_btn.config(state=state)
        self.skip_back_btn.config(state=state)
        self.skip_fwd_btn.config(state=state)
        
        for btn in self.speed_buttons:
            btn.config(state=state)
            
    def show_error(self, message):
        """Show error message"""
        self.status_label.config(text=f"Error: {message}", foreground='red')


def main():
    """Main entry point"""
    root = TkinterDnD.Tk()
    app = AudioBookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
