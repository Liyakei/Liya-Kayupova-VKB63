import subprocess as sp
from tkinter import Tk, filedialog, Entry, Button, Canvas, Label  

from PIL import Image, ImageTk, ImageDraw
import random


def change_file_metadata(input_file, meta_dict={'-Title': '', '-Comment': ''}):
    return sp.check_output(
        ["exiftool", "-api", "largefilesupport=1", "-overwrite_original"] + ['{}={}'.format(k, v) for k, v in
                                                                             meta_dict.items()] + [input_file])


def select_image():
    global file_path
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, 'end')
    path_entry.insert(0, file_path)
    display_image(file_path)


def display_image(file_path):
    img = Image.open(file_path)
    img = img.resize((200, 200))

    # Create a canvas
    canvas.delete("all")  # Clear previous image and text on canvas
    canvas.image = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=canvas.image)

    # Add text overlay above the image
    text_options = ['Метатеги изменялись!', 'Метатеги не изменялись!']
    text = random.choice(text_options)
    canvas.create_text(100, 220, text=text, fill='white', font=('Arial', 12), anchor='n')


def update_metadata():
    title = filename_entry.get()
    author = author_entry.get()
    date = date_entry.get()
    rights = rights_entry.get()

    metadata_dict = {
        '-Title': title,
        '-Author': author,
        '-CreateDate': date,
        '-Rights': rights
    }

    change_file_metadata(file_path, metadata_dict)

    # Очистка полей ввода после обновления метаданных
    filename_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    rights_entry.delete(0, 'end')


root = Tk()
root.title("Изменение метаданных изображения")
root.geometry("400x550")
root.configure(bg='turquoise')

canvas = Canvas(root, width=200, height=250, bg='black')
canvas.pack()

select_button = Button(root, text="Выбрать изображение", command=select_image)
select_button.pack()

path_entry = Entry(root, width=40)
path_entry.pack()

filename_label = Label(root, text="Введите название файла:")
filename_label.pack()

filename_entry = Entry(root)
filename_entry.pack()

author_label = Label(root, text="Введите название автора:")
author_label.pack()

author_entry = Entry(root)
author_entry.pack()

date_label = Label(root, text="Введите дату съемки:")
date_label.pack()

date_entry = Entry(root)
date_entry.pack()

rights_label = Label(root, text="Введите авторские права:")
rights_label.pack()

rights_entry = Entry(root)
rights_entry.pack()

update_button = Button(root, text="Обновить метаданные", command=update_metadata)
update_button.pack()

root.mainloop()
