import tkinter as tk
from tkinter import filedialog
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
        self.root.title("Grayscale Image Processing")
        self.root.configure(bg='#2e2e2e')

        self.canvas = tk.Canvas(root, width=1100, height=700, bg='#2e2e2e', highlightthickness=0)
        self.canvas.pack()

        self.button_frame = tk.Frame(root, bg='#2e2e2e')
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.upload_btn = tk.Button(
            self.button_frame, text="Upload Image", command=self.upload_image,
            font=("Helvetica", 14, "bold"), bg="#26C4D3", fg="black",
            padx=20, pady=10, width=15
        )
        self.upload_btn.pack(side=tk.LEFT, padx=30)

        self.save_btn = tk.Button(
            self.button_frame, text="Save Outputs", command=self.save_images,
            font=("Helvetica", 14, "bold"), bg="#21F391", fg="black",
            padx=20, pady=10, width=15
        )
        self.save_btn.pack(side=tk.RIGHT, padx=30)

        self.processed_images = []
        self.image_name = ""

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image_name = os.path.splitext(os.path.basename(file_path))[0]
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

        # Display images
        self.canvas.delete("all")
        for i, (img, title) in enumerate(zip(self.processed_images, titles)):
            img_pil = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(img_pil.resize((250, 250)))
            x_offset = 50 + (i % 3) * 350
            y_offset = 30 + (i // 3) * 310
            border = self.canvas.create_rectangle(x_offset-2, y_offset-2, x_offset+252, y_offset+252, outline="red", width=5)
            self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img_tk)
            self.canvas.create_text(x_offset + 125, y_offset + 270, anchor=tk.CENTER, text=title, fill="white", font=("Helvetica", 18, "bold"))
            setattr(self, f'image_{i}', img_tk)  # Prevent image garbage collection

    def save_images(self):
        if not self.processed_images:
            return

        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        filenames = ["input", "box_blur", "edge_detection", "sharpen", "high_pass", "low_pass"]
        for img, name in zip(self.processed_images, filenames):
            Image.fromarray(img).save(os.path.join(save_dir, f"{self.image_name}_{name}.png"))

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
