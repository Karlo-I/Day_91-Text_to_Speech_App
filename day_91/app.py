from tkinter import messagebox, ttk, filedialog # 'ttk' for the Combobox' and filedialog' for file selection
import tkinter as tk
import pygame
from day_91.pdf import extract_text_from_pdf
from day_91.voice_rss import voice_2_text

PLACEHOLDER_TEXT = "Extracted text from PDF goes here..."
EN_GB = "en-gb" # Default language
LANGUAGE_CODE_MAP = {
    "English (Great Britain)": EN_GB,
    "Chinese (China)": "zh-cn",
    "Spanish (Mexico)": "es-mx",
    "Arabic (Saudi Arabia)": "ar-sa",
    "Dutch (Netherlands)": "nl-nl",
    "French (France)": "fr-fr",
    "Malay": "ms-my",
    "Thai": "th-th",
    "Polish": "pl-pl",
    "Vietnamese": "vi-vn",
    "Russian": "ru-ru"
}
LANG_DESCR = [lang_title for lang_title in LANGUAGE_CODE_MAP.keys()]

class Pdf2Voice:
    def __init__(self):
        self.pdf_text = ""
        self.language = EN_GB

        # Initialize pygame mixer to ensure it's ready for audio playback
        print("Initializing the app...")
        pygame.mixer.init()

        window = tk.Tk()
        window.geometry("550x510")
        window.title("Text-to-Speech App")
        window.config(bg="light cyan")

        entrance_label = tk.Label(window,
                                  text="Extract text from PDF and click the speech button.",
                                  font=('Arial', 20),
                                  fg="black",
                                  bg="light cyan")

        entrance_label.pack(pady=20)

        # Text widget for writing
        self.text_block = tk.Text(window,
                             wrap="word",
                             height=10,
                             width=50,
                             font=('Arial', 14),
                             bg="light yellow")

        self.text_block.pack(pady=20)

        # Text input area is focused on click and at the start
        self.text_block.bind("<Button-1>", self.on_click)  # This ensures focus when clicked
        self.text_block.focus_set()  # Ensure focus on the text box at the start

        # Text placeholder
        self.text_block.insert(tk.END, PLACEHOLDER_TEXT)
        self.text_block.config(fg="grey")  # Set the color of placeholder text

        # Button to extract PDF text
        extract_button = tk.Button(window,
                                   text="Choose PDF File",
                                   command=self.extract_pdf_text,
                                   font=("Arial", 14),
                                   bg="light green",
                                   height=2,
                                   width=20)

        extract_button.pack(pady=10)

        # Label for the language selection dropdown
        language_label = tk.Label(window,
                                  text="Select Language:",
                                  font=('Arial', 16),
                                  fg="black",
                                  bg="light cyan")

        language_label.pack(pady=10)

        # Language selection dropdown (Combobox)
        self.language_combobox = ttk.Combobox(window,
                                              values=LANG_DESCR,
                                              font=('Arial', 14),
                                              state="readonly")

        self.language_combobox.pack(pady=2)

        # Sets the default value of the dropdown to EN-GB
        self.language_combobox.set("English (Great Britain)")

        # Binds the combobox to the update_language function, so it updates the language when user selects language
        self.language_combobox.bind("<<ComboboxSelected>>", self.update_language)

        # Microphone button
        voice_icon = tk.PhotoImage(file="../assets/voice-search.png")
        voice_icon = voice_icon.subsample(15, 15)
        voice_button = tk.Button(window,
                                 image=voice_icon,  # Use the icon as the button
                                 command=self.get_text_voiceover,
                                 borderwidth=0,  # Remove border for cleaner look
                                 relief="flat",  # Make it flat without the default raised look
                                 bg="light cyan",
                                 height=50,
                                 width=50)

        voice_button.pack(pady=20)

        window.mainloop() # Run the Tkinter event loop

    def on_click(self,event):
        # Ensure that the cursor is visible when clicking
        self.text_block.focus_set()

        # Clear any previous highlights when the user clicks anywhere in the text
        self.text_block.tag_remove("highlight", "1.0", tk.END)

        # If the placeholder text is still there, remove it when user clicks to start typing
        if self.text_block.get("1.0", "1.end") == PLACEHOLDER_TEXT:
            self.text_block.delete("1.0", "1.end")
            self.text_block.config(fg="black")

            # Insert the extracted PDF text if it is available
            if self.pdf_text:
                self.text_block.insert("1.0", self.pdf_text)
                self.text_block.config(fg="black")
            else:
                messagebox.showwarning("No Text", "No PDF text extracted.")

    def extract_pdf_text(self):
        # Open a file dialog to allow the user to choose a PDF file
        pdf_file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")], title="Select a PDF File"
        )

        if pdf_file_path:
            pdf_text = extract_text_from_pdf(pdf_file_path)
            messagebox.showinfo("Text Extraction", "PDF text has been successfully extracted!")

            # Clear any existing text and insert the extracted text into the text block automatically
            self.text_block.delete("1.0", tk.END)
            self.text_block.insert("1.0", pdf_text)
            self.text_block.config(fg="black")

        else:
            messagebox.showwarning("File Selection", "No File Selected.")

    def update_language(self, event):
        selected_language = self.language_combobox.get()  # Get the selected language name

        # Map the selected language name to the language code, set 'en-gb' as default
        self.language = LANGUAGE_CODE_MAP.get(selected_language, "en-gb")
        # print(f"Selected language: {self.language}")  # Debugging print to confirm language change

    # GET API request
    def get_text_voiceover(self):
        input_text = self.text_block.get("1.0", tk.END).strip() # Get the text entered by the user

        if input_text == "" or input_text == PLACEHOLDER_TEXT:
            messagebox.showwarning("Input Error", "Please enter some text first.")
            return

        try:
            # Make sure pygame mixer is initialized before playing audio
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Convert text to speech, load audio file and play audio
            file_path = voice_2_text(input_text, self.language)
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        return input_text