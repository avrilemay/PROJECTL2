import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global original_image, img, displayed_image
        original_image = Image.open(file_path)
        displayed_image = original_image.copy()
        img = ImageTk.PhotoImage(displayed_image)
        canvas.create_image(0, 0, anchor='nw', image=img)
        canvas.image = img  # Garder une référence.
        line_coordinates.clear()
        update_coordinates_display()

def start_line(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def draw_line(event):
    global end_x, end_y
    end_x = event.x
    end_y = event.y
    # Temporarily redraw the image to show the line
    temp_image = displayed_image.copy()
    draw = ImageDraw.Draw(temp_image)
    draw.line((start_x, start_y, end_x, end_y), fill='red', width=2)
    img = ImageTk.PhotoImage(temp_image)
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.image = img

def finish_line(event):
    # Save line to image and list
    global displayed_image
    draw = ImageDraw.Draw(displayed_image)
    draw.line((start_x, start_y, end_x, end_y), fill='red', width=2)
    line_coordinates.append((start_x, start_y, end_x, end_y))
    update_coordinates_display()
    img = ImageTk.PhotoImage(displayed_image)
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.image = img

def update_coordinates_display():
    # Update the text displaying coordinates
    coordinates_text = "\n".join(f"Coordonnées 'x1''y1'({x1}, {y1}) vers 'x2''y2'({x2}, {y2})"
                                 for x1, y1, x2, y2 in line_coordinates)
    coordinates_display.config(text=coordinates_text)

# Initialiser tkinter
root = tk.Tk()
canvas = tk.Canvas(root, width=1300, height=700, bg='gray')
canvas.pack()
canvas.bind("<Button-1>", start_line)
canvas.bind("<B1-Motion>", draw_line)
canvas.bind("<ButtonRelease-1>", finish_line)

open_button = tk.Button(root, text="Ouvrir image", command=open_image)
open_button.pack()

coordinates_display = tk.Label(root, text="", justify=tk.LEFT)
coordinates_display.pack()

line_coordinates = []  # Store line coordinates
displayed_image = None  # Displayed image with permanent lines

root.mainloop()
