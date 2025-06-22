import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import os

# ================= Image Processing Functions ================= #
def convolve2d(image, kernel):
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    output = np.zeros_like(image)

    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            output[i, j] = np.clip(np.sum(region * kernel), 0, 255)
    return output.astype(np.uint8)

# Filters
def box_blur(img):
    kernel = np.ones((3, 3)) / 9.0
    return convolve2d(img, kernel)

def sobel_edge_detection(img):
    Gx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    Gy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    edge_x = convolve2d(img, Gx).astype(float)
    edge_y = convolve2d(img, Gy).astype(float)
    magnitude = np.sqrt(edge_x**2 + edge_y**2)
    return np.clip(magnitude / magnitude.max() * 255, 0, 255).astype(np.uint8)

def sharpen(img):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return convolve2d(img, kernel)

def high_pass_filter(img):
    kernel = np.array([[-7/9, -7/9, 0], [0, 5, 0], [0, -7/9, -7/9]])
    return convolve2d(img, kernel)

def low_pass_filter(img):
    kernel = np.array([[0, 0, 0], [0, 5/9, 0], [0, 0, 0]])
    return convolve2d(img, kernel)

# ================= GUI APP ================= #
class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FPGA Image Processing GUI APP")

        # Force Tkinter to update its internal geometry information
        # This is crucial for getting accurate screen dimensions, especially on multi-monitor setups.
        self.root.update_idletasks()
        
        # Get screen dimensions based on where the window is currently being drawn
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Explicitly set the window's geometry to the full screen size
        # This positions the window at (0,0) and sets its width and height.
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Now, set the fullscreen attribute.
        # With the geometry already set, this often helps the window manager
        # correctly interpret the fullscreen request for the current display.
        self.root.attributes("-fullscreen", True) 

        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and set background image
        try:
            # Construct a path relative to the script's directory
            # This assumes 'Background.png' is inside an 'Image' folder
            # which is in the same directory as this script.
            script_dir = os.path.dirname(__file__)
            bg_path = os.path.join(script_dir, 'Image', 'Background.png')

            # Use Image.LANCZOS instead of Image.ANTIALIAS as it's deprecated
            bg_img = Image.open(bg_path).resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_img)
            self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image, tags="bg")
            self.canvas.tag_lower("bg") # Ensure background is behind other elements
        except Exception as e:
            print(f"Failed to load background image from {bg_path}: {e}")
            # You might want to display a fallback or a message to the user here
            # For example, by setting a default background color.
            self.canvas.config(bg="darkblue") # Fallback background color

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Upload.TButton', font=('Helvetica', 25, 'bold'), foreground='black', background='#26C4D3', padding=10, highlightbackground='black', highlightcolor='white', borderwidth=1.5)
        style.map('Upload.TButton', background=[('active', '#1DAEBE')])
        style.configure('Save.TButton', font=('Helvetica', 25, 'bold'), foreground='black', background='#21F391', padding=10, highlightbackground='black', highlightcolor='white', borderwidth=1.5)
        style.map('Save.TButton', background=[('active', '#1FD382')])

        self.upload_btn = ttk.Button(root, text="Upload Image", style='Upload.TButton', command=self.upload_image)
        self.save_btn = ttk.Button(root, text="Save Outputs", style='Save.TButton', command=self.save_images)

        # Position buttons within the canvas
        # The window argument ensures the Tkinter widget (button) is managed by the canvas
        self.upload_window = self.canvas.create_window(screen_width - 340, 355, window=self.upload_btn, anchor=tk.NW)
        self.save_window = self.canvas.create_window(screen_width - 340, 435, window=self.save_btn, anchor=tk.NW)

        self.processed_images = []
        self.image_name = ""

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image_name = os.path.splitext(os.path.basename(file_path))[0]
        # Ensure the image is converted to grayscale ('L') for processing,
        # but keep a reference to the original for potential color display
        # if you ever expand the app.
        image = Image.open(file_path).convert('L')
        img_array = np.array(image)

        # Apply filters
        blurred = box_blur(img_array)
        edged = sobel_edge_detection(img_array)
        sharpened = sharpen(img_array)
        high_passed = high_pass_filter(img_array)
        low_passed = low_pass_filter(img_array)

        self.processed_images = [img_array, blurred, edged, sharpened, high_passed, low_passed]
        titles = ["Input", "Box Blur", "Edge Detection", "Sharpen", "High Pass", "Low Pass"]

        # Clear previous images from the canvas
        self.canvas.delete("images")

        start_x = 40
        start_y = 260
        gap_x = 320 # Horizontal gap between images
        gap_y = 320 # Vertical gap between image rows

        # Display processed images on the canvas
        for i, (img, title) in enumerate(zip(self.processed_images, titles)):
            img_pil = Image.fromarray(img)
            # Resize image for display to 250x220 pixels
            img_tk = ImageTk.PhotoImage(img_pil.resize((250, 220), Image.LANCZOS))
            
            # Calculate row and column for grid layout
            row = i // 3
            col = i % 3
            x_offset = start_x + col * gap_x
            y_offset = start_y + row * gap_y
            
            # Create the image on the canvas
            self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img_tk, tags="images")
            
        
            # Store a reference to the ImageTk.PhotoImage object to prevent garbage collection
            # If not stored, the image might disappear after the function exits.
            setattr(self, f'image_display_{i}', img_tk)

    def save_images(self):
        if not self.processed_images:
            # Display a message to the user if no images have been processed yet
            print("No images to save. Please upload and process an image first.")
            return

        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        filenames = ["input_image", "box_blur", "edge_detection", "sharpen", "high_pass", "low_pass"]
        for img, name in zip(self.processed_images, filenames):
            save_path = os.path.join(save_dir, f"{self.image_name}_{name}.png")
            try:
                Image.fromarray(img).save(save_path)
                print(f"Saved {save_path}")
            except Exception as e:
                print(f"Failed to save {save_path}: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
