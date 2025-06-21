import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from ultralytics import YOLO
import cv2
import numpy as np
import pathlib
import math
import threading
import time
from datetime import datetime


class StarField:
    """Animated starfield background for space theme"""
    def __init__(self, canvas, width, height, num_stars=100):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.stars = []
        self.animation_running = False
        
        # Create stars with random positions and speeds
        for _ in range(num_stars):
            self.stars.append({
                'x': np.random.uniform(0, width),
                'y': np.random.uniform(0, height),
                'speed': np.random.uniform(0.1, 0.5),
                'brightness': np.random.uniform(0.3, 1.0),
                'size': np.random.choice([1, 2])
            })
    
    def update_and_draw(self):
        """Update star positions and redraw"""
        if not self.animation_running:
            return
            
        self.canvas.delete("star")
        
        for star in self.stars:
            # Move star
            star['y'] += star['speed']
            
            # Reset star position if it goes off screen
            if star['y'] > self.height:
                star['y'] = -5
                star['x'] = np.random.uniform(0, self.width)
            
            # Draw star with twinkling effect
            alpha = int(255 * star['brightness'] * (0.7 + 0.3 * math.sin(time.time() * 3 + star['x'])))
            color = f"#{alpha:02x}{alpha:02x}{255:02x}"  # Blue-white stars
            
            self.canvas.create_oval(
                star['x'], star['y'], 
                star['x'] + star['size'], star['y'] + star['size'],
                fill=color, outline=color, tags="star"
            )
        
        # Schedule next update
        self.canvas.after(50, self.update_and_draw)
    
    def start_animation(self):
        """Start the starfield animation"""
        self.animation_running = True
        self.update_and_draw()
    
    def stop_animation(self):
        """Stop the starfield animation"""
        self.animation_running = False


class SpaceProgressBar:
    """Custom space-themed progress bar"""
    def __init__(self, parent, width=400, height=20):
        self.frame = tk.Frame(parent, bg="#0a0a1a")
        self.canvas = tk.Canvas(self.frame, width=width, height=height, 
                               bg="#0a0a1a", highlightthickness=0)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.progress = 0
        
    def set_progress(self, value):
        """Set progress value (0-100)"""
        self.progress = max(0, min(100, value))
        self.draw()
    
    def draw(self):
        """Draw the progress bar"""
        self.canvas.delete("all")
        
        # Background
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                   fill="#1a1a2e", outline="#3a3a5c", width=2)
        
        # Progress fill with gradient effect
        fill_width = (self.width - 4) * (self.progress / 100)
        if fill_width > 0:
            # Create gradient effect
            for i in range(int(fill_width)):
                alpha = 0.6 + 0.4 * (i / fill_width) if fill_width > 0 else 0.6
                color_val = int(255 * alpha)
                color = f"#{color_val:02x}{int(color_val*0.5):02x}{255:02x}"
                self.canvas.create_line(2 + i, 2, 2 + i, self.height - 2, fill=color)
        
        # Progress text
        text = f"{self.progress:.0f}%"
        self.canvas.create_text(self.width // 2, self.height // 2, 
                              text=text, fill="#ffffff", font=("Courier", 8, "bold"))


class AstroGuardApp(tk.Tk):
    """Enhanced space-themed Tkinter desktop front-end for YOLOv8 space-station object detector."""

    CONF_THRES = 0.5
    WINDOW_TITLE = "🛰️ AstroGuard Orbital Defense System"
    
    # Space theme colors
    COLORS = {
        'bg_primary': '#0a0a1a',      # Deep space black
        'bg_secondary': '#1a1a2e',    # Dark blue-black
        'accent': '#3a3a5c',          # Space blue
        'text_primary': '#ffffff',    # Bright white
        'text_secondary': '#b0b0d0',  # Light blue-gray
        'success': '#00ff88',         # Bright green
        'warning': '#ffaa00',         # Orange
        'danger': '#ff4444'           # Red
    }

    def __init__(self, weights_path: str):
        super().__init__()
        self.setup_window()
        
        # Load YOLO model in background
        self.model = None
        self.model_loaded = False
        self.detection_in_progress = False
        
        # GUI state
        self._img_path: pathlib.Path | None = None
        self._tk_img: ImageTk.PhotoImage | None = None
        
        # Create GUI
        self.create_gui()
        
        # Load model in background thread
        self.load_model_async(weights_path)
        
        # Start animations
        self.starfield.start_animation()
        self.update_system_status()

    def setup_window(self):
        """Configure main window with space theme"""
        self.title(self.WINDOW_TITLE)
        self.geometry("1000x800")
        self.resizable(True, True)
        self.configure(bg=self.COLORS['bg_primary'])
        
        # Try to set window icon (space station emoji as fallback)
        try:
            # You can replace this with an actual .ico file
            self.iconbitmap(default="")
        except:
            pass

    def create_gui(self):
        """Create the main GUI with space theme"""
        # Main container with gradient background
        main_frame = tk.Frame(self, bg=self.COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Animated starfield background
        self.bg_canvas = tk.Canvas(main_frame, bg=self.COLORS['bg_primary'], 
                                  highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.starfield = StarField(self.bg_canvas, 980, 780)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg=self.COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Mission title with glow effect
        title_label = tk.Label(header_frame, 
                              text="🛰️ ASTROGUARD ORBITAL DEFENSE SYSTEM",
                              font=("Orbitron", 24, "bold"),
                              fg=self.COLORS['text_primary'],
                              bg=self.COLORS['bg_primary'])
        title_label.pack()
        
        # Mission subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="⚡ Advanced Space Station Object Detection & Classification ⚡",
                                 font=("Courier", 12),
                                 fg=self.COLORS['text_secondary'],
                                 bg=self.COLORS['bg_primary'])
        subtitle_label.pack(pady=5)
        
        # System status frame
        status_frame = tk.Frame(main_frame, bg=self.COLORS['bg_secondary'], 
                               relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=10, padx=20)
        
        status_inner = tk.Frame(status_frame, bg=self.COLORS['bg_secondary'])
        status_inner.pack(fill=tk.X, padx=10, pady=8)
        
        # System status indicators
        self.status_label = tk.Label(status_inner, text="🔄 INITIALIZING DETECTION SYSTEMS...",
                                    font=("Courier", 10, "bold"),
                                    fg=self.COLORS['warning'],
                                    bg=self.COLORS['bg_secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        self.time_label = tk.Label(status_inner, text="",
                                  font=("Courier", 10),
                                  fg=self.COLORS['text_secondary'],
                                  bg=self.COLORS['bg_secondary'])
        self.time_label.pack(side=tk.RIGHT)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.COLORS['bg_secondary'],
                                relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=10, padx=20)
        
        control_inner = tk.Frame(control_frame, bg=self.COLORS['bg_secondary'])
        control_inner.pack(pady=15)
        
        # Upload button with space styling
        self.upload_btn = tk.Button(control_inner, 
                                   text="🚀 INITIATE SCAN",
                                   command=self.browse,
                                   font=("Orbitron", 14, "bold"),
                                   fg=self.COLORS['text_primary'],
                                   bg=self.COLORS['accent'],
                                   activebackground=self.COLORS['success'],
                                   activeforeground=self.COLORS['text_primary'],
                                   relief=tk.RAISED,
                                   bd=3,
                                   padx=30,
                                   pady=10)
        self.upload_btn.pack(pady=5)
        
        # Progress bar
        self.progress_bar = SpaceProgressBar(control_inner)
        self.progress_bar.frame.pack(pady=10)
        self.progress_bar.frame.pack_forget()  # Hide initially
        
        # Detection info
        self.detection_info = tk.Label(control_inner, text="",
                                      font=("Courier", 10),
                                      fg=self.COLORS['text_secondary'],
                                      bg=self.COLORS['bg_secondary'])
        self.detection_info.pack()
        
        # Image display area
        image_frame = tk.Frame(main_frame, bg=self.COLORS['bg_secondary'],
                              relief=tk.SUNKEN, bd=3)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Image panel with space border
        self.image_panel = tk.Label(image_frame, 
                                   text="🌌 AWAITING TARGET IMAGE FOR ANALYSIS 🌌\n\n" +
                                        "📡 Upload an image to detect:\n" +
                                        "🧯 Fire Extinguishers\n" +
                                        "🧰 Tool Boxes\n" +
                                        "🫁 Oxygen Tanks",
                                   font=("Courier", 14),
                                   fg=self.COLORS['text_secondary'],
                                   bg=self.COLORS['bg_primary'],
                                   justify=tk.CENTER)
        self.image_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_model_async(self, weights_path: str):
        """Load YOLO model in background thread"""
        def load_model():
            try:
                self.model = YOLO(weights_path)
                self.model_loaded = True
                self.after(0, self.on_model_loaded)
            except Exception as e:
                self.after(0, lambda: self.on_model_error(str(e)))
        
        thread = threading.Thread(target=load_model, daemon=True)
        thread.start()

    def on_model_loaded(self):
        """Called when model loading is complete"""
        self.status_label.configure(text="✅ DETECTION SYSTEMS ONLINE",
                                   fg=self.COLORS['success'])
        self.upload_btn.configure(state=tk.NORMAL)

    def on_model_error(self, error_msg: str):
        """Called when model loading fails"""
        self.status_label.configure(text=f"❌ SYSTEM ERROR: {error_msg}",
                                   fg=self.COLORS['danger'])
        messagebox.showerror("Model Loading Error", 
                           f"Failed to load detection model:\n{error_msg}")

    def update_system_status(self):
        """Update system time and status"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.time_label.configure(text=f"🕐 {current_time}")
        
        # Schedule next update
        self.after(1000, self.update_system_status)

    def browse(self):
        """Open file dialog and load image"""
        if not self.model_loaded:
            messagebox.showwarning("System Not Ready", 
                                 "Detection systems are still initializing. Please wait...")
            return
        
        if self.detection_in_progress:
            messagebox.showinfo("Detection In Progress", 
                              "Please wait for current detection to complete.")
            return
        
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
            ("All files", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            title="Select Target Image for Analysis",
            filetypes=filetypes
        )
        
        if not path:
            return

        self._img_path = pathlib.Path(path)
        self.show_image(self._img_path)
        self.detect_objects_async()

    def show_image(self, img_path: pathlib.Path):
        """Display original image"""
        try:
            pil_img = Image.open(img_path).convert("RGB")
            self.display_pil_image(pil_img)
            self.detection_info.configure(
                text=f"📁 Loaded: {img_path.name} | 📐 Size: {pil_img.size[0]}x{pil_img.size[1]}"
            )
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image:\n{str(e)}")

    def detect_objects_async(self):
        """Run detection in background thread"""
        if not self.model_loaded or self.detection_in_progress:
            return
        
        self.detection_in_progress = True
        self.upload_btn.configure(state=tk.DISABLED)
        self.progress_bar.frame.pack(pady=10)
        
        def detect():
            try:
                self.after(0, lambda: self.progress_bar.set_progress(20))
                
                # Run inference
                results = self.model(str(self._img_path), conf=self.CONF_THRES)[0]
                self.after(0, lambda: self.progress_bar.set_progress(60))
                
                # Process results
                detection_result = self.process_detection_results(results)
                self.after(0, lambda: self.progress_bar.set_progress(100))
                
                # Update UI
                self.after(0, lambda: self.on_detection_complete(detection_result))
                
            except Exception as e:
                self.after(0, lambda: self.on_detection_error(str(e)))
        
        thread = threading.Thread(target=detect, daemon=True)
        thread.start()

    def process_detection_results(self, results):
        """Process YOLO detection results and create annotated image"""
        pil_img = Image.open(self._img_path).convert("RGB")
        img_np = np.array(pil_img)
        
        detections = []
        colors = {
            'fire_extinguisher': (0, 255, 100),    # Bright green
            'toolbox': (255, 165, 0),              # Orange
            'oxygen_tank': (0, 150, 255),          # Blue
            'default': (255, 255, 0)               # Yellow
        }
        
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            class_name = self.model.names[cls_id]
            
            detections.append({
                'class': class_name,
                'confidence': conf,
                'bbox': (x1, y1, x2, y2)
            })
            
            # Get color for this class
            color = colors.get(class_name.lower().replace(' ', '_'), colors['default'])
            
            # Draw enhanced bounding box
            thickness = 3
            cv2.rectangle(img_np, (x1, y1), (x2, y2), color, thickness)
            
            # Create label with background
            label = f"{class_name} {conf:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            
            # Label background
            cv2.rectangle(img_np, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            
            # Label text
            cv2.putText(img_np, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        return {
            'image': img_np,
            'detections': detections
        }

    def on_detection_complete(self, result):
        """Called when detection is complete"""
        # Display annotated image
        pil_img = Image.fromarray(result['image'])
        self.display_pil_image(pil_img)
        
        # Update info
        detections = result['detections']
        if detections:
            detection_summary = {}
            for det in detections:
                cls = det['class']
                detection_summary[cls] = detection_summary.get(cls, 0) + 1
            
            summary_text = "🎯 DETECTION COMPLETE | "
            summary_parts = [f"{cls}: {count}" for cls, count in detection_summary.items()]
            summary_text += " | ".join(summary_parts)
            
            self.detection_info.configure(text=summary_text, fg=self.COLORS['success'])
        else:
            self.detection_info.configure(text="🔍 SCAN COMPLETE - NO OBJECTS DETECTED", 
                                        fg=self.COLORS['warning'])
        
        # Reset UI
        self.detection_in_progress = False
        self.upload_btn.configure(state=tk.NORMAL)
        self.progress_bar.frame.pack_forget()

    def on_detection_error(self, error_msg: str):
        """Called when detection fails"""
        self.detection_info.configure(text=f"❌ DETECTION FAILED: {error_msg}", 
                                    fg=self.COLORS['danger'])
        self.detection_in_progress = False
        self.upload_btn.configure(state=tk.NORMAL)
        self.progress_bar.frame.pack_forget()
        messagebox.showerror("Detection Error", f"Detection failed:\n{error_msg}")

    def display_pil_image(self, pil_img: Image.Image):
        """Display PIL image in the GUI with proper scaling"""
        # Calculate display size while maintaining aspect ratio
        display_width, display_height = 700, 400
        img_width, img_height = pil_img.size
        
        scale = min(display_width / img_width, display_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image
        pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self._tk_img = ImageTk.PhotoImage(pil_img)
        self.image_panel.configure(image=self._tk_img, text="")


# Entry point
if __name__ == "__main__":
    # Replace with your actual model path
    WEIGHTS = r"C:\Users\ritig\OneDrive\Desktop\CodeClash\AstroGuard\best.pt"
    
    try:
        app = AstroGuardApp(WEIGHTS)
        app.mainloop()
    except Exception as e:
        print(f"Failed to start AstroGuard: {e}")
        messagebox.showerror("Startup Error", f"Failed to initialize AstroGuard:\n{e}")