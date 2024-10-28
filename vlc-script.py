import vlc
import os
import tkinter as tk
from tkinter import messagebox, filedialog

class VideoPlayer:
    def __init__(self, root, folder_path):
        self.root = root
        self.folder_path = folder_path
        self.video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.mp4', '.webp'))]
        self.current_index = 0
        self.delete_alert = False

        # Initialize VLC player instance
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        # Set up GUI
        self.root.title("Video Dataset Curation")
        self.root.geometry("800x600")

        # Video Frame (using a Canvas widget to display VLC video)
        self.video_frame = tk.Canvas(root, bg='black')
        self.video_frame.pack(fill=tk.BOTH, expand=1)

        # Control Frame
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(fill=tk.X, pady=10)

        # Play Next Button
        self.next_button = tk.Button(self.control_frame, text="Next Video", command=self.play_next_video, bg="green", fg="white")
        self.next_button.pack(side=tk.RIGHT, padx=10)
        
        # Rewatch
        self.rewatch_button = tk.Button(self.control_frame, text="Rewatch Video", command=self.rewatch, bg="yellow")
        self.rewatch_button.pack(side=tk.RIGHT, padx=10)

        # Delete Video Button
        self.delete_button = tk.Button(self.control_frame, text="Delete Video", command=self.delete_current_video, bg="red", fg="white")
        self.delete_button.pack(side=tk.RIGHT, padx=10)

        self.goback_button = tk.Button(self.control_frame, text="Previous Video", command=self.go_back, bg="green", fg="white")
        self.goback_button.pack(side=tk.RIGHT, padx=10)

        # Quit Button
        self.quit_button = tk.Button(self.control_frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        # Select Directory Button
        self.select_button = tk.Button(self.control_frame, text="Select Directory", command=self.select_directory)
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.root.bind('<Delete>', lambda event: self.delete_current_video())  # Bind Delete key
        self.root.bind('<Right>', lambda event: self.play_next_video())  # Bind Right Arrow key
        self.root.bind('<Left>', lambda event: self.go_back())  # Bind Right Arrow key

        self.play_video()

    def select_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.folder_path = selected_directory
            self.video_files = [os.path.join(selected_directory, f) for f in os.listdir(selected_directory) if f.endswith(('.mp4', '.webp'))]
            self.current_index = 0
            self.play_video()

    def play_video(self):
        if self.current_index < len(self.video_files):
            media = self.instance.media_new(self.video_files[self.current_index])
            self.player.set_media(media)
            self.player.set_hwnd(self.video_frame.winfo_id())  # Set video output to the canvas
            self.player.play()
            self.root.title(f"Now Playing: {os.path.basename(self.video_files[self.current_index])}")
        else:
            messagebox.showinfo("Info", "No more videos in the folder.")

    def delete_current_video(self):
        current_video = self.video_files[self.current_index]
        if os.path.exists(current_video):
            self.player.stop()
            os.remove(current_video)
            if self.delete_alert == False:
                self.delete_alert = messagebox.askquestion("Deleted", f"Deleted: {os.path.basename(current_video)}, hit 'YES' if you dont want to see this box in the future ",type="yesno")

            self.video_files.pop(self.current_index)
            if self.current_index >= len(self.video_files):
                self.current_index = 0
            self.play_video()

    def play_next_video(self):
        self.player.stop()
        self.current_index = (self.current_index + 1) % len(self.video_files)
        self.play_video()
    
    def go_back(self):
        self.player.stop()
        if self.current_index == 0:
            value = 0
        else:
            value = 1
        self.current_index = (self.current_index - value) % len(self.video_files)
        self.play_video()

    def quit(self):
        self.player.stop()
        self.root.destroy()
    
    def rewatch(self):
        self.player.stop()
        self.play_video()

# Path to folder with videos
folder_path = "./dataset"

# Run the application
root = tk.Tk()
app = VideoPlayer(root, folder_path)
root.mainloop()
