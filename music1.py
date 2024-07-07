import os
import tkinter as tk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("300x200")
        
        self.playlist = []
        self.current_track = 0
        self.is_paused = False

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Create GUI Elements
        self.label = tk.Label(self.root, text="No Folder Selected")
        self.label.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.select_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.label.config(text=f"Folder: {os.path.basename(folder_selected)}")
            self.load_music_files(folder_selected)

    def load_music_files(self, folder):
        self.playlist = []
        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                self.playlist.append(os.path.join(folder, file))
        self.current_track = 0

    def play_music(self):
        if self.playlist:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(pygame.USEREVENT)
                self.root.after(100, self.check_music_end)
    
    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.is_paused = False

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.current_track = (self.current_track + 1) % len(self.playlist)
                self.play_music()
        self.root.after(100, self.check_music_end)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
