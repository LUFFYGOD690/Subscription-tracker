import tkinter as tk
from gui.app import SubscriptionApp  # Import the main GUI class

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()  # Create main window
    app = SubscriptionApp(root)  # Initialize app UI
    root.mainloop()  # Run the GUI loop