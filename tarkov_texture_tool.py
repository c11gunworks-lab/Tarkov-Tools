import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageOps
import os

class TextureToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Texture Toolbox")
        self.root.geometry("400x540") # Increased height slightly to fit the stacked buttons
        self.root.resizable(False, False)

        # UI Styling
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabelframe", padding=10)

        # Main Title
        lbl_title = tk.Label(root, text="Texture Modding Toolkit", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        # --- SECTION 1: SPLITTING & UNPACKING ---
        lf_split = ttk.LabelFrame(root, text="Channel Splitters")
        lf_split.pack(fill="x", padx=15, pady=5)

        # ORM/RMA Radio Buttons (STACKED VERTICALLY SO THEY DON'T CUT OFF)
        self.mode_var = tk.StringVar(value="ORM")
        frame_radios = tk.Frame(lf_split)
        frame_radios.pack(pady=5)
        tk.Radiobutton(frame_radios, text="ORM (R=AO, G=Rough, B=Metal)", variable=self.mode_var, value="ORM").pack(anchor=tk.W)
        tk.Radiobutton(frame_radios, text="RMA (R=Rough, G=Metal, B=AO)", variable=self.mode_var, value="RMA").pack(anchor=tk.W)
        
        ttk.Button(lf_split, text="1. Split ORM / RMA Textures", command=self.process_orm_rma).pack(fill="x", pady=2)
        ttk.Button(lf_split, text="2. Split Diffuse (RGBA ➔ RGB + Spec)", command=self.process_diffuse).pack(fill="x", pady=(8, 2))

        # --- SECTION 2: NORMAL MAP TOOLS ---
        lf_normals = ttk.LabelFrame(root, text="Normal Map Converters")
        lf_normals.pack(fill="x", padx=15, pady=10)

        ttk.Button(lf_normals, text="3. DirectX ↔ OpenGL (Batch Invert Y-Axis)", command=self.process_dx_gl).pack(fill="x", pady=2)
        ttk.Button(lf_normals, text="4. Unity/Tarkov Normals (Red ➔ Blue)", command=self.process_tarkov_normals).pack(fill="x", pady=(8, 2))

        # --- SECTION 3: IMAGE TRANSFORMATIONS ---
        lf_utils = ttk.LabelFrame(root, text="Image Transformations")
        lf_utils.pack(fill="x", padx=15, pady=5)

        ttk.Button(lf_utils, text="5. Vertical Texture Flipper (Select Folder)", command=self.process_flipper).pack(fill="x", pady=2)

        # --- STATUS BAR ---
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(root, textvariable=self.status_var, fg="gray", font=("Arial", 9))
        self.status_label.pack(side=tk.BOTTOM, pady=15)

    def update_status(self, text):
        self.status_var.set(text)
        self.root.update()

    # ==========================================
    # TOOL 1: ORM / RMA SPLITTER
    # ==========================================
    def process_orm_rma(self):
        mode = self.mode_var.get()
        files = filedialog.askopenfilenames(title=f"Select {mode} Textures", filetypes=[("Image Files", "*.png *.tga *.jpg *.jpeg *.tiff")])
        if not files: return

        self.update_status(f"Processing {len(files)} {mode} files...")
        success_count = 0

        for filepath in files:
            try:
                with Image.open(filepath) as img:
                    img = img.convert('RGB')
                    r, g, b = img.split()

                    if mode == "ORM":
                        ao_img, rough_img, metal_img = r, g, b
                    else: # RMA
                        rough_img, metal_img, ao_img = r, g, b

                    directory, filename = os.path.split(filepath)
                    name, ext = os.path.splitext(filename)

                    ao_img.save(os.path.join(directory, f"{name}_AO.png"))
                    rough_img.save(os.path.join(directory, f"{name}_Roughness.png"))
                    metal_img.save(os.path.join(directory, f"{name}_Metallic.png"))
                    success_count += 1
            except Exception as e:
                print(f"Error splitting {filepath}: {e}")

        self.update_status("Ready")
        messagebox.showinfo("Complete", f"Successfully split {success_count} {mode} files.")

    # ==========================================
    # TOOL 2: DIFFUSE SPLITTER
    # ==========================================
    def process_diffuse(self):
        files = filedialog.askopenfilenames(title="Select RGBA Diffuse Textures", filetypes=[("Image Files", "*.png *.tga *.tiff")])
        if not files: return

        self.update_status(f"Splitting {len(files)} Diffuse files...")
        success_count = 0

        for filepath in files:
            try:
                with Image.open(filepath) as img:
                    if img.mode != 'RGBA':
                        continue # Skip if no alpha

                    r, g, b, a = img.split()
                    directory, filename = os.path.split(filepath)
                    name, ext = os.path.splitext(filename)

                    # Save Base Color and Specular
                    Image.merge('RGB', (r, g, b)).save(os.path.join(directory, f"{name}_BaseColor.png"))
                    a.save(os.path.join(directory, f"{name}_Specular.png"))
                    success_count += 1
            except Exception as e:
                print(f"Error splitting diffuse {filepath}: {e}")

        self.update_status("Ready")
        messagebox.showinfo("Complete", f"Successfully split {success_count} Diffuse files.")

    # ==========================================
    # TOOL 3: DIRECTX ↔ OPENGL (BATCH INVERT GREEN)
    # ==========================================
    def process_dx_gl(self):
        files = filedialog.askopenfilenames(title="Select Normal Maps to Invert", filetypes=[("Image Files", "*.png *.tga *.jpg *.jpeg *.bmp *.tiff")])
        if not files: return

        self.update_status(f"Inverting Y-Axis for {len(files)} Normal maps...")
        success_count = 0

        for filepath in files:
            try:
                with Image.open(filepath) as img:
                    # Convert to RGBA to be safe and extract bands
                    if img.mode not in ('RGB', 'RGBA'):
                        img = img.convert('RGBA')
                    
                    bands = img.split()
                    r, g, b = bands[0], bands[1], bands[2]
                    
                    # Invert the Green Channel
                    g = ImageOps.invert(g)

                    # Recombine
                    if len(bands) >= 4:
                        new_img = Image.merge("RGBA", (r, g, b, bands[3]))
                    else:
                        new_img = Image.merge("RGB", (r, g, b))

                    # Save file with a suffix automatically
                    directory, filename = os.path.split(filepath)
                    name, ext = os.path.splitext(filename)
                    new_img.save(os.path.join(directory, f"{name}_InvertedY{ext}"))
                    
                    success_count += 1
            except Exception as e:
                print(f"Error inverting {filepath}: {e}")

        self.update_status("Ready")
        messagebox.showinfo("Complete", f"Successfully inverted {success_count} Normal maps.\nSaved alongside originals with '_InvertedY'.")

    # ==========================================
    # TOOL 4: TARKOV / UNITY NORMALS
    # ==========================================
    def process_tarkov_normals(self):
        files = filedialog.askopenfilenames(title="Select Unity Normals", filetypes=[("Image Files", "*.png *.tga *.tiff")])
        if not files: return

        self.update_status(f"Converting {len(files)} Unity Normals...")
        success_count = 0

        for filepath in files:
            try:
                with Image.open(filepath) as img:
                    img = img.convert('RGBA')
                    r, g, b, a = img.split()

                    # Reconstruct Z as White, Move Alpha to Red
                    z_channel = Image.new('L', img.size, 255)
                    new_normal = Image.merge('RGB', (a, g, z_channel))

                    directory, filename = os.path.split(filepath)
                    name, ext = os.path.splitext(filename)
                    new_normal.save(os.path.join(directory, f"{name}_Normal_OpenGL.png"))
                    
                    success_count += 1
            except Exception as e:
                print(f"Error on Unity Normal {filepath}: {e}")

        self.update_status("Ready")
        messagebox.showinfo("Complete", f"Successfully converted {success_count} Unity Normal maps.")

    # ==========================================
    # TOOL 5: VERTICAL FLIPPER (FOLDER)
    # ==========================================
    def process_flipper(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Flip Vertically")
        if not folder_path: return

        output_dir = os.path.join(folder_path, "Vertically_Flipped")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        valid_exts = (".png", ".tga", ".jpg", ".jpeg", ".bmp", ".tiff")
        success_count = 0
        
        files_to_process = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts)]
        self.update_status(f"Flipping {len(files_to_process)} images in folder...")

        for filename in files_to_process:
            file_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(file_path)
                flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                flipped_img.save(os.path.join(output_dir, filename))
                success_count += 1
            except Exception as e:
                print(f"Error flipping {filename}: {e}")

        self.update_status("Ready")
        messagebox.showinfo("Complete", f"Flipped {success_count} images.\nSaved to a new 'Vertically_Flipped' folder inside the chosen directory.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextureToolboxApp(root)
    root.mainloop()