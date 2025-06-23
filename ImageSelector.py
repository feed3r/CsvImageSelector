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


def detect_delimiter(sample_line):
    if '\t' in sample_line:
        return '\t'
    elif ';' in sample_line:
        return ';'
    elif ',' in sample_line:
        return ','
    else:
        return ','  # fallback


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
            
            first_line = f.readline()
            f.seek(0)  # torna all'inizio del file
            delimiter = detect_delimiter(first_line)
            reader = csv.DictReader(f, delimiter=delimiter)
            
            # Case-insensitive header matching
            header_map = {col.lower(): col for col in reader.fieldnames}
            requested_col = file_name_column.strip().lower()
            if requested_col not in header_map:
                messagebox.showerror("Error", f"Column '{file_name_column}' not found in CSV.")
                return
            actual_column = header_map[requested_col]

            photo_names = {
                os.path.basename(row[actual_column])
                for row in reader
                if row.get(actual_column)
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
            # Crea una finestra figlia
            not_found_window = tk.Toplevel(root)
            not_found_window.title("Images Not Found")
            not_found_window.geometry("500x400")

            label = tk.Label(not_found_window, text="The following images were not found:", font=("Arial", 12))
            label.pack(pady=10)

            frame = tk.Frame(not_found_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=60)
            for image in not_found:
                listbox.insert(tk.END, image)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=listbox.yview)

            # Aggiungi un pulsante per chiudere
            close_button = tk.Button(not_found_window, text="Close", command=not_found_window.destroy)
            close_button.pack(pady=10)

            # Rendi modale la finestra
            not_found_window.transient(root)
            not_found_window.grab_set()
            root.deiconify()  # Assicura che root sia "vivo"
            root.wait_window(not_found_window)



    except KeyError as e:
        messagebox.showerror("Error", f"Column '{file_name_column}' not found in CSV: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()
