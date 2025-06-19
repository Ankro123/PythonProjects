import os
import sys
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

def get_dir(prompt) -> str:
    selected_dir = filedialog.askdirectory(title=prompt)
    if not selected_dir:
        messagebox.showerror("Directory Required", "No Directory Selected")
        sys.exit()
    else:
        return selected_dir

def get_prefix() -> str:
    prefix = simpledialog.askstring("Input Prefix", "Enter new Prefix")
    if not prefix:
        messagebox.showerror("Input Required", "prefix Can't be empty!")
        sys.exit()
    else:
        return prefix
    
def update_dir(src_dest):
    for source,dest in src_dest:
        temp_dest = dest
        dest_dir = os.path.dirname(dest)
        file_name, file_ext = os.path.splitext(os.path.basename(dest))
        i = 1
        if check_duplicates:
            while os.path.exists(temp_dest):
                temp_dest = f"{os.path.join(dest_dir, file_name)}_{i}{file_ext}"
                i+=1
        dest = temp_dest
        os.rename(source, dest)

old_dir = get_dir("Select Source Directory")

new_dir = get_dir("Select Destination Directory")

check_duplicates = not old_dir == new_dir

os.makedirs(new_dir, exist_ok=True)
file_paths = list(os.path.join(old_dir, file) for file in os.listdir(old_dir))
files = list(filter(os.path.isfile, file_paths))
file_names = list(os.path.basename(file) for file in files)

if messagebox.askyesno(None, "Do you want to add a new Prefix?"):
    prefix = get_prefix()
    file_exts = list(os.path.splitext(file)[1] for file in files)
    new_file_paths = list(os.path.join(new_dir, f"{prefix}_{i}{file_ext}" )for i,file_ext in enumerate(file_exts))
else:
    new_file_paths = list(os.path.join(new_dir, file_name) for file_name in file_names)

src_dest = list(zip(files, new_file_paths))

update_dir(src_dest)