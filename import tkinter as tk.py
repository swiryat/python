import tkinter as tk
from tkinter import scrolledtext, Text
import requests
from bs4 import BeautifulSoup

def is_valid_html(html):
    try:
        # Use BeautifulSoup to check syntax
        soup = BeautifulSoup(html, 'html.parser')
        
        # Use W3C Markup Validation Service for additional validation
        validator_url = "https://validator.w3.org/nu/?format=json"
        headers = {"Content-Type": "text/html; charset=utf-8"}
        response = requests.post(validator_url, data=html.encode('utf-8'), headers=headers)
        result = response.json()

        if result['messages']:
            raise Exception(result['messages'])

        return True
    except Exception as e:
        # If an error occurs, HTML is considered invalid
        show_error_window(html, str(e))
        return False

def show_error_window(html, error_message):
    error_window = tk.Toplevel(window)
    error_window.title("Error in HTML")

    error_label = tk.Label(error_window, text=error_message, fg="red")
    error_label.pack(pady=10)

    error_code_label = tk.Label(error_window, text="HTML with error:")
    error_code_label.pack()

    error_code_text = Text(error_window, wrap=tk.WORD, width=40, height=10)
    error_code_text.insert(tk.END, html)
    error_code_text.pack(padx=10, pady=10)

# Create the main window
window = tk.Tk()
window.title("HTML Validation")

# Create a text field for entering HTML code
text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
text.pack(padx=10, pady=10)

# Button to initiate the validation
check_button = tk.Button(window, text="Validate HTML", command=lambda: is_valid_html(text.get("1.0", tk.END)))
check_button.pack(pady=5)

# Label to display the validation result
result_label = tk.Label(window, text="", fg="black")
result_label.pack(pady=5)

# Run the event loop
window.mainloop()
