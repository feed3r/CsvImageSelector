import unittest
import os
import shutil
import sys
import tempfile
import csv
from unittest.mock import patch, MagicMock

# Add parent directory to path to import ImageSelector
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ImageSelector


class TestImageSelector(unittest.TestCase):

    def setUp(self):
        # Create temporary directories and files for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.temp_dir, "test.csv")
        self.test_photo_folder = os.path.join(self.temp_dir, "test_photos")
        self.test_destination_folder = os.path.join(self.temp_dir, "test_destination")

        os.makedirs(self.test_photo_folder)
        os.makedirs(self.test_destination_folder)

        # Create test CSV with semicolon delimiter
        with open(self.test_csv, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['image', 'description'])
            writer.writerow(['photo1.jpg', 'First photo'])
            writer.writerow(['photo2.png', 'Second photo'])
            writer.writerow(['nonexistent.jpg', 'Missing photo'])

        # Create test image files
        with open(os.path.join(self.test_photo_folder, "photo1.jpg"), "w") as f:
            f.write("dummy image data 1")
        with open(os.path.join(self.test_photo_folder, "photo2.png"), "w") as f:
            f.write("dummy image data 2")

    def tearDown(self):
        # Clean up temporary directories and files
        shutil.rmtree(self.temp_dir)

    def test_csv_parsing_with_paths(self):
        """Test that CSV parsing correctly handles file paths"""
        # Create CSV with full paths
        csv_with_paths = os.path.join(self.temp_dir, "test_paths.csv")
        with open(csv_with_paths, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['filepath'])
            writer.writerow(['/some/path/photo1.jpg'])
            writer.writerow(['C:\\Windows\\photo2.png'])
        
        # Read CSV and extract photo names
        with open(csv_with_paths, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            photo_names = {
                os.path.basename(row['filepath'])
                for row in reader
                if row['filepath']
            }
        
        # Verify only filenames are extracted
        expected_names = {'photo1.jpg', 'photo2.png'}
        self.assertEqual(photo_names, expected_names)

    def test_file_copying_behavior(self):
        """Test file copying and tracking of not found files"""
        # Create a test scenario with mixed existing/non-existing files
        photo_names = {'photo1.jpg', 'photo2.png', 'nonexistent.jpg', 'another_missing.png'}
        
        not_found = []
        copied = 0
        
        for photo_name in photo_names:
            src = os.path.join(self.test_photo_folder, photo_name)
            dst = os.path.join(self.test_destination_folder, photo_name)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                copied += 1
            else:
                not_found.append(photo_name)
        
        # Verify results
        self.assertEqual(copied, 2)
        self.assertEqual(len(not_found), 2)
        self.assertIn('nonexistent.jpg', not_found)
        self.assertIn('another_missing.png', not_found)
        
        # Verify copied files exist in destination
        self.assertTrue(os.path.exists(os.path.join(self.test_destination_folder, 'photo1.jpg')))
        self.assertTrue(os.path.exists(os.path.join(self.test_destination_folder, 'photo2.png')))

    def test_select_csv(self):
        """Test the select_csv function"""
        with patch('ImageSelector.filedialog.askopenfilename') as mock_dialog:
            mock_dialog.return_value = '/path/to/test.csv'
            result = ImageSelector.select_csv()
            self.assertEqual(result, '/path/to/test.csv')
            mock_dialog.assert_called_once_with(
                title="Select the CSV file",
                filetypes=[("CSV files", "*.csv")]
            )

    def test_select_folder(self):
        """Test the select_folder function"""
        with patch('ImageSelector.filedialog.askdirectory') as mock_dialog:
            mock_dialog.return_value = '/path/to/folder'
            result = ImageSelector.select_folder("Test Title")
            self.assertEqual(result, '/path/to/folder')
            mock_dialog.assert_called_once_with(title="Test Title")

    @patch('ImageSelector.tk.Tk')
    @patch('ImageSelector.messagebox.showerror')
    @patch('ImageSelector.filedialog.askopenfilename')
    def test_main_no_csv_selected(self, mock_open_file, mock_error, mock_tk):
        """Test behavior when no CSV file is selected"""
        mock_open_file.return_value = ""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        ImageSelector.main()
        
        mock_error.assert_called_once_with("Error", "No CSV file selected.")

    @patch('ImageSelector.tk.Tk')
    @patch('ImageSelector.messagebox.showerror')
    @patch('ImageSelector.filedialog.askdirectory')
    @patch('ImageSelector.filedialog.askopenfilename')
    def test_main_no_photo_folder_selected(self, mock_open_file, mock_ask_dir, mock_error, mock_tk):
        """Test behavior when no photo folder is selected"""
        mock_open_file.return_value = self.test_csv
        mock_ask_dir.return_value = ""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        ImageSelector.main()
        
        mock_error.assert_called_once_with("Error", "No photo folder selected.")

    @patch('ImageSelector.tk.Toplevel')
    @patch('ImageSelector.tk.Listbox')
    @patch('ImageSelector.tk.Scrollbar')
    @patch('ImageSelector.tk.Tk')
    @patch('ImageSelector.messagebox.showinfo')
    @patch('ImageSelector.simpledialog.askstring')
    @patch('ImageSelector.filedialog.askdirectory')
    @patch('ImageSelector.filedialog.askopenfilename')
    def test_main_successful_copy(self, mock_open_file, mock_ask_dir, mock_ask_string, 
                                  mock_info, mock_tk, mock_scrollbar, mock_listbox, mock_toplevel):
        """Test successful file copy operation"""
        # Mock return values
        mock_open_file.return_value = self.test_csv
        mock_ask_dir.side_effect = [self.test_photo_folder, self.test_destination_folder]
        mock_ask_string.return_value = "image"
        
        # Mock tkinter components
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_toplevel_instance = MagicMock()
        mock_toplevel.return_value = mock_toplevel_instance
        mock_scrollbar_instance = MagicMock()
        mock_scrollbar.return_value = mock_scrollbar_instance
        mock_listbox_instance = MagicMock()
        mock_listbox.return_value = mock_listbox_instance
        
        ImageSelector.main()
        
        # Verify success message was shown
        mock_info.assert_called_once()
        args = mock_info.call_args[0]
        self.assertEqual(args[0], "Completed")
        self.assertIn("Copied 2 images", args[1])
        self.assertIn("Not found: 1", args[1])
        
        # Verify GUI components were created for not found images
        mock_toplevel.assert_called_once_with(mock_root)
        mock_toplevel_instance.title.assert_called_once_with("Not Found Images")

    @patch('ImageSelector.tk.Tk')
    @patch('ImageSelector.messagebox.showerror')
    @patch('ImageSelector.simpledialog.askstring')
    @patch('ImageSelector.filedialog.askdirectory')
    @patch('ImageSelector.filedialog.askopenfilename')
    def test_main_no_column_name(self, mock_open_file, mock_ask_dir, mock_ask_string, mock_error, mock_tk):
        """Test behavior when no column name is provided"""
        mock_open_file.return_value = self.test_csv
        mock_ask_dir.side_effect = [self.test_photo_folder, self.test_destination_folder]
        mock_ask_string.return_value = ""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        ImageSelector.main()
        
        mock_error.assert_called_once_with("Error", "No column name provided.")

    @patch('ImageSelector.tk.Tk')
    @patch('ImageSelector.messagebox.showerror')
    @patch('ImageSelector.simpledialog.askstring')
    @patch('ImageSelector.filedialog.askdirectory')
    @patch('ImageSelector.filedialog.askopenfilename')
    def test_main_csv_error(self, mock_open_file, mock_ask_dir, mock_ask_string, mock_error, mock_tk):
        """Test behavior when CSV file causes an error"""
        mock_open_file.return_value = "/nonexistent/file.csv"
        mock_ask_dir.side_effect = [self.test_photo_folder, self.test_destination_folder]
        mock_ask_string.return_value = "image"
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        ImageSelector.main()
        
        # Should show error for file not found
        mock_error.assert_called_once()
        args = mock_error.call_args[0]
        self.assertEqual(args[0], "Error")


if __name__ == "__main__":
    unittest.main()
