"""
PassFoto GUI Application
A user-friendly interface for passport photo enhancement.
Compatible with Windows 8+ and systems with 6GB RAM.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

try:
    from ttkthemes import ThemedTk
    HAS_THEMES = True
except ImportError:
    HAS_THEMES = False

from .image_processor import ImageProcessor


class PassFotoApp:
    """Main application class for PassFoto GUI."""
    
    def __init__(self):
        """Initialize the application."""
        # Create main window
        if HAS_THEMES:
            self.root = ThemedTk(theme="arc")
        else:
            self.root = tk.Tk()
        
        self.root.title("PassFoto - Passport Photo Enhancement")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Initialize variables
        self.processor = ImageProcessor()
        self.original_image = None
        self.processed_image = None
        self.current_file_path = None
        self.preview_size = (400, 500)
        
        # Enhancement options
        self.options = {
            'auto_straighten': tk.BooleanVar(value=True),
            'auto_enhance': tk.BooleanVar(value=True),
            'white_balance': tk.BooleanVar(value=True),
            'denoise': tk.BooleanVar(value=True),
            'smooth_skin': tk.BooleanVar(value=False),
            'sharpen': tk.BooleanVar(value=True),
            'remove_red_eyes': tk.BooleanVar(value=True),
        }
        
        self.brightness_var = tk.IntVar(value=0)
        self.contrast_var = tk.IntVar(value=0)
        self.selected_size = tk.StringVar(value="35x45 mm (EU)")
        
        # Setup UI
        self._setup_ui()
        self._setup_menu()
        self._bind_events()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # File operations
        file_frame = ttk.LabelFrame(left_panel, text="File Operations", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="📂 Open Image", command=self.open_image).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="💾 Save Image", command=self.save_image).pack(fill=tk.X, pady=2)
        
        # Photo size selection
        size_frame = ttk.LabelFrame(left_panel, text="Photo Size", padding="10")
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        sizes = list(ImageProcessor.PHOTO_SIZES.keys())
        size_combo = ttk.Combobox(size_frame, textvariable=self.selected_size, values=sizes, state="readonly")
        size_combo.pack(fill=tk.X)
        
        # Enhancement options
        enhance_frame = ttk.LabelFrame(left_panel, text="Auto Enhancements", padding="10")
        enhance_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(enhance_frame, text="Auto Straighten", variable=self.options['auto_straighten']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="Auto Enhance", variable=self.options['auto_enhance']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="White Balance", variable=self.options['white_balance']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="Denoise", variable=self.options['denoise']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="Smooth Skin", variable=self.options['smooth_skin']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="Sharpen", variable=self.options['sharpen']).pack(anchor=tk.W)
        ttk.Checkbutton(enhance_frame, text="Remove Red Eyes", variable=self.options['remove_red_eyes']).pack(anchor=tk.W)
        
        # Manual adjustments
        adjust_frame = ttk.LabelFrame(left_panel, text="Manual Adjustments", padding="10")
        adjust_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(adjust_frame, text="Brightness:").pack(anchor=tk.W)
        brightness_scale = ttk.Scale(adjust_frame, from_=-100, to=100, variable=self.brightness_var, orient=tk.HORIZONTAL)
        brightness_scale.pack(fill=tk.X)
        
        ttk.Label(adjust_frame, text="Contrast:").pack(anchor=tk.W)
        contrast_scale = ttk.Scale(adjust_frame, from_=-100, to=100, variable=self.contrast_var, orient=tk.HORIZONTAL)
        contrast_scale.pack(fill=tk.X)
        
        # Action buttons
        action_frame = ttk.LabelFrame(left_panel, text="Actions", padding="10")
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="🔄 Apply Enhancements", command=self.apply_enhancements).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="✂️ Crop to Face", command=self.crop_to_face).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="🎨 Change Background", command=self.change_background_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="↩️ Reset to Original", command=self.reset_image).pack(fill=tk.X, pady=2)
        
        # Center panel - Original image
        center_panel = ttk.LabelFrame(main_frame, text="Original Image", padding="10")
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.original_canvas = tk.Canvas(center_panel, bg="#f0f0f0")
        self.original_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Processed image
        right_panel = ttk.LabelFrame(main_frame, text="Enhanced Image", padding="10")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.processed_canvas = tk.Canvas(right_panel, bg="#f0f0f0")
        self.processed_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready. Open an image to get started.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_menu(self):
        """Set up the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Image", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_image_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Apply All Enhancements", command=self.apply_enhancements)
        edit_menu.add_command(label="Crop to Face", command=self.crop_to_face)
        edit_menu.add_command(label="Change Background", command=self.change_background_dialog)
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset to Original", command=self.reset_image)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Usage Guide", command=self.show_guide)
    
    def _bind_events(self):
        """Bind keyboard events."""
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_image_as())
    
    def open_image(self):
        """Open an image file."""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.status_var.set("Loading image...")
                self.current_file_path = file_path
                self.original_image = self.processor.load_image(file_path)
                self.processed_image = self.original_image.copy()
                self._update_previews()
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")
                self.status_var.set("Error loading image.")
    
    def save_image(self):
        """Save the processed image."""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save. Please open an image first.")
            return
        
        if self.current_file_path:
            # Generate default output path
            base, ext = os.path.splitext(self.current_file_path)
            output_path = f"{base}_enhanced{ext}"
            self._save_to_path(output_path)
        else:
            self.save_image_as()
    
    def save_image_as(self):
        """Save the processed image with a new name."""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save. Please open an image first.")
            return
        
        file_types = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image As",
            filetypes=file_types,
            defaultextension=".jpg"
        )
        
        if file_path:
            self._save_to_path(file_path)
    
    def _save_to_path(self, file_path):
        """Save the image to the specified path."""
        try:
            self.processor.save_image(self.processed_image, file_path)
            self.status_var.set(f"Saved: {os.path.basename(file_path)}")
            messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {str(e)}")
    
    def apply_enhancements(self):
        """Apply all selected enhancements."""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please open an image first.")
            return
        
        self.status_var.set("Applying enhancements...")
        self.root.update()
        
        try:
            # Get options
            options = {key: var.get() for key, var in self.options.items()}
            
            # Apply enhancements
            self.processed_image = self.processor.apply_all_enhancements(
                self.original_image.copy(), 
                options
            )
            
            # Apply brightness and contrast if not default
            brightness = self.brightness_var.get()
            contrast = self.contrast_var.get()
            if brightness != 0 or contrast != 0:
                self.processed_image = self.processor.adjust_brightness_contrast(
                    self.processed_image, 
                    brightness, 
                    contrast
                )
            
            self._update_previews()
            self.status_var.set("Enhancements applied successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Enhancement failed: {str(e)}")
            self.status_var.set("Enhancement failed.")
    
    def crop_to_face(self):
        """Crop the image to center on the face."""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "Please open an image first.")
            return
        
        self.status_var.set("Cropping to face...")
        self.root.update()
        
        try:
            size_name = self.selected_size.get()
            self.processed_image = self.processor.crop_to_face(
                self.processed_image, 
                size_name
            )
            self._update_previews()
            self.status_var.set("Image cropped to face.")
        except Exception as e:
            messagebox.showerror("Error", f"Cropping failed: {str(e)}")
            self.status_var.set("Cropping failed.")
    
    def change_background_dialog(self):
        """Show dialog to change background color."""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "Please open an image first.")
            return
        
        # Create color picker dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Background Color")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select background color:").pack(pady=10)
        
        # Color buttons
        colors_frame = ttk.Frame(dialog)
        colors_frame.pack(pady=10)
        
        colors = {
            "White": (255, 255, 255),
            "Light Blue": (255, 200, 200),
            "Light Gray": (220, 220, 220),
            "Red": (0, 0, 255),
            "Blue": (255, 0, 0),
        }
        
        selected_color = tk.StringVar(value="White")
        
        for color_name in colors:
            ttk.Radiobutton(colors_frame, text=color_name, variable=selected_color, value=color_name).pack(anchor=tk.W)
        
        def apply_color():
            color = colors[selected_color.get()]
            self.status_var.set("Changing background...")
            self.root.update()
            try:
                self.processed_image = self.processor.change_background(self.processed_image, color)
                self._update_previews()
                self.status_var.set("Background changed.")
            except Exception as e:
                messagebox.showerror("Error", f"Background change failed: {str(e)}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Apply", command=apply_color).pack(pady=10)
    
    def reset_image(self):
        """Reset to the original image."""
        if self.original_image is None:
            return
        
        self.processed_image = self.original_image.copy()
        self.brightness_var.set(0)
        self.contrast_var.set(0)
        self._update_previews()
        self.status_var.set("Image reset to original.")
    
    def _update_previews(self):
        """Update the preview canvases."""
        self._display_image(self.original_canvas, self.original_image)
        self._display_image(self.processed_canvas, self.processed_image)
    
    def _display_image(self, canvas, image):
        """Display an image on a canvas."""
        if image is None:
            return
        
        # Get canvas size
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 400, 500
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculate resize ratio to fit canvas
        img_height, img_width = image.shape[:2]
        ratio = min(canvas_width / img_width, canvas_height / img_height) * 0.95
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Resize image
        resized = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert to PhotoImage
        pil_image = Image.fromarray(resized)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo, anchor=tk.CENTER)
        canvas.image = photo  # Keep reference
    
    def show_about(self):
        """Show about dialog."""
        about_text = """PassFoto - Passport Photo Enhancement

Version: 1.0.0

A Windows-compatible application for enhancing 
formal/passport photos.

Features:
• Auto face detection and alignment
• Automatic rotation correction
• Color enhancement and white balance
• Red eye removal
• Skin smoothing
• Background replacement
• Standard photo size cropping

Compatible with Windows 8+ and 
systems with 6GB RAM.

© 2024 PassFoto Team"""
        
        messagebox.showinfo("About PassFoto", about_text)
    
    def show_guide(self):
        """Show usage guide."""
        guide_text = """PassFoto Usage Guide

1. OPENING AN IMAGE
   - Click "Open Image" or press Ctrl+O
   - Select a photo file (JPG, PNG, etc.)

2. ENHANCING YOUR PHOTO
   - Select enhancement options in the left panel
   - Click "Apply Enhancements" to process

3. AVAILABLE ENHANCEMENTS
   • Auto Straighten: Corrects tilted photos
   • Auto Enhance: Improves overall quality
   • White Balance: Fixes color cast
   • Denoise: Removes image noise
   • Smooth Skin: Softens skin texture
   • Sharpen: Increases image sharpness
   • Remove Red Eyes: Fixes red eye effect

4. CROPPING
   - Select target photo size
   - Click "Crop to Face" to auto-crop

5. BACKGROUND CHANGE
   - Click "Change Background"
   - Select desired color
   - Click "Apply"

6. SAVING
   - Click "Save Image" or press Ctrl+S
   - Enhanced image is saved with "_enhanced" suffix

Tips:
- Use "Reset to Original" to start over
- Adjust brightness/contrast manually if needed
- Preview changes before saving"""
        
        # Create guide window
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Usage Guide")
        guide_window.geometry("500x600")
        
        text_widget = tk.Text(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, guide_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(text_widget, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = PassFotoApp()
    app.run()


if __name__ == "__main__":
    main()
