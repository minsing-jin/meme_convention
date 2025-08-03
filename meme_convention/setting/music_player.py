import pygame
import os
import random
import threading
import time

MUSIC_PATH = os.path.join(os.getcwd(), 'resources', 'music')

# TODO: add youtube music collection player
class MusicPlayer:
    """Handles background music playback with continuity"""

    def __init__(self):
        self.music_folder = MUSIC_PATH
        self.is_playing = False
        self.current_track = None
        self.current_track_path = None
        self._mixer_initialized = False
        self._init_mixer()

    def _init_mixer(self):
        """Initialize pygame mixer safely"""
        try:
            if not self._mixer_initialized:
                pygame.mixer.quit()  # Ensure clean state
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
                self._mixer_initialized = True
                print("🎵 pygame mixer initialized successfully")
        except pygame.error as e:
            print(f"❌ Failed to initialize pygame mixer: {e}")
            self._mixer_initialized = False

    def get_music_files(self):
        """Get all music files from the specified folder"""
        if not os.path.exists(self.music_folder):
            print(f"❌ Music folder not found: {self.music_folder}")
            return []

        music_files = [f for f in os.listdir(self.music_folder)
                       if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac'))]
        print(f"🎵 Found {len(music_files)} music files in {self.music_folder}")
        return music_files

    def play_random_music(self):
        """Play a random music file from the folder"""
        if not self._mixer_initialized:
            print("❌ pygame mixer not initialized")
            return False

        # Check if music is already playing
        if self.is_playing and pygame.mixer.music.get_busy():
            print(f"🎵 Music already playing: {self.current_track}")
            return True

        music_files = self.get_music_files()
        if not music_files:
            print(f"❌ No music files found in {self.music_folder}")
            return False

        random_file = random.choice(music_files)
        music_path = os.path.join(self.music_folder, random_file)

        try:
            # Stop any currently playing music
            pygame.mixer.music.stop()
            time.sleep(0.1)  # Small delay for cleanup

            # Load and play new music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely

            self.is_playing = True
            self.current_track = random_file
            self.current_track_path = music_path
            print(f"🎵 Now playing: {random_file}")
            return True

        except pygame.error as e:
            print(f"❌ Error playing music: {e}")
            self.is_playing = False
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.is_playing = False
            return False

    def ensure_music_playing(self):
        """Ensure the same music continues playing"""
        if not self._mixer_initialized:
            return False

        if self.is_playing:
            # Check if pygame music is actually playing
            if not pygame.mixer.music.get_busy():
                # Music stopped, try to resume the same track
                if self.current_track_path and os.path.exists(self.current_track_path):
                    try:
                        pygame.mixer.music.load(self.current_track_path)
                        pygame.mixer.music.play(-1)
                        print(f"🎵 Resuming: {self.current_track}")
                        return True
                    except pygame.error as e:
                        print(f"❌ Error resuming music: {e}")
                        self.is_playing = False
                        return False
                else:
                    print("❌ Current track path not found")
                    self.is_playing = False
                    return False
            else:
                print(f"🎵 Music continues: {self.current_track}")
                return True
        else:
            # No music playing, start new music
            return self.play_random_music()

    def stop_music(self):
        """Stop the currently playing music"""
        if self._mixer_initialized and self.is_playing:
            try:
                pygame.mixer.music.stop()
                self.is_playing = False
                print(f"🎵 Music stopped: {self.current_track}")
            except pygame.error as e:
                print(f"❌ Error stopping music: {e}")

    def cleanup(self):
        """Clean up pygame mixer resources"""
        try:
            if self._mixer_initialized:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                self._mixer_initialized = False
                print("🎵 pygame mixer cleaned up")
        except:
            pass
