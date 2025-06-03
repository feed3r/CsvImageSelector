import csv
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


# GUI to select files/folders
def select_csv():
    return filedialog.askopenfilename(
        title="Select the CSV file",
        filetypes=[("CSV files", "*.csv")]
    )


def select_folder(title):
    return filedialog.askdirectory(title=title)


def main():
    root = tk.Tk()
    root.withdraw()  # Hides the main window

    csv_file = select_csv()
    if not csv_file:
        messagebox.showerror("Error", "No CSV file selected.")
        return

    photo_folder = select_folder("Select the folder of original photos")
    if not photo_folder:
        messagebox.showerror("Error", "No photo folder selected.")
        return

    destination_folder = select_folder("Select the destination folder")
    if not destination_folder:
        messagebox.showerror("Error", "No destination folder selected.")
        return

    file_name_column = simpledialog.askstring(
        "Input",
        "Enter the name of the column containing the image in the CSV:"
    )
    if not file_name_column:
        messagebox.showerror("Error", "No column name provided.")
        return

    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            photo_names = {
                os.path.basename(row[file_name_column])
                for row in reader
                if row[file_name_column]
            }

        not_found = []
        copied = 0

        for photo_name in photo_names:
            src = os.path.join(photo_folder, photo_name)
            dst = os.path.join(destination_folder, photo_name)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                copied += 1
            else:
                not_found.append(photo_name)

        messagebox.showinfo(
            "Completed",
            f"Copied {copied} images.\nNot found: {len(not_found)}"
        )

        if not_found:
            not_found_window = tk.Toplevel(root)
            not_found_window.title("Not Found Images")

            scrollbar = tk.Scrollbar(not_found_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(not_found_window, yscrollcommand=scrollbar.set)
            for image in not_found:
                listbox.insert(tk.END, image)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=listbox.yview)

    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()
