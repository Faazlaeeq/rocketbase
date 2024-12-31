import tkinter as tk
from tkinter import ttk

class DarkThemeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Theme App")
        
        # Set the style and dark theme
        self.style = ttk.Style()
        
        # Configure TButton for a dark theme
        self.style.configure(
            "Dark.TButton",
            foreground="white",
            background="#333333",  # Dark gray background
            font=("Segoe UI", 12, "bold"),
            borderwidth=1,
            focuscolor="none"
        )
        self.style.map(
            "Dark.TButton",
            background=[
                ("active", "#555555"),  # Slightly lighter gray when active
                ("!disabled", "#333333")  # Default dark background
            ],
            foreground=[("active", "white"), ("!disabled", "white")]
        )
        
        # Configure the application background
        self.root.configure(bg="#1e1e1e")  # Very dark gray for app background
        
        # Create buttons
        self.create_button("Click Me", self.on_click, 0, 0)
        self.create_button("Exit", self.root.quit, 1, 0)

    def create_button(self, text, command, row, column):
        button = ttk.Button(self.root, text=text, command=command, style="Dark.TButton")
        button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

    def on_click(self):
        print("Button clicked!")

# Main application
root = tk.Tk()
app = DarkThemeApp(root)
root.mainloop()
