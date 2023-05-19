import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from tqdm import tqdm


def select_video_file():
    video_file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
    if video_file_path:
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(tk.END, video_file_path)


def convert_video_to_images():
    video_file_path = video_path_entry.get()
    if not video_file_path:
        messagebox.showerror("Error", "Please select a video file.")
        return

    output_directory = filedialog.askdirectory()
    if not output_directory:
        return

    try:
        video = cv2.VideoCapture(video_file_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = int(frame_rate_entry.get()) or 2  # Get frame rate from entry field, default to 2 if empty
        frame_interval = int(round(video.get(cv2.CAP_PROP_FPS) / frame_rate))
        current_frame = 0
        output_frame = 0

        progress_bar["maximum"] = total_frames // frame_interval

        def extract_frames_recursive():
            nonlocal current_frame, output_frame
            ret, frame = video.read()

            if current_frame % frame_interval == 0:
                output_path = os.path.join(output_directory, f"frame_{output_frame}.jpg")
                cv2.imwrite(output_path, frame)
                output_frame += 1

            current_frame += 1
            progress_bar["value"] = current_frame // frame_interval

            if current_frame < total_frames:
                window.after(1, extract_frames_recursive)
            else:
                video.release()
                messagebox.showinfo("Conversion Complete", "Video to images conversion completed successfully!")

        extract_frames_recursive()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
window = tk.Tk()
window.title("Video to Image Converter")
window.geometry("600x350")
window.configure(bg="#2b2b2b")  # Set background color

# Set a custom style for the window
style = ttk.Style(window)
style.theme_use('clam')  # Use the 'clam' theme
style.configure("TFrame", background="#2b2b2b")  # Set frame background color
style.configure("TButton", background="#51a1cc", foreground="#ffffff", font=("Arial", 12, "bold"))
style.map("TButton",
          background=[("active", "#51a1cc"), ("pressed", "#3986a3")],  # Set button colors for different states
          foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])
style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Arial", 12))
style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

# Create a frame to hold the content
content_frame = ttk.Frame(window)
content_frame.pack(pady=20)

# Create and pack the title label
title_label = ttk.Label(content_frame, text="Video to Image Converter", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the video path selection button
video_path_button = ttk.Button(content_frame, text="Select Video File", command=select_video_file)
video_path_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the video path entry field
video_path_entry = ttk.Entry(content_frame)
video_path_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Create and pack the frame rate label and entry
frame_rate_label = ttk.Label(content_frame, text="Frame Rate (frames per second):")
frame_rate_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
frame_rate_entry = ttk.Entry(content_frame)
frame_rate_entry.grid(row=3, column=1, padx=10, pady=5)
frame_rate_entry.insert(tk.END, "2")  # Set the default frame rate to 2

# Create and pack the convert button
convert_button = ttk.Button(content_frame, text="Convert", command=convert_video_to_images)
convert_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", style="green.Horizontal.TProgressbar")
progress_bar.pack(pady=20)

# Center the window on the screen
window.eval('tk::PlaceWindow . center')

# Set the style for the progress bar when it is increasing
style.configure("green.Horizontal.TProgressbar",
                troughcolor="#2b2b2b",  # Set the color of the progress bar trough
                background="#4caf50",  # Set the color of the progress bar
                bordercolor="#4caf50"  # Set the color of the progress bar border
                )

# Run the main window event loop
window.mainloop()