# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext
# from ultralytics import YOLO
# import threading
# import sys
# import psutil
# import time
# from contextlib import redirect_stdout
# from io import StringIO
# import logging
# import torch   # <-- for auto-detect

# # Auto-detect device
# AUTO_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# # Global flag
# stop_training_flag = False

# class RedirectOutput:
#     def __init__(self, text_widget):
#         self.text_widget = text_widget

#     def write(self, msg):
#         self.text_widget.insert(tk.END, msg)
#         self.text_widget.see(tk.END)
#         self.text_widget.update_idletasks()

#     def flush(self):
#         pass

#     def emit(self, record):
#         msg = self.format(record)
#         self.write(msg + "\n")

# def setup_logger(output_widget):
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     for h in logger.handlers[:]:
#         logger.removeHandler(h)
#     handler = logging.StreamHandler(RedirectOutput(output_widget))
#     handler.setFormatter(logging.Formatter("%(message)s"))
#     logger.addHandler(handler)

# def start_training():
#     global stop_training_flag
#     stop_training_flag = False

#     def run_training():
#         try:
#             # Gather inputs
#             model_path       = model_path_entry.get().strip()
#             data_yaml        = data_yaml_entry.get().strip()
#             epochs_str       = epochs_entry.get().strip()
#             imgsz_str        = imgsz_entry.get().strip()
#             batch_str        = batch_entry.get().strip()
#             workers_str      = workers_entry.get().strip()
#             project_name     = project_entry.get().strip()
#             experiment_name  = experiment_name_entry.get().strip()
#             device_str       = AUTO_DEVICE  # <- override manual entry

#             # Log config
#             print("Training config:")
#             print(f" • Model:    {model_path}")
#             print(f" • Data YAML:{data_yaml}")
#             print(f" • Epochs:   {epochs_str}")
#             print(f" • ImgSize:  {imgsz_str}")
#             print(f" • Batch:    {batch_str}")
#             print(f" • Workers:  {workers_str}")
#             print(f" • Project:  {project_name}")
#             print(f" • Experiment:{experiment_name}")
#             print(f" • Device:   {device_str}")

#             # Validate
#             if not all([model_path, data_yaml, epochs_str, imgsz_str,
#                         batch_str, workers_str, project_name, experiment_name]):
#                 messagebox.showerror("Error", "Please fill in all fields!")
#                 return

#             try:
#                 epochs  = int(epochs_str)
#                 imgsz   = int(imgsz_str)
#                 batch   = int(batch_str)
#                 workers = int(workers_str)
#             except ValueError:
#                 messagebox.showerror("Error",
#                                      "Epochs, Image Size, Batch Size and Workers must be integers.")
#                 return

#             # Redirect stdout
#             buffer = StringIO()
#             with redirect_stdout(buffer):
#                 model = YOLO(model_path)
#                 print("✅ Model loaded")
#                 model.train(
#                     data=data_yaml,
#                     epochs=epochs,
#                     imgsz=imgsz,
#                     batch=batch,
#                     workers=workers,
#                     amp=False,
#                     cache=True,
#                     project=project_name,
#                     name=experiment_name,
#                     device=device_str,
#                     resume=resume_var.get()
#                 )
#             output_text.insert(tk.END, buffer.getvalue())
#             output_text.see(tk.END)

#         except Exception as e:
#             print("Error:", e)
#             messagebox.showerror("Training Error", str(e))

#     threading.Thread(target=run_training, daemon=True).start()


# def update_resource_usage():
#     while True:
#         cpu_usage.set(f"CPU Usage: {psutil.cpu_percent()}%")
#         ram_usage.set(f"RAM Usage: {psutil.virtual_memory().percent}%")
#         time.sleep(1)


# # ─── GUI SETUP ─────────────────────────────────────────────────────────
# root = tk.Tk()
# root.title("YOLOv8 Training Configuration")
# root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# # Resource labels
# cpu_usage = tk.StringVar(value="CPU Usage: 0%")
# ram_usage = tk.StringVar(value="RAM Usage: 0%")
# tk.Label(root, textvariable=cpu_usage, fg="blue").grid(row=0, column=0, sticky="w", padx=10)
# tk.Label(root, textvariable=ram_usage, fg="blue").grid(row=0, column=1, sticky="w", padx=10)

# # Model Path
# tk.Label(root, text="Model Path:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
# model_path_entry = tk.Entry(root, width=70); model_path_entry.grid(row=1, column=1, pady=5)
# tk.Button(root, text="Browse", command=lambda:
#           model_path_entry.insert(0, filedialog.askopenfilename())).grid(row=1, column=2)

# # Data YAML
# tk.Label(root, text="Data YAML Path:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
# data_yaml_entry = tk.Entry(root, width=70); data_yaml_entry.grid(row=2, column=1, pady=5)
# tk.Button(root, text="Browse", command=lambda:
#           data_yaml_entry.insert(0, filedialog.askopenfilename())).grid(row=2, column=2)

# # Epochs / Image Size / Batch / Workers
# tk.Label(root, text="Epochs:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
# epochs_entry = tk.Entry(root, width=20); epochs_entry.grid(row=3, column=1, pady=5)
# epochs_entry.insert(0, "120")

# tk.Label(root, text="Image Size:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
# imgsz_entry = tk.Entry(root, width=20); imgsz_entry.grid(row=4, column=1, pady=5)
# imgsz_entry.insert(0, "512")

# tk.Label(root, text="Batch Size:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
# batch_entry = tk.Entry(root, width=20); batch_entry.grid(row=5, column=1, pady=5)
# batch_entry.insert(0, "1")

# tk.Label(root, text="Workers:").grid(row=6, column=0, sticky="e", padx=10, pady=5)
# workers_entry = tk.Entry(root, width=20); workers_entry.grid(row=6, column=1, pady=5)
# workers_entry.insert(0, "2")

# # Project & Experiment
# tk.Label(root, text="Project Directory:").grid(row=7, column=0, sticky="e", padx=10, pady=5)
# project_entry = tk.Entry(root, width=70); project_entry.grid(row=7, column=1, pady=5)
# tk.Button(root, text="Browse", command=lambda:
#           project_entry.delete(0, tk.END) or project_entry.insert(0, filedialog.askdirectory())
#           ).grid(row=7, column=2)

# tk.Label(root, text="Experiment Name:").grid(row=8, column=0, sticky="e", padx=10, pady=5)
# experiment_name_entry = tk.Entry(root, width=70); experiment_name_entry.grid(row=8, column=1, pady=5)
# experiment_name_entry.insert(0, "yolov8_experiment")

# # Device (auto-detected)
# tk.Label(root, text="Device:").grid(row=9, column=0, sticky="e", padx=10, pady=5)
# device_entry = tk.Entry(root, width=20, state="readonly")
# device_entry.grid(row=9, column=1, pady=5)
# device_entry.configure(state="normal")
# device_entry.insert(0, AUTO_DEVICE)
# device_entry.configure(state="readonly")

# # Resume checkbox
# tk.Label(root, text="Resume Training:").grid(row=10, column=0, sticky="e", padx=10, pady=5)
# resume_var = tk.BooleanVar(value=False)
# tk.Checkbutton(root, text="Resume", variable=resume_var).grid(row=10, column=1, sticky="w")

# # Start button
# tk.Button(root, text="Start Training", command=start_training,
#           bg="green", fg="white").grid(row=11, column=0, pady=10, padx=10)

# # Output log
# tk.Label(root, text="Training Progress:").grid(row=12, column=0, sticky="nw", padx=10)
# output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=120, height=12)
# output_text.grid(row=13, column=1, columnspan=2, pady=5, padx=10)

# # Redirect prints to widget
# sys.stdout = RedirectOutput(output_text)

# # Footer
# tk.Label(root, text="Powered by V V Technologies, Bangalore",
#          fg="gray", font=("Arial", 10, "italic"))\
#     .grid(row=14, column=0, columnspan=3, pady=5)

# # Start resource monitor
# threading.Thread(target=update_resource_usage, daemon=True).start()

# root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from ultralytics import YOLO
import threading
import sys
import psutil
import time
from contextlib import redirect_stdout
from io import StringIO
import logging
import queue

# Global flag to stop training
stop_training = False

class RedirectOutput:
    """Redirect stdout to a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()
        
    def write(self, message):
        # Put message in queue for thread-safe GUI updates
        self.queue.put(message)
        
    def flush(self):
        pass

def update_output_display():
    """Update the output display from the queue (thread-safe)."""
    try:
        while True:
            message = redirect_output.queue.get_nowait()
            output_text.insert(tk.END, message)
            output_text.see(tk.END)
            output_text.update_idletasks()
    except queue.Empty:
        pass
    # Schedule next update
    root.after(100, update_output_display)

def start_training():
    """Invoke YOLO training in a background thread."""
    def run_training():
        global stop_training
        stop_training = False
        
        try:
            # Collect inputs
            model_path = model_path_entry.get().strip()
            data_yaml = data_yaml_entry.get().strip()
            epochs_str = epochs_entry.get().strip()
            imgsz_str = imgsz_entry.get().strip()
            batch_str = batch_entry.get().strip()
            workers_str = workers_entry.get().strip()
            project_name = project_entry.get().strip()
            experiment_name = experiment_name_entry.get().strip()
            device_str = device_entry.get().strip()
            resume_flag = resume_var.get()
            amp_flag = amp_var.get()

            # Log config
            print("Training configuration:")
            print(f" Model Path:     {model_path}")
            print(f" Data YAML:      {data_yaml}")
            print(f" Epochs:         {epochs_str}")
            print(f" Image Size:     {imgsz_str}")
            print(f" Batch Size:     {batch_str}")
            print(f" Workers:        {workers_str}")
            print(f" Project:        {project_name}")
            print(f" Experiment:     {experiment_name}")
            print(f" Device:         {device_str}")
            print(f" Resume:         {resume_flag}")
            print(f" Mixed Precision: {amp_flag}")

            # Validate inputs
            if not all([model_path, data_yaml, epochs_str, imgsz_str,
                       batch_str, workers_str, project_name, experiment_name, device_str]):
                root.after(0, lambda: messagebox.showerror("Error", "Please fill in all fields."))
                return

            # Convert to integers
            try:
                epochs = int(epochs_str)
                imgsz = int(imgsz_str)
                batch = int(batch_str)
                workers = int(workers_str)
            except ValueError:
                root.after(0, lambda: messagebox.showerror("Error", "Epochs, Image Size, Batch Size, and Workers must be integers."))
                return

            # Load model and start training
            print("Loading YOLO model...")
            model = YOLO(model_path)
            print("✅ Model loaded successfully.")
            
            print("Starting training...")
            model.train(
                data=data_yaml,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                workers=workers,
                amp=amp_flag,
                cache=True,
                project=project_name,
                name=experiment_name,
                device=device_str,
                resume=resume_flag,
                optimizer='AdamW',
                lr0=0.01,
                lrf=0.1,
                momentum=0.937,
                weight_decay=0.0005,
                warmup_epochs=3,
                warmup_momentum=0.8,
                warmup_bias_lr=0.1,
                mosaic=1.0,
                mixup=0.1,
                copy_paste=0.1
            )
            
            print("✅ Training completed successfully!")

        except Exception as e:
            error_msg = f"Training error: {e}"
            print(error_msg)
            root.after(0, lambda: messagebox.showerror("Training Error", str(e)))

    # Start training in a separate thread
    threading.Thread(target=run_training, daemon=True).start()

def stop_training_func():
    """Stop the training process."""
    global stop_training
    stop_training = True
    print("Stopping training...")

def update_resource_usage():
    """Periodically update CPU/RAM usage labels."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent
        cpu_usage.set(f"CPU Usage: {cpu_percent:.1f}%")
        ram_usage.set(f"RAM Usage: {ram_percent:.1f}%")
        
        # Add GPU temperature monitoring if available
        try:
            import torch
            if torch.cuda.is_available():
                gpu_temp = torch.cuda.temperature()
                if gpu_temp > 0:
                    print(f"⚠️ GPU Temperature: {gpu_temp}°C")
                    if gpu_temp > 90:
                        print("⚠️ WARNING: High GPU temperature detected!")
        except Exception:
            pass
            
    except Exception:
        cpu_usage.set("CPU Usage: N/A")
        ram_usage.set("RAM Usage: N/A")
    
    # Schedule next update
    root.after(2000, update_resource_usage)

def browse_model_file():
    """Browse for model file."""
    filename = filedialog.askopenfilename(
        title="Select Model File",
        filetypes=[("Model files", "*.pt *.yaml"), ("All files", "*.*")]
    )
    if filename:
        model_path_entry.delete(0, tk.END)
        model_path_entry.insert(0, filename)

def browse_data_yaml():
    """Browse for data YAML file."""
    filename = filedialog.askopenfilename(
        title="Select Data YAML File",
        filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
    )
    if filename:
        data_yaml_entry.delete(0, tk.END)
        data_yaml_entry.insert(0, filename)

def browse_project_dir():
    """Browse for project directory."""
    dirname = filedialog.askdirectory(title="Select Project Directory")
    if dirname:
        project_entry.delete(0, tk.END)
        project_entry.insert(0, dirname)

# Build GUI
root = tk.Tk()
root.title("YOLOv8 Training Configuration")
root.geometry("1200x800")

# Configure grid weights for responsive design
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(14, weight=1)

# Bind Enter key to start training
root.bind("<Return>", lambda e: start_training())

# Resource usage labels
cpu_usage = tk.StringVar(value="CPU Usage: 0%")
ram_usage = tk.StringVar(value="RAM Usage: 0%")
tk.Label(root, textvariable=cpu_usage, fg="blue", font=("Arial", 12)).grid(
    row=0, column=0, padx=10, pady=5, sticky="w"
)
tk.Label(root, textvariable=ram_usage, fg="blue", font=("Arial", 12)).grid(
    row=0, column=1, padx=10, pady=5, sticky="w"
)

# Model Path
tk.Label(root, text="Model Path:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
model_path_entry = tk.Entry(root, width=70)
model_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Browse", command=browse_model_file).grid(
    row=1, column=2, padx=10, pady=5
)

# Data YAML Path
tk.Label(root, text="Data YAML Path:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
data_yaml_entry = tk.Entry(root, width=70)
data_yaml_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Browse", command=browse_data_yaml).grid(
    row=2, column=2, padx=10, pady=5
)

# Epochs
tk.Label(root, text="Number of Epochs:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
epochs_entry = tk.Entry(root, width=20)
epochs_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
epochs_entry.insert(0, "120")

# Image Size
tk.Label(root, text="Image Size:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
imgsz_entry = tk.Entry(root, width=20)
imgsz_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
imgsz_entry.insert(0, "512")

# Batch Size
tk.Label(root, text="Batch Size:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
batch_entry = tk.Entry(root, width=20)
batch_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
batch_entry.insert(0, "16")

# Workers
tk.Label(root, text="Number of Workers:").grid(row=6, column=0, sticky="e", padx=10, pady=5)
workers_entry = tk.Entry(root, width=20)
workers_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
workers_entry.insert(0, "8")

# Project Directory
tk.Label(root, text="Project Directory:").grid(row=7, column=0, sticky="e", padx=10, pady=5)
project_entry = tk.Entry(root, width=70)
project_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Browse", command=browse_project_dir).grid(
    row=7, column=2, padx=10, pady=5
)

# Experiment Name
tk.Label(root, text="Experiment Name:").grid(row=8, column=0, sticky="e", padx=10, pady=5)
experiment_name_entry = tk.Entry(root, width=70)
experiment_name_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
experiment_name_entry.insert(0, "yolov8_experiment")

# Device
tk.Label(root, text="Device (e.g., 'cpu' or '0'):").grid(row=9, column=0, sticky="e", padx=10, pady=5)
device_entry = tk.Entry(root, width=20)
device_entry.grid(row=9, column=1, padx=10, pady=5, sticky="w")
device_entry.insert(0, "cuda")

# Resume Training
resume_var = tk.BooleanVar(value=False)
tk.Label(root, text="Resume Training:").grid(row=10, column=0, sticky="e", padx=10, pady=5)
tk.Checkbutton(root, text="Resume", variable=resume_var).grid(
    row=10, column=1, sticky="w", padx=10, pady=5
)

# Mixed Precision Training
amp_var = tk.BooleanVar(value=True)
tk.Label(root, text="Mixed Precision (AMP):").grid(row=11, column=0, sticky="e", padx=10, pady=5)
tk.Checkbutton(root, text="Enable AMP (Faster)", variable=amp_var).grid(
    row=11, column=1, sticky="w", padx=10, pady=5
)

# Control buttons frame
button_frame = tk.Frame(root)
button_frame.grid(row=12, column=0, columnspan=3, pady=10)

# Start Training Button
tk.Button(button_frame, text="Start Training", command=start_training, 
          bg="green", fg="white", font=("Arial", 12), padx=20).pack(side=tk.LEFT, padx=10)

# Stop Training Button
tk.Button(button_frame, text="Stop Training", command=stop_training_func, 
          bg="red", fg="white", font=("Arial", 12), padx=20).pack(side=tk.LEFT, padx=10)

# Training Progress Log
tk.Label(root, text="Training Progress:").grid(row=13, column=0, sticky="nw", padx=10, pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=120, height=15)
output_text.grid(row=14, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Create redirect output object
redirect_output = RedirectOutput(output_text)

# Redirect stdout to our custom output handler
sys.stdout = redirect_output

# Footer
tk.Label(root, text="Powered by V V Technologies, Bangalore", 
         fg="gray", font=("Arial", 10, "italic")).grid(
    row=15, column=0, columnspan=3, pady=5
)

# Start the output update loop
update_output_display()

# Start resource monitoring
update_resource_usage()

# Launch GUI
if __name__ == "__main__":
    root.mainloop()