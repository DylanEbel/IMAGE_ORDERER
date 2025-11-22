import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class CropTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Move Crop Box (600x800)")
        self.canvas = tk.Canvas(root, cursor="fleur")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.image_path = None
        self.tk_img = None
        self.crop_box = None
        self.rect = None

        self.crop_w = 600
        self.crop_h = 800

        self.drag_start = None

        self.create_menu()

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Crop and Save", command=self.save_crop)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not file_path:
            return

        img = Image.open(file_path)
        width, height = img.size

        if width < self.crop_w or height < self.crop_h:
            messagebox.showerror(
                "Image Too Small",
                f"Selected image is {width}x{height}. It must be at least {self.crop_w}x{self.crop_h} pixels."
            )
            return

        self.image = img
        self.image_path = file_path
        self.display_image()

    def display_image(self):
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")
        self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        img_w, img_h = self.image.size
        x0 = (img_w - self.crop_w) // 2
        y0 = (img_h - self.crop_h) // 2
        x1 = x0 + self.crop_w
        y1 = y0 + self.crop_h
        self.rect = self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2)
        self.crop_box = (x0, y0, x1, y1)

    def start_drag(self, event):
        if not self.rect:
            return
        self.drag_start = (event.x, event.y)

    def do_drag(self, event):
        if not self.image or not self.drag_start:
            return

        dx = event.x - self.drag_start[0]
        dy = event.y - self.drag_start[1]

        x0, y0, x1, y1 = self.crop_box
        new_x0 = x0 + dx
        new_y0 = y0 + dy
        new_x1 = x1 + dx
        new_y1 = y1 + dy

        # Keep the crop box inside image boundaries
        img_w, img_h = self.image.size
        if new_x0 < 0:
            new_x1 -= new_x0
            new_x0 = 0
        if new_y0 < 0:
            new_y1 -= new_y0
            new_y0 = 0
        if new_x1 > img_w:
            new_x0 -= (new_x1 - img_w)
            new_x1 = img_w
        if new_y1 > img_h:
            new_y0 -= (new_y1 - img_h)
            new_y1 = img_h

        self.crop_box = (new_x0, new_y0, new_x1, new_y1)
        self.canvas.coords(self.rect, self.crop_box)
        self.drag_start = (event.x, event.y)

    def save_crop(self):
        if not self.image or not self.crop_box:
            messagebox.showerror("Error", "No image loaded or crop area selected.")
            return

        left, top, right, bottom = [int(v) for v in self.crop_box]
        cropped = self.image.crop((left, top, right, bottom))
        cropped = cropped.resize((self.crop_w, self.crop_h))

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(self.image_path)
        name, _ = os.path.splitext(base_name)
        output_path = os.path.join(output_dir, f"cropped_{name}.jpg")

        cropped.save(output_path)
        messagebox.showinfo("Saved", f"Cropped image saved to:\n{output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CropTool(root)
    root.mainloop()
