import os
import base64
import tkinter as tk
from tkinter import filedialog
import re

def is_model_file(rel_path):
    """Check if the relative path is inside a .xcdatamodeld or .xcdatamodel bundle."""
    parts = rel_path.split(os.sep)
    return '.xcdatamodeld' in parts or '.xcdatamodel' in parts

def pack_files(project_dir, output_file):
    extensions = ['.txt', '.swift', '.plist', '.entitlements', '.json']  # Removed .xcdatamodeld
    with open(output_file, 'w', encoding='utf-8') as out:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_dir)
                
                # Pack all files inside model bundles, regardless of extension
                if is_model_file(rel_path):
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    encoded = base64.b64encode(content).decode('utf-8')
                    out.write(f"--- FILE: {rel_path} ---\n")
                    out.write(f"BASE64: {encoded}\n")
                    out.write("--- END ---\n\n")
                # For other files, check extensions
                elif any(file.endswith(ext) for ext in extensions):
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    encoded = base64.b64encode(content).decode('utf-8')
                    out.write(f"--- FILE: {rel_path} ---\n")
                    out.write(f"BASE64: {encoded}\n")
                    out.write("--- END ---\n\n")
    print(f"Packed files into {output_file}")

def unpack_files(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r', encoding='utf-8') as inp:
        content = inp.read()
    
    sections = re.split(r'--- END ---\n\n', content)
    for section in sections:
        if not section.strip():
            continue
        lines = section.split('\n')
        file_line = lines[0].strip()
        if not file_line.startswith('--- FILE: '):
            continue
        rel_path = file_line[len('--- FILE: '):-len(' ---')]
        base64_line = lines[1].strip()
        if not base64_line.startswith('BASE64: '):
            continue
        encoded = base64_line[len('BASE64: '):]
        try:
            decoded = base64.b64decode(encoded)
        except Exception as e:
            print(f"Error decoding {rel_path}: {e}, skipping.")
            continue
        
        out_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as out:
            out.write(decoded)
    print(f"Unpacked files into {output_dir}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print("Do you want to (p)ack or (u)npack? Enter 'p' or 'u':")
    choice = input().strip().lower()
    
    if choice == 'p':
        project_dir = filedialog.askdirectory(title="Select Xcode Project Directory")
        if not project_dir:
            print("No directory selected. Exiting.")
            return
        output_file = filedialog.asksaveasfilename(title="Save Packed File As", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not output_file:
            print("No output file selected. Exiting.")
            return
        pack_files(project_dir, output_file)
    elif choice == 'u':
        input_file = filedialog.askopenfilename(title="Select Packed .txt File", filetypes=[("Text files", "*.txt")])
        if not input_file:
            print("No input file selected. Exiting.")
            return
        output_dir = filedialog.askdirectory(title="Select Output Directory for Unpacking")
        if not output_dir:
            print("No output directory selected. Exiting.")
            return
        unpack_files(input_file, output_dir)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()