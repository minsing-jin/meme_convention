# from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
# from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtCore import QTimer
# import sys
#
#
# class AnimatedTrayIcon:
#     def __init__(self):
#         self.app = QApplication(sys.argv)
#         self.app.setQuitOnLastWindowClosed(False)
#
#         # Create tray icon
#         self.tray = QSystemTrayIcon()
#         self.tray.setVisible(True)
#
#         # Load GIF frames
#         self.frames = []
#         self.current_frame = 0
#         self.load_gif_frames()
#
#         # Set up animation timer
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_icon)
#         self.timer.start(100)  # Update every 100ms
#
#         # Create context menu
#         menu = QMenu()
#         quit_action = menu.addAction("Quit")
#         quit_action.triggered.connect(self.app.quit)
#         self.tray.setContextMenu(menu)
#
#     def load_gif_frames(self):
#         # Load your GIF frames here
#         # Convert each frame to QIcon
#         pass
#
#     def update_icon(self):
#         if self.frames:
#             self.tray.setIcon(self.frames[self.current_frame])
#             self.current_frame = (self.current_frame + 1) % len(self.frames)
#
#     def run(self):
#         self.app.exec_()
#
#
# if __name__ == "__main__":
#     app = AnimatedTrayIcon()
#     app.run()
