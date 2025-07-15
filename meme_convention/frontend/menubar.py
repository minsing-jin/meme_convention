# import rumps
# from meme_convention.meme_feature.autocomplete import AutoComplete
#
# class MemeMenuBarApp(rumps.App):
#     def __init__(self):
#         super(MemeMenuBarApp, self).__init__("🎭", quit_button=None)
#         self.menu = ["Show Meme", "Settings", "Quit"]
#
#     @rumps.clicked("Show Meme")
#     def show_meme(self, _):
#         # Trigger your meme display function
#         self.show_meme_gui()
#
#     @rumps.clicked("Settings")
#     def settings(self, _):
#         rumps.alert("Settings", "Configure your meme preferences here")
#
#     @rumps.clicked("Quit")
#     def quit_app(self, _):
#         rumps.quit_application()
#
#     def show_meme_gui(self):
#         autocomplete = AutoComplete(None, None, None)
#         autocomplete.gui_display_meme("pr")
#
# if __name__ == "__main__":
#     MemeMenuBarApp().run()
