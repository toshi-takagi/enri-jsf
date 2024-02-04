import tkinter as tk
import os
import glob

class ImageLabelingApp:
    def __init__(self, root, image_dir, file_pattern):
        self.root = root
        self.root.title("Image Labeling App")

        self.label = tk.Label(self.root, text="Press 'd' for Day, 'n' for Night, 'q' for Quiet, 'x' for Bad, 'e' to Quit")
        self.label.pack(pady=10)

        self.image_dir = image_dir
        self.file_pattern = file_pattern
        self.result_dict = {}

        self.load_existing_results()  # 先に結果を読み込む
        self.image_files = self.get_matching_files()
        self.current_image_index = 0

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.root.bind("<Key>", self.key_pressed)

        self.show_next_image()

    def get_matching_files(self):
        pattern = os.path.join(self.image_dir, self.file_pattern)
        return sorted([os.path.basename(file) for file in glob.glob(pattern) if os.path.basename(file) not in self.result_dict])

    def load_existing_results(self):
        if os.path.exists("status.txt"):
            with open("status.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        filename, label = parts
                        self.result_dict[filename] = label

    def save_results_to_file(self):
        with open("status.txt", "w") as file:
            for filename, label in sorted(self.result_dict.items()):
                file.write(f"{filename} {label}\n")

    def show_next_image(self):
        if self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.image_dir, self.image_files[self.current_image_index])
            image = tk.PhotoImage(file=image_path)
            self.image_label.configure(image=image)
            self.image_label.image = image
            filename = self.image_files[self.current_image_index]
            self.label.configure(text=f"Press 'd' for Day, 'n' for Night, 'q' for Quiet, 'x' for Bad, 'e' to Quit\nCurrent Image: {filename}")
        else:
            self.save_results_to_file()
            self.label.configure(text="All images labeled. Press 'E' to quit.")
            self.root.unbind("<Key>")
            self.root.bind("<Key>", self.quit_application)

    def key_pressed(self, event):
        key = event.char.lower()

        if key in ['d', 'n', 'q', 'x']:
            filename = self.image_files[self.current_image_index]
            label = self.get_label_description(key)
            self.result_dict[filename] = label

            self.current_image_index += 1
            self.show_next_image()
        elif key == 'e':
            self.save_results_to_file()
            self.root.destroy()

    def quit_application(self, event):
        if event.char.lower() == 'e':
            self.save_results_to_file()
            self.root.destroy()

    def get_label_description(self, key):
        if key == 'd':
            return 'Day'
        elif key == 'n':
            return 'Night'
        elif key == 'q':
            return 'Quiet'
        elif key == 'x':
            return 'Bad'
        else:
            return ''


def main():
    image_directory = "results/stec/"
    file_pattern = "Hanoi*.png"

    root = tk.Tk()
    app = ImageLabelingApp(root, image_directory, file_pattern)
    root.mainloop()

if __name__ == "__main__":
    main()
    print('Results are stored in status.txt')



