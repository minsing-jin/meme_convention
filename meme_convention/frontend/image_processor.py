from PIL import Image, ImageTk
import os
import pyperclip
import tempfile


def play_animated_image(meme_img, label, anim_id=None):
    """
    Play an animated GIF image in a Tkinter label widget.
    :param meme_img: PIL Image object of the animated GIF.
    :param label: Tkinter Label widget where the GIF will be displayed.
    :param anim_id: Optional ID for the animation callback, used to stop the animation.

    :return: The ID of the animation callback. This can be used to stop the animation later.
    anmin_id is for preventing multiple animations running at the same time when user draw another meme.
    """
    frames = []
    durations = []
    try:
        while True:
            frame = meme_img.copy()
            frames.append(ImageTk.PhotoImage(frame))
            duration = meme_img.info.get('duration', 100)
            durations.append(duration)
            meme_img.seek(meme_img.tell() + 1)
    except EOFError:
        pass
    current_frame = 0
    anim_id = animate_gif(current_frame=current_frame, frames=frames,
                          durations=durations, label=label, anim_id=anim_id)
    return anim_id


def animate_gif(current_frame, frames, durations, label, anim_id=None):
    frame = frames[current_frame]
    label.config(image=frame)
    label.image = frame
    delay = durations[current_frame]
    current_frame = (current_frame + 1) % len(frames)
    anim_id = label.after(delay,
                          lambda cf=current_frame: animate_gif(cf, frames,
                                                               durations, label, anim_id))
    return anim_id


class GifProcessor:
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
