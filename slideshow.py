#
import os
import glob
from tkinter import Tk, Label, PhotoImage

def load_images(image_folder, file_types):
    images = []
    for file_type in file_types:
        images.extend(glob.glob(os.path.join(image_folder, file_type)))
    return images

def slideshow(images, delay, window, current_index=0):
    if current_index < len(images):
        image_path = images[current_index]
        image = PhotoImage(file=image_path)
        label = Label(window, image=image)
        label.pack()
        window.update()
        window.after(delay, lambda: close_and_continue(window, label, image, images, delay, current_index + 1))
    else:
        window.destroy()

def close_and_continue(window, label, image, images, delay, current_index):
    label.pack_forget()
    image.__del__()
    window.update()
    slideshow(images, delay, window, current_index)

def main():

    image_folder = './results/stec/'
    file_types = ['Hanoi*.png']  # 拡張子に注意

    delay = 2000  # スライドショーの表示時間（ミリ秒）

    images = load_images(image_folder, file_types)

    root = Tk()
    root.title("スライドショー")

    slideshow(images, delay, root)

    root.mainloop()

if __name__ == "__main__":
    main()
