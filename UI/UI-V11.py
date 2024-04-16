import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess  # Import subprocess for launching external Python scripts

def show_image(path, target_canvas):
    img = Image.open(path)
    target_canvas.update_idletasks()
    canvas_width = target_canvas.winfo_width()
    canvas_height = target_canvas.winfo_height()
    img_width, img_height = img.size
    scaling_factor = min(canvas_width / img_width, canvas_height / img_height)
    new_width = int(img_width * scaling_factor)
    new_height = int(img_height * scaling_factor)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)
    target_canvas.img_photo = img_photo  # Keep reference to prevent garbage collection
    x = (canvas_width - new_width) // 2
    y = (canvas_height - new_height) // 2
    target_canvas.create_image(x, y, anchor="nw", image=img_photo)
    target_canvas.config(scrollregion=target_canvas.bbox("all"))

def import_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        show_image(file_path, canvas)  # Use the canvas from the first tab

def import_images():
    file_paths = filedialog.askopenfilenames()  # Changed to askopenfilenames for multiple files
    if file_paths:
        listbox.delete(0, tk.END)  # Clear previous entries
        for path in file_paths:
            listbox.insert(tk.END, path)  # Add file path to the listbox
#            show_image(path, tab3_canvas)  # Show image on the third tab's canvas

def load_specific_file(text_widget, filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.INSERT, content)
    except FileNotFoundError:
        text_widget.insert(tk.INSERT, "Le fichier spécifié n'a pas été trouvé.")

def run_external_script():
    subprocess.run(["python", "TesseractOCR.py"])

def run_external_script():
    subprocess.run(["python", "Sys_exp.py"])

root = tk.Tk()
root.geometry('1368x768')
root.title("ProjectL2")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)  # New tab for Importing Images
tab4 = ttk.Frame(tab_control)  # New tab for Expert System
tab_control.add(tab1, text='Affichage Image')
tab_control.add(tab2, text='Traduction')
tab_control.add(tab3, text='Importer des images')
tab_control.add(tab4, text='Système expert')
tab_control.pack(expand=1, fill='both')

# Gestion des boutons dans la barre général
#*****************************************************************************************

top_buttons_frame = tk.Frame(root)
top_buttons_frame.pack(side='top', fill='x', padx=10, pady=10)

btn_load_file1 = tk.Button(top_buttons_frame, text='Actualiser extractionTesseractOCR', command=lambda: load_specific_file(text_widget1, "extractionTesseractOCR"))
btn_load_file1.pack(side='left', padx=5)

btn_load_file2 = tk.Button(top_buttons_frame, text='Actualiser Traduction', command=lambda: load_specific_file(text_widget2, "Traduction"))
btn_load_file2.pack(side='left', padx=5)

btn_run_script = tk.Button(top_buttons_frame, text='Exécuter Script Externe', command=run_external_script)
btn_run_script.pack(side='left', padx=5)

btn_run_script = tk.Button(top_buttons_frame, text='Exécuter Système expert', command=run_external_script)
btn_run_script.pack(side='left', padx=5)

#*****************************************************************************************

# Setup for the 'Affichage Image' tab
#*****************************************************************************************
image_frame = tk.Frame(tab1)
image_frame.pack(side='top', fill='both', expand=True)

canvas = tk.Canvas(image_frame)
canvas.pack(side="right", fill="both", expand=True)


btn_import_image = tk.Button(image_frame, text='Importer Image', command=import_image)
btn_import_image.pack(side='left', padx=10, pady=10)

#*****************************************************************************************

# Setup for the 'Importer des images' tab
#*****************************************************************************************

#tab3_canvas = tk.Canvas(tab3)
#tab3_canvas.pack(fill="both", expand=True)

btn_import_images = tk.Button(tab3, text='Importer Images', command=import_images)
btn_import_images.pack(side='top', pady=5)

listbox = tk.Listbox(tab3, height=5)
listbox.pack(fill='both', expand=True)

#*****************************************************************************************

# Configuration for text widgets in 'Traduction' tab
#*****************************************************************************************

frame = ttk.Frame(tab2)
frame.pack(fill='both', expand=True)

# Text Widget 1 with Scrollbar
frame_text1 = ttk.Frame(frame)
frame_text1.pack(side='left', fill='both', expand=True)
text_widget1 = tk.Text(frame_text1, height=15, width=50)
scroll_y1 = tk.Scrollbar(frame_text1, orient="vertical", command=text_widget1.yview)
text_widget1.configure(yscrollcommand=scroll_y1.set)
text_widget1.pack(side='left', fill='both', expand=True)
scroll_y1.pack(side='right', fill='y')

# Text Widget 2 with Scrollbar
frame_text2 = ttk.Frame(frame)
frame_text2.pack(side='left', fill='both', expand=True)
text_widget2 = tk.Text(frame_text2, height=15, width=50)
scroll_y2 = tk.Scrollbar(frame_text2, orient="vertical", command=text_widget2.yview)
text_widget2.configure(yscrollcommand=scroll_y2.set)
text_widget2.pack(side='left', fill='both', expand=True)
scroll_y2.pack(side='right', fill='y')
#*****************************************************************************************

root.mainloop()
