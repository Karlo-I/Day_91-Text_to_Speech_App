from dotenv import load_dotenv
from tkinter import messagebox
import tkinter as tk
import os, requests, time, pygame
from urllib.parse import quote_plus  # For encoding the text properly in the URL

# Setup .env password
load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Global variables
placeholder_text = "Start typing here..."  # Placeholder text
URL_ENDPOINT = "http://api.voicerss.org/?"
API_Key = os.getenv("API_Key")
LANGUAGE = "en-gb"
INPUT_TEXT = ""

# Function to handle when the user clicks on the text box and focuses on it
def on_click(event):
    # Ensure that the cursor is visible when clicking
    text_block.focus_set()

    # Clear any previous highlights when the user clicks anywhere in the text
    text_block.tag_remove("highlight", "1.0", tk.END)

    # If the placeholder text is still there, remove it when user clicks to start typing
    if text_block.get("1.0", "1.end") == placeholder_text:
        text_block.delete("1.0", "1.end")  # Remove placeholder text
        text_block.config(fg="black")  # Change text color to black

# Function to insert placeholder text
def insert_placeholder():
    text_block.insert(tk.END, placeholder_text)
    text_block.config(fg="grey")  # Set the color of placeholder text

# Function to send a GET API request
def get_text_voiceover():
    global INPUT_TEXT

    # Get the text entered by the user
    INPUT_TEXT = text_block.get("1.0", tk.END).strip()

    if INPUT_TEXT == "" or INPUT_TEXT == placeholder_text:
        messagebox.showwarning("Input Error", "Please enter some text first.")
        return

    # URL encode the text to ensure it's safe for use in the URL
    encoded_text = quote_plus(INPUT_TEXT)

    # Prepare the URL with encoded text, and specify MP3 format with 'f=mp3'
    url = f"{URL_ENDPOINT}key={API_Key}&hl={LANGUAGE}&src={encoded_text}&f=mp3"

    try:
        response = requests.get(url)

        # Debugging: Print the response headers and the length of the content
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Content length: {len(response.content)} bytes")

        # If the response is successful, receive an audio file in MP3 format
        if response.status_code == 200:
            # Check if the response is an MP3 file by looking at the Content-Type header
            if 'audio/mpeg' not in response.headers['Content-Type']:
                messagebox.showerror("Error", "Received file is not a valid MP3.")
                return

            # Save the audio response as a file
            if os.path.exists("voiceover.mp3"):
                os.remove("voiceover.mp3")  # Remove the old file if it exists

            with open("voiceover.mp3", "wb") as file:
                file.write(response.content)

            # Wait for a short time to ensure the file is completely written before playing it
            time.sleep(1)

            # Play the audio file using pygame
            pygame.mixer.music.load("voiceover.mp3")
            pygame.mixer.music.play()

        else:
            messagebox.showerror("Error", "Failed to retrieve voiceover from the API.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the Tkinter window and UI elements
window = tk.Tk()
window.geometry("500x400")
window.title("Text-to-Speech App")
window.config(bg="light cyan")

entrance_label = tk.Label(window,
                         text="Enter text below and click the speech button.",
                         font=('Arial', 20),
                         fg="black",
                         bg="light cyan")

entrance_label.pack(pady=20)

# Text widget for writing (reduced size)
text_block = tk.Text(window,
                     wrap="word",
                     height=10,   # Reduced height
                     width=50,    # Reduced width
                     font=('Arial', 14),
                     bg="light yellow")

text_block.pack(pady=20)

# Ensure the text input area is focused on click and at the start
text_block.bind("<Button-1>", on_click)  # This ensures focus when clicked
text_block.focus_set()  # Ensure focus on the text box at the start

# Insert placeholder text initially
insert_placeholder()

# Load the microphone icon (replace with the path to your icon)
voice_icon = tk.PhotoImage(file="assets/voice-search.png")  # Ensure you have a .png image

# Resize the icon to a smaller size (e.g., 30% of the original size)
voice_icon = voice_icon.subsample(15, 15)  # Adjust the numbers to fit the size you want

# Voice button to trigger voiceover with icon
voice_button = tk.Button(window,
                         image=voice_icon,   # Use the icon as the button
                         command=get_text_voiceover,
                         borderwidth=0,      # Remove border for cleaner look
                         relief="flat",      # Make it flat without the default raised look
                         bg="light cyan",    # Match the window background color
                         height=50,          # Button height
                         width=50)           # Button width

voice_button.pack(pady=20)

# Run the Tkinter event loop (don't need to handle pygame events here)
window.mainloop()

