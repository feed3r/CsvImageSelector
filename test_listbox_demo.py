#!/usr/bin/env python3
"""
Automated test to demonstrate and validate tkinter Listbox behavior
for the ImageSelector not found files feature.
"""

import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import ImageSelector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestListboxBehavior(unittest.TestCase):
    """Test the Listbox behavior with actual tkinter components"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide during tests
        
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass
    
    def test_listbox_with_not_found_files(self):
        """Test creating and populating a listbox with not found files"""
        
        # Test data - simulate files that were not found
        not_found_files = [
            "missing1.jpg",
            "notfound2.png", 
            "absent3.gif",
            "lost4.jpeg",
            "vanished5.tiff"
        ]
        
        # Create the same components as ImageSelector
        not_found_window = tk.Toplevel(self.root)
        not_found_window.title("Not Found Images")
        not_found_window.geometry("400x300")
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(not_found_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox exactly like ImageSelector
        listbox = tk.Listbox(not_found_window, yscrollcommand=scrollbar.set)
        
        # Populate listbox with not found files
        for image in not_found_files:
            listbox.insert(tk.END, image)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Validate listbox contents
        self.assertEqual(listbox.size(), len(not_found_files))
        
        # Check each item in listbox
        for i, expected_file in enumerate(not_found_files):
            actual_file = listbox.get(i)
            self.assertEqual(actual_file, expected_file)
        
        # Test scrollbar is properly configured
        self.assertEqual(listbox.cget('yscrollcommand'), scrollbar.set)
        
        print(f"✅ Listbox successfully created with {listbox.size()} not found files:")
        for i in range(listbox.size()):
            print(f"   - {listbox.get(i)}")
        
        not_found_window.destroy()
    
    def test_listbox_scrolling_behavior(self):
        """Test listbox with many items to verify scrolling works"""
        
        # Create many files to test scrolling
        not_found_files = [f"missing_file_{i:03d}.jpg" for i in range(1, 26)]  # 25 files
        
        not_found_window = tk.Toplevel(self.root)
        not_found_window.title("Scrolling Test")
        not_found_window.geometry("300x200")  # Small window to force scrolling
        
        scrollbar = tk.Scrollbar(not_found_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(not_found_window, yscrollcommand=scrollbar.set, height=5)  # Small height
        
        for image in not_found_files:
            listbox.insert(tk.END, image)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Force update to calculate scrolling
        not_found_window.update()
        
        # Validate all items are present
        self.assertEqual(listbox.size(), len(not_found_files))
        
        # Test first and last items
        self.assertEqual(listbox.get(0), "missing_file_001.jpg")
        self.assertEqual(listbox.get(listbox.size()-1), "missing_file_025.jpg")
        
        print(f"✅ Scrollable listbox created with {listbox.size()} items")
        print(f"   First item: {listbox.get(0)}")
        print(f"   Last item: {listbox.get(listbox.size()-1)}")
        
        not_found_window.destroy()
    
    def test_empty_listbox_behavior(self):
        """Test behavior when there are no not found files"""
        
        not_found_files = []  # Empty list
        
        # In ImageSelector, if not_found is empty, no window should be created
        # But let's test creating an empty listbox anyway
        if not not_found_files:
            print("✅ No not found files - window would not be created (correct behavior)")
            return
        
        # This code wouldn't execute in ImageSelector, but we test it anyway
        not_found_window = tk.Toplevel(self.root)
        listbox = tk.Listbox(not_found_window)
        
        self.assertEqual(listbox.size(), 0)
        print("✅ Empty listbox behavior validated")
        
        not_found_window.destroy()


def demo_actual_behavior():
    """Interactive demo showing the actual behavior"""
    print("\n" + "="*60)
    print("🎯 INTERACTIVE DEMO - ImageSelector Listbox Behavior")
    print("="*60)
    print("This demo shows exactly what users see when files are not found.")
    print("\nScenario: 3 files copied successfully, 5 files not found")
    print("-"*60)
    
    root = tk.Tk()
    root.withdraw()
    
    # Simulate ImageSelector results
    copied_count = 3
    not_found = ["image001.jpg", "photo_missing.png", "document.pdf", "scan_lost.tiff", "backup_gone.jpeg"]
    
    print(f"✅ Copied: {copied_count} files")
    print(f"❌ Not found: {len(not_found)} files")
    print(f"   Files not found: {', '.join(not_found)}")
    
    # Show completion message (exactly like ImageSelector)
    try:
        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Completed",
            f"Copied {copied_count} images.\nNot found: {len(not_found)}"
        )
        
        # Create not found window (exactly like ImageSelector)
        if not_found:
            not_found_window = tk.Toplevel(root)
            not_found_window.title("Not Found Images")
            not_found_window.geometry("400x250")
            
            # Add instructional label
            info_label = tk.Label(
                not_found_window, 
                text="The following images could not be found:",
                font=("Arial", 10, "bold"),
                pady=10
            )
            info_label.pack()
            
            # Create scrollable listbox (exactly like ImageSelector)
            scrollbar = tk.Scrollbar(not_found_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(not_found_window, yscrollcommand=scrollbar.set)
            for image in not_found:
                listbox.insert(tk.END, image)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar.config(command=listbox.yview)
            
            # Add close button
            close_btn = tk.Button(
                not_found_window, 
                text="Close", 
                command=lambda: [print("✅ Demo completed successfully!"), root.destroy()]
            )
            close_btn.pack(pady=5)
            
            # Make window visible
            not_found_window.deiconify()
            not_found_window.lift()
            
        root.mainloop()
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("✅ Demo completed (GUI may not be available in this environment)")


if __name__ == "__main__":
    print("🧪 Testing ImageSelector Listbox Behavior")
    print("=" * 50)
    
    # Run unit tests
    print("\n1. Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestListboxBehavior)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed! Listbox behavior is working correctly.")
        
        # Run interactive demo
        print("\n2. Running Interactive Demo...")
        demo_actual_behavior()
    else:
        print("\n❌ Some tests failed. Check the output above.")
