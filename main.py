
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import cv2
import numpy as np

# ----------------------- Core Functions -----------------------
MAX_PREVIEW = 400  # maximum width/height for preview images

def open_image():
    global img, filtered_img, original_preview, filtered_preview
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if not path:
        return
    try:
        img = Image.open(path)
        filtered_img = img.copy()
        original_preview = create_preview(img)
        filtered_preview = create_preview(filtered_img)
        display_images()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")

def save_image():
    global filtered_img
    if filtered_img is None:
        messagebox.showinfo("Info", "No filtered image to save!")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if path:
        filtered_img.save(path)
        messagebox.showinfo("Saved", f"Image saved at {path}")

def create_preview(image):
    """Resize image for preview keeping aspect ratio."""
    img_width, img_height = image.size
    ratio = min(MAX_PREVIEW / img_width, MAX_PREVIEW / img_height, 1)
    new_size = (int(img_width * ratio), int(img_height * ratio))
    return image.resize(new_size, Image.Resampling.LANCZOS)

def display_images():
    """Display original and filtered images side by side."""
    global tk_original, tk_filtered
    canvas.delete("all")
    if original_preview:
        tk_original = ImageTk.PhotoImage(original_preview)
        canvas.create_image(0, 0, anchor="nw", image=tk_original)
    if filtered_preview:
        tk_filtered = ImageTk.PhotoImage(filtered_preview)
        canvas.create_image(MAX_PREVIEW + 20, 0, anchor="nw", image=tk_filtered)
    canvas.config(scrollregion=canvas.bbox("all"))

# ----------------------- Filters -----------------------
def apply_grayscale():
    global filtered_img, filtered_preview
    if img:
        filtered_img = img.convert("L").convert("RGB")
        filtered_preview = create_preview(filtered_img)
        display_images()

def apply_blur():
    global filtered_img, filtered_preview
    if img:
        filtered_img = img.filter(ImageFilter.BLUR)
        filtered_preview = create_preview(filtered_img)
        display_images()

def apply_edge():
    global filtered_img, filtered_preview
    if img:
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        edges = cv2.Canny(cv_img, 100, 200)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        filtered_img = Image.fromarray(edges)
        filtered_preview = create_preview(filtered_img)
        display_images()

def apply_sepia():
    global filtered_img, filtered_preview
    if img:
        cv_img = np.array(img)
        tr = 0.393 * cv_img[:,:,0] + 0.769 * cv_img[:,:,1] + 0.189 * cv_img[:,:,2]
        tg = 0.349 * cv_img[:,:,0] + 0.686 * cv_img[:,:,1] + 0.168 * cv_img[:,:,2]
        tb = 0.272 * cv_img[:,:,0] + 0.534 * cv_img[:,:,1] + 0.131 * cv_img[:,:,2]
        sepia_img = np.clip(np.stack([tr, tg, tb], axis=2), 0, 255).astype(np.uint8)
        filtered_img = Image.fromarray(sepia_img)
        filtered_preview = create_preview(filtered_img)
        display_images()

def adjust_brightness(factor=1.2):
    global filtered_img, filtered_preview
    if img:
        filtered_img = ImageEnhance.Brightness(img).enhance(factor)
        filtered_preview = create_preview(filtered_img)
        display_images()

def adjust_contrast(factor=1.5):
    global filtered_img, filtered_preview
    if img:
        filtered_img = ImageEnhance.Contrast(img).enhance(factor)
        filtered_preview = create_preview(filtered_img)
        display_images()

# ----------------------- GUI Setup -----------------------
root = tk.Tk()
root.title("Image Filter App - Original vs Edited")
root.geometry("900x500")

img = None
filtered_img = None
original_preview = None
filtered_preview = None
tk_original = None
tk_filtered = None

# Left frame for buttons
btn_frame = tk.Frame(root)
btn_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

tk.Button(btn_frame, text="Open Image", command=open_image, width=20).pack(pady=5)
tk.Button(btn_frame, text="Save Image", command=save_image, width=20).pack(pady=5)
tk.Label(btn_frame, text="Filters", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(btn_frame, text="Grayscale", command=apply_grayscale, width=20).pack(pady=5)
tk.Button(btn_frame, text="Blur", command=apply_blur, width=20).pack(pady=5)
tk.Button(btn_frame, text="Edge Detection", command=apply_edge, width=20).pack(pady=5)
tk.Button(btn_frame, text="Sepia", command=apply_sepia, width=20).pack(pady=5)
tk.Button(btn_frame, text="Brightness +20%", command=lambda: adjust_brightness(1.2), width=20).pack(pady=5)
tk.Button(btn_frame, text="Contrast +50%", command=lambda: adjust_contrast(1.5), width=20).pack(pady=5)

# Right frame for canvas
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvas_frame, bg="gray", width=2*MAX_PREVIEW+50, height=MAX_PREVIEW)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
