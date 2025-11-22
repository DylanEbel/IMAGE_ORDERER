import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class CropTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crop Tool - 600x800")
        
        # Crop box dimensions (fixed)
        self.crop_width = 600
        self.crop_height = 800
        
        # Variables for image handling
        self.original_image = None
        self.display_image = None
        self.photo = None
        self.cropped_image = None
        
        # Crop box position (top-left corner)
        self.crop_x = 0
        self.crop_y = 0
        
        # Display scaling
        self.scale_factor = 1.0
        self.display_width = 0
        self.display_height = 0
        
        # Drag tracking
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Top frame for buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Upload button
        self.upload_btn = tk.Button(
            top_frame, 
            text=" Upload Image", 
            command=self.upload_image,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Crop button
        self.crop_btn = tk.Button(
            top_frame,
            text=" Crop & Save",
            command=self.crop_and_save,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.crop_btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        self.info_label = tk.Label(
            top_frame,
            text="Upload an image to begin",
            font=("Arial", 10),
            fg="#666"
        )
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # Canvas for image display
        self.canvas = tk.Canvas(
            self.root,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Crop box rectangle (will be created when image is loaded)
        self.crop_rect = None
        
    def upload_image(self):
        """Open file dialog and load selected image"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            # Load the original image
            self.original_image = Image.open(file_path)
            
            # Check if image is large enough
            if (self.original_image.width < self.crop_width or 
                self.original_image.height < self.crop_height):
                messagebox.showwarning(
                    "Image Too Small",
                    f"Image must be at least {self.crop_width}x{self.crop_height} pixels.\n"
                    f"Your image is {self.original_image.width}x{self.original_image.height} pixels."
                )
                return
            
            # Display the image
            self.display_image_on_canvas()
            
            # Enable crop button
            self.crop_btn.config(state=tk.NORMAL)
            
            # Update instructions
            self.info_label.config(
                text=f"Drag the box to position your crop area | Image: {self.original_image.width}x{self.original_image.height}px"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def display_image_on_canvas(self):
        """Display the image on canvas with crop box overlay"""
        if not self.original_image:
            return
        
        # Get canvas dimensions
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate scaling to fit image in canvas
        img_width = self.original_image.width
        img_height = self.original_image.height
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        self.scale_factor = min(scale_x, scale_y, 1.0)  # Don't scale up
        
        self.display_width = int(img_width * self.scale_factor)
        self.display_height = int(img_height * self.scale_factor)
        
        # Resize image for display
        self.display_image = self.original_image.resize(
            (self.display_width, self.display_height),
            Image.Resampling.LANCZOS
        )
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(self.display_image)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Center image on canvas
        x_offset = (canvas_width - self.display_width) // 2
        y_offset = (canvas_height - self.display_height) // 2
        
        # Draw image
        self.canvas.create_image(
            x_offset, y_offset,
            image=self.photo,
            anchor=tk.NW,
            tags="image"
        )
        
        # Initialize crop box position (centered)
        scaled_crop_width = int(self.crop_width * self.scale_factor)
        scaled_crop_height = int(self.crop_height * self.scale_factor)
        
        self.crop_x = x_offset + (self.display_width - scaled_crop_width) // 2
        self.crop_y = y_offset + (self.display_height - scaled_crop_height) // 2
        
        # Draw crop box
        self.draw_crop_box()
        
    def draw_crop_box(self):
        """Draw the crop box rectangle on canvas"""
        # Delete old crop box if exists
        self.canvas.delete("cropbox")
        self.canvas.delete("overlay")
        
        # Get image bounds
        img_bounds = self.canvas.bbox("image")
        if not img_bounds:
            return
            
        img_x1, img_y1, img_x2, img_y2 = img_bounds
        
        # Calculate scaled crop dimensions
        scaled_crop_width = int(self.crop_width * self.scale_factor)
        scaled_crop_height = int(self.crop_height * self.scale_factor)
        
        # Constrain crop box within image bounds
        self.crop_x = max(img_x1, min(self.crop_x, img_x2 - scaled_crop_width))
        self.crop_y = max(img_y1, min(self.crop_y, img_y2 - scaled_crop_height))
        
        # Calculate crop box corners
        x1 = self.crop_x
        y1 = self.crop_y
        x2 = x1 + scaled_crop_width
        y2 = y1 + scaled_crop_height
        
        # Draw semi-transparent overlay outside crop box
        self.canvas.create_rectangle(
            img_x1, img_y1, img_x2, y1,
            fill="black", stipple="gray50", tags="overlay"
        )  # Top
        self.canvas.create_rectangle(
            img_x1, y2, img_x2, img_y2,
            fill="black", stipple="gray50", tags="overlay"
        )  # Bottom
        self.canvas.create_rectangle(
            img_x1, y1, x1, y2,
            fill="black", stipple="gray50", tags="overlay"
        )  # Left
        self.canvas.create_rectangle(
            x2, y1, img_x2, y2,
            fill="black", stipple="gray50", tags="overlay"
        )  # Right
        
        # Draw crop box border
        self.crop_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="#00FF00",
            width=3,
            tags="cropbox"
        )
        
        # Add corner markers
        marker_size = 10
        self.canvas.create_rectangle(
            x1-marker_size, y1-marker_size, x1+marker_size, y1+marker_size,
            fill="#00FF00", outline="white", tags="cropbox"
        )  # Top-left
        self.canvas.create_rectangle(
            x2-marker_size, y1-marker_size, x2+marker_size, y1+marker_size,
            fill="#00FF00", outline="white", tags="cropbox"
        )  # Top-right
        self.canvas.create_rectangle(
            x1-marker_size, y2-marker_size, x1+marker_size, y2+marker_size,
            fill="#00FF00", outline="white", tags="cropbox"
        )  # Bottom-left
        self.canvas.create_rectangle(
            x2-marker_size, y2-marker_size, x2+marker_size, y2+marker_size,
            fill="#00FF00", outline="white", tags="cropbox"
        )  # Bottom-right
        
        # Add dimension label
        self.canvas.create_text(
            (x1 + x2) // 2, y1 - 15,
            text=f"{self.crop_width}x{self.crop_height}px",
            fill="#00FF00",
            font=("Arial", 12, "bold"),
            tags="cropbox"
        )
        
    def on_mouse_down(self, event):
        """Handle mouse button press"""
        if not self.crop_rect:
            return
            
        # Check if click is inside crop box
        coords = self.canvas.coords(self.crop_rect)
        if coords:
            x1, y1, x2, y2 = coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.dragging = True
                self.drag_start_x = event.x - self.crop_x
                self.drag_start_y = event.y - self.crop_y
                self.canvas.config(cursor="fleur")
    
    def on_mouse_drag(self, event):
        """Handle mouse drag motion"""
        if self.dragging:
            self.crop_x = event.x - self.drag_start_x
            self.crop_y = event.y - self.drag_start_y
            self.draw_crop_box()
    
    def on_mouse_up(self, event):
        """Handle mouse button release"""
        self.dragging = False
        self.canvas.config(cursor="")
    
    def crop_and_save(self):
        """Crop the image and save it locally"""
        if not self.original_image or not self.crop_rect:
            return
        
        try:
            # Get image bounds on canvas
            img_bounds = self.canvas.bbox("image")
            if not img_bounds:
                return
            img_x1, img_y1, _, _ = img_bounds
            
            # Calculate crop coordinates in original image space
            # Convert from display coordinates to original image coordinates
            crop_x_original = int((self.crop_x - img_x1) / self.scale_factor)
            crop_y_original = int((self.crop_y - img_y1) / self.scale_factor)
            
            # Ensure coordinates are within bounds
            crop_x_original = max(0, crop_x_original)
            crop_y_original = max(0, crop_y_original)
            
            # Calculate crop box in original image
            x1 = crop_x_original
            y1 = crop_y_original
            x2 = min(x1 + self.crop_width, self.original_image.width)
            y2 = min(y1 + self.crop_height, self.original_image.height)
            
            # Crop the image
            self.cropped_image = self.original_image.crop((x1, y1, x2, y2))
            
            # Create output directory if it doesn't exist
            output_dir = "cropped_images"
            os.makedirs(output_dir, exist_ok=True)
            
            # Save the cropped image
            output_path = os.path.join(output_dir, "cropped_image.png")
            self.cropped_image.save(output_path)
            
            messagebox.showinfo(
                "Success",
                f"Image cropped and saved to:\n{os.path.abspath(output_path)}\n\n"
                f"Dimensions: {self.cropped_image.width}x{self.cropped_image.height}px"
            )
            
            # Update info label
            self.info_label.config(
                text=f"✓ Cropped image saved! ({self.cropped_image.width}x{self.cropped_image.height}px)"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to crop image:\n{str(e)}")


def main():
    """Main function to run the crop tool"""
    root = tk.Tk()
    root.geometry("1000x900")
    root.minsize(800, 700)
    
    app = CropTool(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()

