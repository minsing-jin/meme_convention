import pygame
import os
import random
import threading
from pathlib import Path

MUSIC_PATH = os.path.join(Path("./").parent, 'resources', 'music')


class MusicPlayer:
    """Handles background music playbook with continuity"""

    def __init__(self):
        self.music_folder = MUSIC_PATH
        self.is_playing = False
        self.current_track = None
        self.current_track_path = None
        pygame.mixer.init()

    def get_music_files(self):
        """Get all music files from the specified folder"""
        if not os.path.exists(self.music_folder):
            return []
        return [f for f in os.listdir(self.music_folder)
                if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac'))]

    def play_random_music(self):
        """Play a random music file from the folder"""
        # 이미 음악이 재생 중이면 새로 시작하지 않음
        if self.is_playing and pygame.mixer.music.get_busy():
            print(f"🎵 Music already playing: {self.current_track}")
            return True

        music_files = self.get_music_files()
        if not music_files:
            print(f"No music files found in {self.music_folder}")
            return False

        random_file = random.choice(music_files)
        music_path = os.path.join(self.music_folder, random_file)

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.is_playing = True
            self.current_track = random_file
            self.current_track_path = music_path
            print(f"🎵 Now playing: {random_file}")
            return True
        except pygame.error as e:
            print(f"Error playing music: {e}")
            return False

    def ensure_music_playing(self):
        """Ensure the same music continues playing"""
        if self.is_playing:
            # pygame에서 음악이 실제로 재생 중인지 확인
            if not pygame.mixer.music.get_busy():
                # 음악이 멈췄다면 같은 곡을 다시 재생
                if self.current_track_path and os.path.exists(self.current_track_path):
                    try:
                        pygame.mixer.music.load(self.current_track_path)
                        pygame.mixer.music.play(-1)
                        print(f"🎵 Resuming: {self.current_track}")
                        return True
                    except pygame.error as e:
                        print(f"Error resuming music: {e}")
                        return False
            else:
                print(f"🎵 Music continues: {self.current_track}")
                return True
        return False

    def stop_music(self):
        """Stop the currently playing music"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            print(f"🎵 Music stopped: {self.current_track}")
