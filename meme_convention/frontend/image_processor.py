from PIL import Image, ImageTk
import os
import pyperclip
import tempfile


class GIFAnimator:
    def __init__(self, meme_img, label):
        self.meme_img = meme_img
        self.label = label
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.anim_id = None
        self.load_frames()

    def load_frames(self):
        """Load all frames and durations from the GIF"""
        try:
            while True:
                frame = self.meme_img.copy()
                self.frames.append(ImageTk.PhotoImage(frame))
                duration = self.meme_img.info.get('duration', 100)
                self.durations.append(duration)
                self.meme_img.seek(self.meme_img.tell() + 1)
        except EOFError:
            pass

    def start_animation(self):
        """Start the GIF animation"""
        self.current_frame = 0
        self.animate()

    def animate(self):
        """Animate the GIF by cycling through frames"""
        frame = self.frames[self.current_frame]
        self.label.config(image=frame)
        self.label.image = frame

        delay = self.durations[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.anim_id = self.label.after(delay, self.animate)

    def stop_animation(self):
        """Stop the current animation"""
        if self.anim_id is not None:
            self.label.after_cancel(self.anim_id)
            self.anim_id = None


class GIFProcessor:
    def __init__(self):
        pass

    def send_gif_to_clipboard(self, root, meme_io):
        # Save GIF to temporary file and copy file to clipboard
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as temp_file:
            temp_path = temp_file.name

            # Reset BytesIO pointer to beginning
            meme_io.seek(0)

            # Write the original GIF bytes to temp file
            temp_file.write(meme_io.read())

        # Copy the GIF file to clipboard (Windows/macOS specific)
        self.copy_file_to_clipboard(temp_path)

        # Clean up temp file after a delay
        root.after(3000, lambda: self.cleanup_temp_file(temp_path))

    def copy_file_to_clipboard(self, file_path):
        """Copy file to clipboard based on operating system"""
        import platform
        import subprocess

        system = platform.system()

        if system == "Windows":
            # Windows PowerShell method
            cmd = f"Get-Item -LiteralPath '{file_path}' | Set-Clipboard"
            subprocess.run(["powershell", "-command", cmd], shell=True)

        elif system == "Darwin":  # macOS
            # macOS AppleScript method
            script = f'''
               tell application "Finder"
                   set the clipboard to (POSIX file "{os.path.abspath(file_path)}")
               end tell
               '''
            subprocess.run(['osascript', '-e', script])

        elif system == "Linux":
            # Linux xclip method (requires xclip to be installed)
            try:
                subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'text/uri-list', file_path])
            except FileNotFoundError:
                # Fallback: copy file path as text
                pyperclip.copy(file_path)

        else:
            # Fallback: copy file path as text
            pyperclip.copy(file_path)

    def cleanup_temp_file(self, file_path):
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Warning: Could not delete temp file {file_path}: {e}")
