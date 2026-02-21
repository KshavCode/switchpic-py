import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import time
from pathlib import Path

class SwitchPicVanilla:
    def __init__(self, root):
        self.root = root
        self.root.title("SwitchPic - Format Converter")
        self.root.geometry("550x450") 
        self.root.resizable(False, False)
        
        # Set a light gray background for the main window
        self.root.configure(bg="#F3F4F6")

        # --- App State ---
        self.image = None
        self.current_filename = ""
        
        self.format_mapping = {
            "JPEG (.jpg)": ("JPEG", ".jpg"),
            "PNG (.png)": ("PNG", ".png"),
            "ICO (.ico)": ("ICO", ".ico"),
            "WEBP (.webp)": ("WEBP", ".webp"),
            "BMP (.bmp)": ("BMP", ".bmp"),
            "TIFF (.tiff)": ("TIFF", ".tiff")
        }

        self.setup_ui()

    def setup_ui(self):
        # Fonts
        font_title = ("Helvetica", 24, "bold")
        font_sub = ("Helvetica", 11)
        font_btn = ("Helvetica", 11, "bold")
        font_btn_lrg = ("Helvetica", 14, "bold")

        # --- Title Section ---
        tk.Label(self.root, text="SwitchPic", font=font_title, bg="#F3F4F6", fg="#1F2937").pack(pady=(20, 5))
        tk.Label(self.root, text="Seamless Image Format Conversion", font=font_sub, bg="#F3F4F6", fg="#6B7280").pack(pady=(0, 20))

        # --- Card 1: Upload Section ---
        # Using a white frame with a thin border to act as a "Card"
        upload_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid", padx=20, pady=20)
        upload_frame.pack(fill="x", padx=40, pady=(0, 10))

        btn_frame = tk.Frame(upload_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x")

        self.btn_upload = tk.Button(btn_frame, text="Browse Image", font=font_btn, bg="#3B82F6", fg="white", 
                                    activebackground="#2563EB", activeforeground="white", relief="flat", 
                                    cursor="hand2", command=self.upload, height=2)
        self.btn_upload.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.btn_unload = tk.Button(btn_frame, text="Clear", font=font_btn, bg="#EF4444", fg="white", 
                                    activebackground="#DC2626", activeforeground="white", relief="flat", 
                                    cursor="hand2", command=self.unload, height=2, width=10)
        self.btn_unload.pack(side="right")

        self.status_label = tk.Label(upload_frame, text="No file selected", font=font_sub, bg="#FFFFFF", fg="#9CA3AF")
        self.status_label.pack(pady=(15, 0))

        # --- Card 2: Settings Section ---
        settings_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid", padx=20, pady=20)
        settings_frame.pack(fill="x", padx=40, pady=10)

        tk.Label(settings_frame, text="Output Format:", font=("Helvetica", 11, "bold"), bg="#FFFFFF", fg="#374151").pack(side="left")

        self.form_var = tk.StringVar(value="JPEG (.jpg)")
        
        # Using ttk.Combobox for a cleaner dropdown than the standard tk.OptionMenu
        self.picform = ttk.Combobox(settings_frame, textvariable=self.form_var, 
                                    values=list(self.format_mapping.keys()), state="readonly", 
                                    font=("Helvetica", 11), width=18)
        self.picform.pack(side="right")

        # --- Action Section ---
        self.btn_convert = tk.Button(self.root, text="Convert & Save", font=font_btn_lrg, bg="#10B981", fg="white", 
                                     activebackground="#059669", activeforeground="white", relief="flat", 
                                     cursor="hand2", command=self.convert, height=2)
        self.btn_convert.pack(fill="x", padx=40, pady=(20, 0))

    def upload(self):
        file_path = filedialog.askopenfilename(
            title="Select File", 
            filetypes=(("Image files", "*.jpg *.png *.webp *.tiff *.ico *.bmp *.jpeg"), ("All files", "*.*"))
        )
        
        if not file_path:
            return 

        try:
            self.image = Image.open(file_path)
            self.current_filename = Path(file_path).name
            
            # Visual feedback
            self.btn_upload.config(text="Image Uploaded", bg="#1D4ED8") 
            self.status_label.config(text=f"Ready: {self.current_filename}", fg="#10B981")
        except Exception as e:
            messagebox.showerror("Upload Error", f"Failed to open image: {e}")
            self.unload()

    def convert(self):
        if self.image is None:
            messagebox.showwarning("Missing Image", "Please browse and upload an image first.")
            return
            
        selected_format = self.form_var.get()
        out_dir = Path("Results")
        out_dir.mkdir(exist_ok=True)
        
        pil_format, extension = self.format_mapping[selected_format]
        ctime = time.strftime("%d%b%Y_%H%M%S")
        out_path = out_dir / f"{ctime}{extension}"

        try:
            img_to_save = self.image
            
            # Handle alpha channels (transparency) safely
            if pil_format in ["JPEG", "BMP"] and img_to_save.mode in ("RGBA", "P", "LA"):
                # Create a white background to replace transparency
                bg = Image.new("RGB", img_to_save.size, (255, 255, 255))
                if img_to_save.mode == "RGBA":
                    bg.paste(img_to_save, mask=img_to_save.split()[3])
                else:
                    bg.paste(img_to_save)
                img_to_save = bg
                
            img_to_save.save(out_path, format=pil_format)
            messagebox.showinfo("Success!", f"Successfully converted and saved as:\n{out_path.name}")
            
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred:\n{e}")

    def unload(self):
        self.image = None
        self.current_filename = ""
        self.btn_upload.config(text="Browse Image", bg="#3B82F6")
        self.status_label.config(text="No file selected", fg="#9CA3AF")

if __name__ == "__main__":
    root = tk.Tk()
    app = SwitchPicVanilla(root)
    root.mainloop()