from pathlib import Path
import tkinter as tk
import os

from meme_convention.setting.setting_configuration import SystemSettingsConfiguration
from meme_convention.recommendar.recommender import classify_context_category
from meme_convention.recommendar.text_recorder import TypingRecorder
from meme_convention.setting.music_player import MusicPlayer
from meme_convention.frontend.meme_selection import *

CONTEXT_CATEGORY_PATH = os.path.join(Path(__file__).parent.parent.parent, 'resources', 'local_db')


# TODO: Add hot key condition that will trigger recommend and the autocomplete function
# TODO: Have to consider whether model is instance or string model name.
# TODO: 할것들: system_setting을 pydantic으로 받고 setting값으로 각각 받기
#  , context_category_dialog 인스턴스 받기
class AutoComplete:
    # In your AutoComplete.__init__ method, modify:
    def __init__(self, db,
                 typing_recorder: TypingRecorder,
                 system_settings: SystemSettingsConfiguration,
                 analysis_model="gpt-4o-mini",
                 ):
        self.get_image_from_db_func = db.get_random_meme
        self.analysis_model = analysis_model
        self.accepted_image = None
        self.root = None

        self.typing_recorder = typing_recorder
        self.system_settings = system_settings
        self.music_enabled = system_settings.get_settings().music_enabled

        # Initialize music player only if enabled
        if self.music_enabled:
            self.music_player = MusicPlayer()
            # Start music immediately when autocomplete starts
            if not self.music_player.play_random_music():
                print("❌ Failed to start music, disabling music feature")
                self.music_enabled = False
        else:
            self.music_player = None

    def autocomplete(self):
        """
        1. Implement the gui and autoCopy functionality for the autocomplete.
        2. Autocomplete the multimodal based on the model and context category in the future.
        3. Autocomplete in user's text box and page image context.
        """
        context_category_lst = [name for name in os.listdir(CONTEXT_CATEGORY_PATH) if os.path.isdir(os.path.join(CONTEXT_CATEGORY_PATH, name))]
        try:
            context = classify_context_category(context_category_lst,
                                                self.system_settings.get_settings().allow_screenshot,
                                                self.typing_recorder,
                                                model=self.analysis_model)
            print(f"Context category selected: {context}")

            # Check if music player is initialized
            if self.music_enabled:
                success = self.music_player.ensure_music_playing()
                if success:
                    print("🎵 Same music continues in meme selection")
                else:
                    print("🎵 Music playback issue detected")

            accepted_image = self.display_meme_gui(context)

            if accepted_image:
                print("✅ User accepted an image!")
                return accepted_image
            else:
                print("❌ User didn't accept any image")
                return None

        except ValueError as e:
            print(f"Context category selection cancelled: {e}")
            return None
        except Exception as e:
            print(f"Autocomplete error: {e}")
            return None
        finally:
            self._stop_music()

    def display_meme_gui(self, context):
        """GUI for displaying memes - modified for better cleanup"""
        # Ensure any existing window is closed first
        if self.root:
            try:
                self.root.destroy()
            except:
                pass

        self.root = tk.Toplevel()

        if self.music_enabled and self.music_player:
            current_song = self.music_player.current_track or "Unknown"
            self.root.title(f"Select your meme! 🎵 {current_song}")
            # 음악 연속성 한 번 더 확인
            self.music_player.ensure_music_playing()
        else:
            self.root.title("Select your meme!")

        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()

        if self.music_enabled and self.music_player:
            music_frame = tk.Frame(self.root, bg="#f0f0f0")
            music_frame.pack(fill="x", pady=(0, 10))

            music_label = tk.Label(
                music_frame,
                text=f"🎵 Playing: {self.music_player.current_track or 'Unknown'}",
                font=("Arial", 10, "italic"),
                fg="green",
                bg="#f0f0f0"
            )
            music_label.pack(pady=5)

        label = tk.Label(self.root)
        label.pack()

        gui = MemeSelectionGUI(root=self.root, label=label, img=None, context=context,
                               get_image_func=self.get_image_from_db_func)
        gui.autocomplete_ref = self

        # Create buttons
        btn_accept = tk.Button(self.root, text="Accept (Ctrl + c | Cmd + c)", command=gui.accept)
        btn_accept.pack(side="left", padx=10, pady=10)

        btn_reject = tk.Button(self.root, text="Next Meme (Up/Down key)", command=gui.reject)
        btn_reject.pack(side="left", padx=10, pady=10)

        btn_quit = tk.Button(self.root, text="Exit (esc)",
                             command=lambda: self._handle_exit())
        btn_quit.pack(side="left", padx=10, pady=10)

        # Bind keyboard shortcuts
        self.root.bind('<Control-c>', gui.accept)
        self.root.bind('<Command-c>', gui.accept)
        self.root.bind('<Up>', gui.reject)
        self.root.bind('<Down>', gui.reject)
        self.root.bind('<Escape>', self.quit_and_cleanup)

        # Handle window close button
        self.root.protocol("WM_DELETE_WINDOW", self.quit_and_cleanup)

        # TODO: mainloop is necessary? When I run the autocomplete function, it will block the main thread.
        self.root.mainloop()
        return self.accepted_image if self.accepted_image else None

    # TODO: In the future, this will be a multimodal and text recording classification.
    # TODO: color doesn't work in the button.
    def _handle_reject_with_music_check(self, gui):
        """Reject 처리하면서 음악 연속성 확인"""
        gui.reject()
        # Reject 후에도 같은 음악이 계속 재생되는지 확인
        if self.music_enabled and self.music_player:
            self.music_player.ensure_music_playing()

    def _handle_accept(self, gui):
        """Accept 처리 - 음악은 복사 완료 후 정지"""
        result = gui.accept()
        # accept 처리 후 약간의 지연을 두고 음악 정지
        if self.root:
            self.root.after(2500, self._stop_music)  # AutoCloseMessageBox 시간 고려
        return result

    def _handle_exit(self):
        """Exit 처리 - 즉시 음악 정지"""
        self._stop_music()
        self.quit_and_cleanup()

    def _stop_music(self):
        """음악 정지"""
        if self.music_enabled and self.music_player and self.music_player.is_playing:
            self.music_player.stop_music()
            self.music_enabled = False
            print("🎵 Music stopped - autocomplete process finished")

    def quit_and_cleanup(self, event=None):
        """Properly cleanup and close the window"""
        if self.root:
            self.root.quit()  # Exit mainloop
            self.root.destroy()  # Destroy window
            self.root = None
