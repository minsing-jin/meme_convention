import io
from PIL import Image, ImageTk, ImageSequence
from meme_convention.db.user import User
import tkinter as tk

def sample_image_upload(context_category, picture_name, path_to_image):
    user = User()
    # # Example usage
    user.upload_meme(context_category, picture_name, path_to_image)

    meme = user.get_random_meme("pr")
    if meme:
        img = Image.open(io.BytesIO(bytes(meme[-1])))
        img.show()
    else:
        print("No memes found for the specified category.")

def extract_gif_frames(img):
    return [frame.copy() for frame in ImageSequence.Iterator(img)]

#
# def build_header_frame(self, parent):
#     header = tk.Frame(parent, bg="#374151", height=60)
#     header.pack(fill="x")
#     tk.Label(header, text="Select Context Category", font=("Arial", 18, "bold"), fg="white", bg="#374151").pack(
#         expand=True)
#     return header
#
#
# def build_instructions(parent):
#     tk.Label(parent, text="Type category shortcut or click a button.",
#              font=("Arial", 12), fg="white", bg="#1f2937").pack(pady=(0, 18))
#
#
# def build_button_grid(parent, categories, prefixes, on_select):
#     cols = min(5, max(2, (len(categories) + 1) // 2))
#     rows = (len(categories) + cols - 1) // cols
#     frame = tk.Frame(parent, bg="#1f2937")
#     frame.pack(expand=True, fill="both")
#     buttons = {}
#     for i, cat in enumerate(categories):
#         row, col = divmod(i, cols)
#         shortcut = prefixes[cat]
#         btn = tk.Button(frame, text=f"{cat.upper()}\n({shortcut.upper()})",
#                         command=lambda c=cat: on_select(c),
#                         width=10, height=2, bg="#e2e8f0", fg="black",
#                         font=("Arial", 11, "bold"))
#         btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
#         buttons[cat] = btn
#     for i in range(cols): frame.columnconfigure(i, weight=1)
#     for i in range(rows): frame.rowconfigure(i, weight=1)
#     return frame, buttons
#
#
# def build_selection_display(parent, selected_context):
#     frame = tk.Frame(parent, bg="#1f2937")
#     frame.pack(pady=12)
#     tk.Label(frame, text="Current Selection:", font=("Arial", 12, "bold"),
#              fg="white", bg="#1f2937").pack(side="left", padx=4)
#     tk.Label(frame, textvariable=selected_context,
#              font=("Arial", 12, "bold"), fg="white", bg="#3182ce",
#              padx=14, pady=4, relief="ridge").pack(side="left", padx=8)
#
#
# def build_control_buttons(parent, on_confirm, on_cancel):
#     frame = tk.Frame(parent, bg="#1f2937")
#     frame.pack(fill="x", padx=24, pady=(0, 18))
#     btns = tk.Frame(frame, bg="#1f2937")
#     btns.pack()
#     tk.Button(btns, text="✓ Confirm (Enter)", command=on_confirm,
#               bg="#22c55e", fg="black", font=("Arial", 11, "bold"),
#               width=15, height=1).pack(side="left", padx=10)
#     tk.Button(btns, text="✗ Exit (Esc)", command=on_cancel,
#               bg="#ef4444", fg="black", font=("Arial", 11, "bold"),
#               width=12, height=1).pack(side="left", padx=10)
#
#
# # These can also go to utils or kept as methods:
# def select_and_highlight(cat, selected_context, buttons):
#     for k, btn in buttons.items():
#         if k == cat:
#             btn.config(highlightbackground="#34d399", highlightcolor="#34d399")
#         else:
#             btn.config(highlightbackground="#e2e8f0", highlightcolor="#e2e8f0")
#     selected_context.set(cat)
#
#
# def confirm(root, context_confirmed, user_selected_context, selected_context):
#     context_confirmed = True
#     user_selected_context = selected_context.get()
#     root.destroy()
#
#
# def cancel(root, context_confirmed):
#     context_confirmed = False
#     root.destroy()