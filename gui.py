import tkinter as tk
from tkinter import ttk
from .manager import CharacterManager
from .campaign_view import CampaignView
from .character_view import CharacterView
from .dialogs import Dialogs

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Experiencia - D&D")
        self.geometry("1024x768")
        self.configure(padx=20, pady=20)
        self.fullscreen = False
        
        # Inicializar el gestor de personajes
        self.manager = CharacterManager()
        
        # Crear barra de menú
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # Menú Archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Salir", command=self.confirm_exit)
        
        # Menú Ver
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ver", menu=self.view_menu)
        self.view_menu.add_command(
            label="Pantalla completa", 
            command=self.toggle_fullscreen,
            accelerator="F11"
        )
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Tamaño normal", 
            command=self.normal_size,
            accelerator="Ctrl+0"
        )
        
        # Sistema de campañas
        self.campaign_view = CampaignView(self, self.manager)
        self.campaign_view.create_menu(self.menu_bar)
        
        # Marco principal con pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de personajes
        self.characters_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.characters_tab, text="Personajes")
        
        # Vista de personajes
        self.character_view = CharacterView(self.characters_tab, self.manager)
        self.character_view.get_frame().pack(fill=tk.BOTH, expand=True)
        
        # Botón de salir en la interfaz principal
        self.exit_btn = ttk.Button(
            self,
            text="Salir",
            command=self.confirm_exit
        )
        self.exit_btn.pack(side=tk.BOTTOM, pady=10)
        
        # Configurar atajos de teclado
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Control-0>", self.normal_size)
        self.bind("<Escape>", self.exit_fullscreen)
        
        # Verificar si hay campañas al iniciar
        if not self.manager.campaigns:
            self.after(100, self.campaign_view.create_campaign)
    
    def check_campaign(self):
        """Verifica si hay campaña seleccionada, si no, pide crear una"""
        if not self.manager.get_current_campaign():
            return self.campaign_view.create_campaign()
        return True
    
    def update_character_list(self):
        """Actualiza la lista de personajes"""
        self.character_view.update_character_list()
        
        # Actualizar título de la pestaña
        campaign = self.manager.get_current_campaign()
        if campaign:
            self.notebook.tab(0, text=f"Personajes - {campaign.name}")
    
    def confirm_exit(self):
        """Confirma antes de salir"""
        if Dialogs.confirm_dialog(self, "Salir", "¿Estás seguro de que quieres salir?"):
            self.destroy()
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.attributes("-fullscreen", False)
            self.fullscreen = False
        return "break"
    
    def normal_size(self, event=None):
        self.exit_fullscreen()
        self.geometry("1024x768")
        return "break"