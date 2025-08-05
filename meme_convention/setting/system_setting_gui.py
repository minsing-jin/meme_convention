import yaml
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from meme_convention.setting.meme_adder import MemeAdder


class SystemSettingsGUI:
    def __init__(self, root=None, yaml_file_path=None, contexts=None):
        if root is None:
            self.root = TkinterDnD.Tk()  # Changed to TkinterDnD.Tk for drag-drop support
            self.root.title("System Settings Manager")
            self.root.geometry("800x600")
        else:
            self.root = root

        self.yaml_file_path = yaml_file_path
        self.settings_data = {}
        self.contexts = contexts

        self.create_widgets()

        if yaml_file_path and os.path.exists(yaml_file_path):
            self.load_yaml_file(yaml_file_path)

    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="System Settings")

        # Meme Adder tab
        self.meme_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.meme_frame, text="Meme Adder")

        self.create_settings_tab()
        self.create_meme_tab()

    def create_settings_tab(self):
        # File operations frame
        file_frame = ttk.LabelFrame(self.settings_frame, text="File Operations", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(file_frame, text="Load YAML File", command=self.load_file_dialog).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Save Changes", command=self.save_yaml_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Apply Changes", command=self.apply_changes).pack(side="left", padx=5)

        # Current file label
        self.file_label = ttk.Label(file_frame, text="No file loaded")
        self.file_label.pack(side="right", padx=5)

        # Settings configuration frame
        config_frame = ttk.LabelFrame(self.settings_frame, text="Settings Configuration", padding=10)
        config_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create scrollable frame
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dictionary to store widgets for dynamic updates
        self.setting_widgets = {}

    def create_meme_tab(self):
        # Initialize MemeAdder in the meme tab
        self.meme_adder = MemeAdder(self.contexts)

    def load_file_dialog(self):
        file_path = filedialog.askopenfilename(
            title="Select YAML Configuration File",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
        )

        if file_path:
            self.load_yaml_file(file_path)

    def load_yaml_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.settings_data = yaml.safe_load(file) or {}

            self.yaml_file_path = file_path
            self.file_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.create_setting_widgets()

            messagebox.showinfo("Success", f"Successfully loaded {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load YAML file:\n{str(e)}")

    def create_setting_widgets(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.setting_widgets.clear()

        # Create widgets for each setting
        row = 0
        for key, value in self.settings_data.items():
            self.create_widget_for_setting(key, value, row)
            row += 1

    def create_widget_for_setting(self, key, value, row, parent=None, prefix=""):
        if parent is None:
            parent = self.scrollable_frame

        full_key = f"{prefix}{key}" if prefix else key

        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            widget = ttk.Checkbutton(parent, text=key, variable=var)
            widget.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=2)
            self.setting_widgets[full_key] = var

        elif isinstance(value, (int, float)):
            ttk.Label(parent, text=f"{key}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            var = tk.StringVar(value=str(value))
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            self.setting_widgets[full_key] = var

        elif isinstance(value, str):
            ttk.Label(parent, text=f"{key}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            var = tk.StringVar(value=value)
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            self.setting_widgets[full_key] = var

        elif isinstance(value, dict):
            # Create a labeled frame for nested dictionaries
            frame = ttk.LabelFrame(parent, text=key, padding=5)
            frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

            nested_row = 0
            for nested_key, nested_value in value.items():
                self.create_widget_for_setting(
                    nested_key, nested_value, nested_row,
                    frame, f"{full_key}."
                )
                nested_row += 1

        elif isinstance(value, list):
            ttk.Label(parent, text=f"{key} (list):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            var = tk.StringVar(value=", ".join(map(str, value)))
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            self.setting_widgets[full_key] = var

    def collect_settings_data(self):
        """Collect data from all widgets and reconstruct the settings dictionary"""
        new_data = {}

        for full_key, widget_var in self.setting_widgets.items():
            keys = full_key.split('.')
            current_dict = new_data

            # Navigate/create nested structure
            for key in keys[:-1]:
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]

            # Set the value
            final_key = keys[-1]
            value = widget_var.get()

            # Try to convert to appropriate type
            if isinstance(widget_var, tk.BooleanVar):
                current_dict[final_key] = value
            elif value.strip() == "":
                current_dict[final_key] = ""
            else:
                # Try to detect and convert the type
                original_value = self.get_original_value(full_key)
                if isinstance(original_value, list):
                    # Handle list values
                    if value.strip():
                        current_dict[final_key] = [item.strip() for item in value.split(',')]
                    else:
                        current_dict[final_key] = []
                elif isinstance(original_value, int):
                    try:
                        current_dict[final_key] = int(value)
                    except ValueError:
                        current_dict[final_key] = value
                elif isinstance(original_value, float):
                    try:
                        current_dict[final_key] = float(value)
                    except ValueError:
                        current_dict[final_key] = value
                else:
                    current_dict[final_key] = value

        return new_data

    def get_original_value(self, full_key):
        """Get the original value for type detection"""
        keys = full_key.split('.')
        current = self.settings_data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return ""

        return current

    def apply_changes(self):
        """Apply changes to the internal data structure immediately"""
        try:
            self.settings_data = self.collect_settings_data()
            messagebox.showinfo("Success", "Changes applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply changes:\n{str(e)}")

    def save_yaml_file(self):
        """Save the current settings to the YAML file"""
        if not self.yaml_file_path:
            file_path = filedialog.asksaveasfilename(
                title="Save YAML Configuration File",
                defaultextension=".yaml",
                filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")]
            )
            if not file_path:
                return
            self.yaml_file_path = file_path

        try:
            # First apply changes to internal data
            self.settings_data = self.collect_settings_data()

            # Then save to file
            with open(self.yaml_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.settings_data, file, default_flow_style=False, sort_keys=False)

            messagebox.showinfo("Success", f"Settings saved to {os.path.basename(self.yaml_file_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save YAML file:\n{str(e)}")

    def run(self):
        if hasattr(self, 'root'):
            self.root.mainloop()
