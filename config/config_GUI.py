import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
from pathlib import Path
import json

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SkillScout Configuration")
        self.root.geometry("1200x800")
        
        # Load config
        self.config = configparser.ConfigParser()
        self.config_file = "config.toml"
        self.load_config()
        
        # Set style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f5f5f5"
        self.card_bg = "#ffffff"
        self.accent_color = "#2196f3"
        self.secondary_color = "#ff9800"
        
        # Configure styles
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), background=self.bg_color)
        style.configure('Section.TLabel', font=('Segoe UI', 14, 'bold'), background=self.bg_color)
        style.configure('Card.TFrame', background=self.card_bg, relief='raised', borderwidth=1)
        style.configure('Accent.TButton', font=('Segoe UI', 10), background=self.accent_color, foreground='white')
        style.configure('Secondary.TButton', font=('Segoe UI', 10), background=self.secondary_color, foreground='white')
        
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                # Simple parsing for TOML-like structure
                content = f.read()
                self.parse_toml(content)
        except FileNotFoundError:
            self.create_default_config()
            
    def parse_toml(self, content):
        """Simple TOML parser for the config structure"""
        self.parsed_config = {
            'extractors': {},
            'transformers': {},
            'loaders': {}
        }
        
        current_section = None
        subsection = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                if '.' in section:
                    current_section, subsection = section.split('.', 1)
                    if subsection not in self.parsed_config[current_section]:
                        self.parsed_config[current_section][subsection] = {}
                else:
                    current_section = section
                    subsection = None
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                if subsection:
                    self.parsed_config[current_section][subsection][key] = value
                else:
                    if current_section not in self.parsed_config:
                        self.parsed_config[current_section] = {}
                    self.parsed_config[current_section][key] = value
                    
    def create_default_config(self):
        """Create default configuration"""
        self.parsed_config = {
            'extractors': {
                'careerjet': {
                    'enabled': 'true',
                    'max_pages': '2',
                    'base_url': 'https://www.careerjet.com.pk/jobs?l=Pakistan&nw=1&s=',
                    'output_path': 'data/raw/careerjet.json',
                    'card': 'ul.jobs li article.job'
                },
                'rozee': {
                    'enabled': 'true',
                    'max_pages': '2',
                    'base_url': 'https://www.rozee.pk/job/jsearch/q/',
                    'output_path': 'data/raw/rozee.json',
                    'card': 'div.job'
                }
            },
            'transformers': {
                'careerjet': {
                    'output_path': 'data/curated/cleaned_careerjet.json',
                    'date_pattern': r'\d+\s+(?:second|minute|hour|day|week|month|year)s?\s+ago'
                },
                'rozee': {
                    'output_path': 'data/curated/cleaned_rozee.json',
                    'date_pattern': r'(\d+)\s+(hour|day|week|month)s?\s+ago'
                }
            },
            'loaders': {
                'dotenv_path': 'config/.env'
            }
        }
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="SkillScout Configuration", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(header_frame, bg=self.bg_color)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="Save Config", 
                  command=self.save_config, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Config", 
                  command=self.load_config_file, style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export JSON", 
                  command=self.export_json, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_extractors_tab()
        self.create_transformers_tab()
        self.create_loaders_tab()
        self.create_preview_tab()
        
    def create_extractors_tab(self):
        """Create extractors configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Extractors")
        
        # General extractors settings
        general_frame = ttk.LabelFrame(tab, text="General Settings", padding=10)
        general_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(general_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.extractors_output_dir = tk.StringVar(value=self.parsed_config.get('extractors', {}).get('output_dir', 'data/raw'))
        ttk.Entry(general_frame, textvariable=self.extractors_output_dir, width=60).grid(row=0, column=1, padx=10, pady=5)
        
        # CareerJet settings
        careerjet_frame = ttk.LabelFrame(tab, text="CareerJet Settings", padding=10)
        careerjet_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_extractor_fields(careerjet_frame, 'careerjet', 0)
        
        # Rozee settings
        rozee_frame = ttk.LabelFrame(tab, text="Rozee Settings", padding=10)
        rozee_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_extractor_fields(rozee_frame, 'rozee', 0)
        
    def create_extractor_fields(self, parent, name, row_start):
        """Create fields for an extractor"""
        extractor_data = self.parsed_config['extractors'].get(name, {})
        
        # Enabled checkbox
        self.var_enabled = tk.BooleanVar(value=extractor_data.get('enabled', 'true').lower() == 'true')
        ttk.Checkbutton(parent, text="Enabled", variable=self.var_enabled).grid(row=row_start, column=0, sticky=tk.W, pady=5)
        setattr(self, f"{name}_enabled", self.var_enabled)
        
        # Max pages
        ttk.Label(parent, text="Max Pages:").grid(row=row_start, column=1, sticky=tk.W, pady=5)
        self.var_max_pages = tk.StringVar(value=extractor_data.get('max_pages', '2'))
        ttk.Entry(parent, textvariable=self.var_max_pages, width=10).grid(row=row_start, column=2, padx=10, pady=5)
        setattr(self, f"{name}_max_pages", self.var_max_pages)
        
        # Base URL
        ttk.Label(parent, text="Base URL:").grid(row=row_start+1, column=0, sticky=tk.W, pady=5)
        self.var_base_url = tk.StringVar(value=extractor_data.get('base_url', ''))
        ttk.Entry(parent, textvariable=self.var_base_url, width=80).grid(row=row_start+1, column=1, columnspan=3, sticky=tk.W, padx=10, pady=5)
        setattr(self, f"{name}_base_url", self.var_base_url)
        
        # Output path
        ttk.Label(parent, text="Output Path:").grid(row=row_start+2, column=0, sticky=tk.W, pady=5)
        self.var_output_path = tk.StringVar(value=extractor_data.get('output_path', ''))
        ttk.Entry(parent, textvariable=self.var_output_path, width=60).grid(row=row_start+2, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_file(self.var_output_path)).grid(row=row_start+2, column=3, padx=5, pady=5)
        setattr(self, f"{name}_output_path", self.var_output_path)
        
        # Card selector
        ttk.Label(parent, text="Card Selector:").grid(row=row_start+3, column=0, sticky=tk.W, pady=5)
        self.var_card = tk.StringVar(value=extractor_data.get('card', ''))
        ttk.Entry(parent, textvariable=self.var_card, width=80).grid(row=row_start+3, column=1, columnspan=3, sticky=tk.W, padx=10, pady=5)
        setattr(self, f"{name}_card", self.var_card)
        
    def create_transformers_tab(self):
        """Create transformers configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transformers")
        
        # General transformers settings
        general_frame = ttk.LabelFrame(tab, text="General Settings", padding=10)
        general_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(general_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.transformers_output_dir = tk.StringVar(value=self.parsed_config.get('transformers', {}).get('output_dir', 'data/curated'))
        ttk.Entry(general_frame, textvariable=self.transformers_output_dir, width=60).grid(row=0, column=1, padx=10, pady=5)
        
        # CareerJet transformer
        careerjet_frame = ttk.LabelFrame(tab, text="CareerJet Transformer", padding=10)
        careerjet_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_transformer_fields(careerjet_frame, 'careerjet', 0)
        
        # Rozee transformer
        rozee_frame = ttk.LabelFrame(tab, text="Rozee Transformer", padding=10)
        rozee_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_transformer_fields(rozee_frame, 'rozee', 0)
        
    def create_transformer_fields(self, parent, name, row_start):
        """Create fields for a transformer"""
        transformer_data = self.parsed_config['transformers'].get(name, {})
        
        # Output path
        ttk.Label(parent, text="Output Path:").grid(row=row_start, column=0, sticky=tk.W, pady=5)
        self.var_trans_output = tk.StringVar(value=transformer_data.get('output_path', ''))
        ttk.Entry(parent, textvariable=self.var_trans_output, width=60).grid(row=row_start, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_file(self.var_trans_output)).grid(row=row_start, column=3, padx=5, pady=5)
        setattr(self, f"trans_{name}_output", self.var_trans_output)
        
        # Date pattern
        ttk.Label(parent, text="Date Pattern (Regex):").grid(row=row_start+1, column=0, sticky=tk.W, pady=5)
        self.var_date_pattern = tk.StringVar(value=transformer_data.get('date_pattern', ''))
        ttk.Entry(parent, textvariable=self.var_date_pattern, width=80).grid(row=row_start+1, column=1, columnspan=3, sticky=tk.W, padx=10, pady=5)
        setattr(self, f"trans_{name}_pattern", self.var_date_pattern)
        
    def create_loaders_tab(self):
        """Create loaders configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Loaders")
        
        frame = ttk.LabelFrame(tab, text="Loader Settings", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Environment File Path:").pack(anchor=tk.W, pady=(0, 5))
        
        loader_data = self.parsed_config.get('loaders', {})
        self.var_dotenv = tk.StringVar(value=loader_data.get('dotenv_path', 'config/.env'))
        
        path_frame = tk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Entry(path_frame, textvariable=self.var_dotenv, width=60).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(path_frame, text="Browse", 
                  command=lambda: self.browse_file(self.var_dotenv)).pack(side=tk.LEFT)
        
        # Status info
        info_frame = ttk.LabelFrame(frame, text="Information", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = tk.Text(info_frame, height=10, wrap=tk.WORD, font=('Consolas', 10))
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info = """Loaders Configuration:
        
• dotenv_path: Path to the environment file containing database credentials
• The .env file should contain connection strings for your database
• Example .env content:
  
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=jobs
  DB_USER=user
  DB_PASSWORD=password
  
• This configuration is used in the final loading stage of the pipeline"""
        
        info_text.insert(1.0, info)
        info_text.config(state=tk.DISABLED)
        
    def create_preview_tab(self):
        """Create preview tab to show the configuration"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Preview")
        
        # Preview text
        self.preview_text = tk.Text(tab, wrap=tk.NONE, font=('Consolas', 10))
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.preview_text.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(tab, orient="horizontal", command=self.preview_text.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.preview_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Update preview button
        ttk.Button(tab, text="Update Preview", 
                  command=self.update_preview, style='Accent.TButton').pack(pady=10)
        
        self.update_preview()
        
    def browse_file(self, variable):
        """Browse for file/directory"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            variable.set(filename)
            
    def gather_data(self):
        """Gather data from all fields"""
        data = {
            'extractors': {
                'output_dir': self.extractors_output_dir.get(),
                'careerjet': {
                    'enabled': str(getattr(self, 'careerjet_enabled').get()).lower(),
                    'max_pages': getattr(self, 'careerjet_max_pages').get(),
                    'base_url': getattr(self, 'careerjet_base_url').get(),
                    'output_path': getattr(self, 'careerjet_output_path').get(),
                    'card': getattr(self, 'careerjet_card').get()
                },
                'rozee': {
                    'enabled': str(getattr(self, 'rozee_enabled').get()).lower(),
                    'max_pages': getattr(self, 'rozee_max_pages').get(),
                    'base_url': getattr(self, 'rozee_base_url').get(),
                    'output_path': getattr(self, 'rozee_output_path').get(),
                    'card': getattr(self, 'rozee_card').get()
                }
            },
            'transformers': {
                'output_dir': self.transformers_output_dir.get(),
                'careerjet': {
                    'output_path': getattr(self, 'trans_careerjet_output').get(),
                    'date_pattern': getattr(self, 'trans_careerjet_pattern').get()
                },
                'rozee': {
                    'output_path': getattr(self, 'trans_rozee_output').get(),
                    'date_pattern': getattr(self, 'trans_rozee_pattern').get()
                }
            },
            'loaders': {
                'dotenv_path': self.var_dotenv.get()
            }
        }
        return data
        
    def update_preview(self):
        """Update the preview tab with current configuration"""
        data = self.gather_data()
        
        # Format as TOML
        preview = "[extractors]\n"
        preview += f"output_dir = \"{data['extractors']['output_dir']}\"\n\n"
        
        for name in ['careerjet', 'rozee']:
            preview += f"[extractors.{name}]\n"
            extractor = data['extractors'][name]
            for key, value in extractor.items():
                preview += f"{key} = '{value}'\n"
            preview += "\n"
            
        preview += "[transformers]\n"
        preview += f"output_dir = \"{data['transformers']['output_dir']}\"\n\n"
        
        for name in ['careerjet', 'rozee']:
            preview += f"[transformers.{name}]\n"
            transformer = data['transformers'][name]
            for key, value in transformer.items():
                preview += f"{key} = '{value}'\n"
            preview += "\n"
            
        preview += "[loaders]\n"
        preview += f"dotenv_path = \"{data['loaders']['dotenv_path']}\"\n"
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, preview)
        
    def save_config(self):
        """Save configuration to file"""
        try:
            data = self.gather_data()
            with open(self.config_file, 'w') as f:
                self.write_toml(data, f)
            messagebox.showinfo("Success", f"Configuration saved to {self.config_file}")
            self.update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            
    def write_toml(self, data, file):
        """Write data in TOML format"""
        # Extractors
        file.write("[extractors]\n")
        file.write(f"output_dir = \"{data['extractors']['output_dir']}\"\n\n")
        
        for name in ['careerjet', 'rozee']:
            file.write(f"[extractors.{name}]\n")
            for key, value in data['extractors'][name].items():
                file.write(f"{key} = '{value}'\n")
            file.write("\n")
            
        # Transformers
        file.write("[transformers]\n")
        file.write(f"output_dir = \"{data['transformers']['output_dir']}\"\n\n")
        
        for name in ['careerjet', 'rozee']:
            file.write(f"[transformers.{name}]\n")
            for key, value in data['transformers'][name].items():
                file.write(f"{key} = '{value}'\n")
            file.write("\n")
            
        # Loaders
        file.write("[loaders]\n")
        file.write(f"dotenv_path = \"{data['loaders']['dotenv_path']}\"\n")
        
    def load_config_file(self):
        """Load configuration from a file"""
        filename = filedialog.askopenfilename(
            filetypes=[("TOML files", "*.toml"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    self.parse_toml(content)
                    self.update_ui_from_config()
                    messagebox.showinfo("Success", "Configuration loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
                
    def update_ui_from_config(self):
        """Update UI fields from loaded configuration"""
        # This is a simplified version - you would need to implement
        # updating all UI fields from self.parsed_config
        messagebox.showinfo("Info", "Configuration loaded - restart application to see changes")
        
    def export_json(self):
        """Export configuration as JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                data = self.gather_data()
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                messagebox.showinfo("Success", f"Configuration exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

def main():
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()