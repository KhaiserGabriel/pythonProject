import tkinter as tk
from tkinter import ttk
from .dialogs import Dialogs

class CampaignView:
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
    
    def create_menu(self, menu_bar):
        """Crea el menú de campañas"""
        self.campaign_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Campañas", menu=self.campaign_menu)
        self.campaign_menu.add_command(
            label="Nueva campaña", 
            command=self.create_campaign
        )
        self.campaign_menu.add_separator()
        self.update_campaign_menu()
    
    def update_campaign_menu(self):
        """Actualiza el menú de campañas con las existentes"""
        if hasattr(self, 'campaign_menu'):
            self.campaign_menu.delete(2, tk.END)  # Eliminar campañas anteriores
            for i, campaign in enumerate(self.manager.campaigns):
                self.campaign_menu.add_radiobutton(
                    label=campaign.name,
                    command=lambda idx=i: self.select_campaign(idx),
                    variable=tk.IntVar(value=self.manager.current_campaign_index),
                    value=i
                )
    
    def select_campaign(self, index):
        """Selecciona una campaña existente"""
        if 0 <= index < len(self.manager.campaigns):
            self.manager.current_campaign_index = index
            self.manager.save_data()
            self.parent.update_character_list()
    
    def create_campaign(self):
        """Crea una nueva campaña"""
        name = Dialogs.create_campaign_dialog(self.parent)
        if name:
            self.manager.create_campaign(name)
            self.update_campaign_menu()
            self.parent.update_character_list()
            return True
        return False