#!/usr/bin/env python3
"""
Demo script to show tkinter Listbox behavior with not found images.
This simulates the ImageSelector behavior when some files are found and others are not.
"""

import tkinter as tk
from tkinter import messagebox
import time


def demo_listbox_behavior():
    """Demo function that simulates the ImageSelector behavior with mixed results"""
    
    # Simulate processing results
    copied_files = ["photo1.jpg", "photo2.png", "image3.gif", "picture4.jpeg"]
    not_found_files = ["missing1.jpg", "notfound2.png", "absent3.gif", "lost4.jpeg", "vanished5.tiff"]
    
    # Create main window (hidden like in ImageSelector)
    root = tk.Tk()
    root.withdraw()  # Hide main window
    root.title("ImageSelector Demo")
    
    # Show completion message (like in ImageSelector)
    messagebox.showinfo(
        "Completed",
        f"Copied {len(copied_files)} images.\nNot found: {len(not_found_files)}"
    )
    
    # If there are not found files, show the listbox window (exact same logic as ImageSelector)
    if not_found_files:
        not_found_window = tk.Toplevel(root)
        not_found_window.title("Not Found Images")
        not_found_window.geometry("400x300")  # Set a reasonable size
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(not_found_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox with scrollbar
        listbox = tk.Listbox(not_found_window, yscrollcommand=scrollbar.set)
        for image in not_found_files:
            listbox.insert(tk.END, image)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=listbox.yview)
        
        # Add a close button for convenience
        close_button = tk.Button(
            not_found_window, 
            text="Close", 
            command=not_found_window.destroy
        )
        close_button.pack(side=tk.BOTTOM, pady=5)
        
        # Make the window visible and bring to front
        not_found_window.deiconify()
        not_found_window.lift()
        not_found_window.focus_force()
    
    # Keep the demo running
    root.mainloop()


def demo_with_many_files():
    """Demo with many files to show scrolling behavior"""
    
    # Create main window
    root = tk.Tk()
    root.withdraw()
    root.title("ImageSelector Demo - Many Files")
    
    # Simulate many not found files
    not_found_files = [f"missing_file_{i:03d}.jpg" for i in range(1, 51)]  # 50 files
    copied_files = [f"found_file_{i:03d}.jpg" for i in range(1, 21)]  # 20 files
    
    messagebox.showinfo(
        "Completed",
        f"Copied {len(copied_files)} images.\nNot found: {len(not_found_files)}"
    )
    
    if not_found_files:
        not_found_window = tk.Toplevel(root)
        not_found_window.title("Not Found Images - Scrolling Demo")
        not_found_window.geometry("500x400")
        
        # Add a label for context
        label = tk.Label(not_found_window, text=f"{len(not_found_files)} files not found:", font=("Arial", 12, "bold"))
        label.pack(pady=5)
        
        # Create frame for listbox and scrollbar
        frame = tk.Frame(not_found_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Courier", 10))
        for image in not_found_files:
            listbox.insert(tk.END, image)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=listbox.yview)
        
        # Add close button
        close_button = tk.Button(
            not_found_window, 
            text="Close", 
            command=not_found_window.destroy
        )
        close_button.pack(pady=5)
        
        not_found_window.deiconify()
        not_found_window.lift()
        not_found_window.focus_force()
    
    root.mainloop()


def demo_menu():
    """Show a menu to choose which demo to run"""
    
    root = tk.Tk()
    root.title("ImageSelector Listbox Demo")
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    title_label = tk.Label(
        root, 
        text="ImageSelector Listbox Behavior Demo", 
        font=("Arial", 14, "bold")
    )
    title_label.pack(pady=20)
    
    description_label = tk.Label(
        root, 
        text="Choose a demo to see how the 'Not Found Images' window works:",
        font=("Arial", 10)
    )
    description_label.pack(pady=10)
    
    # Demo buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    demo1_button = tk.Button(
        button_frame,
        text="Basic Demo (5 files)",
        command=lambda: [root.destroy(), demo_listbox_behavior()],
        width=20,
        height=2
    )
    demo1_button.pack(pady=5)
    
    demo2_button = tk.Button(
        button_frame,
        text="Scrolling Demo (50 files)",
        command=lambda: [root.destroy(), demo_with_many_files()],
        width=20,
        height=2
    )
    demo2_button.pack(pady=5)
    
    quit_button = tk.Button(
        button_frame,
        text="Quit",
        command=root.destroy,
        width=20
    )
    quit_button.pack(pady=5)
    
    root.mainloop()


if __name__ == "__main__":
    print("🎯 ImageSelector Listbox Behavior Demo")
    print("=" * 50)
    print("This demo shows exactly how the ImageSelector script")
    print("displays not found images in a scrollable window.")
    print("=" * 50)
    demo_menu()
