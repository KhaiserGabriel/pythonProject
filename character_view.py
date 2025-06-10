import tkinter as tk
from tkinter import ttk
from .dialogs import Dialogs

class CharacterView:
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        
        # Marco principal
        self.frame = ttk.Frame(parent)
        
        # Treeview para mostrar personajes
        self.tree = ttk.Treeview(
            self.frame,
            columns=("player", "character", "xp", "level"),
            show="headings"
        )
        self.tree.heading("player", text="Jugador")
        self.tree.heading("character", text="Personaje")
        self.tree.heading("xp", text="Experiencia")
        self.tree.heading("level", text="Nivel")
        
        self.tree.column("player", width=150)
        self.tree.column("character", width=150)
        self.tree.column("xp", width=100)
        self.tree.column("level", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de acción
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.add_btn = ttk.Button(
            self.button_frame,
            text="Añadir Personaje",
            command=self.add_character_dialog
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ttk.Button(
            self.button_frame,
            text="Editar Seleccionado",
            command=self.edit_selected_character
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(
            self.button_frame,
            text="Eliminar Seleccionado",
            command=self.delete_selected_character
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Actualizar lista
        self.update_character_list()
    
    def get_frame(self):
        return self.frame
    
    def update_character_list(self):
        """Actualiza la lista de personajes en la interfaz"""
        # Limpiar árbol existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener campaña actual
        campaign = self.manager.get_current_campaign()
        if campaign:
            # Añadir personajes
            for character in campaign.characters:
                self.tree.insert("", tk.END, values=(
                    character.player_name,
                    character.character_name,
                    character.experience,
                    character.level
                ))
    
    def add_character_dialog(self):
        """Muestra diálogo para añadir nuevo personaje"""
        if self.parent.check_campaign():
            result = Dialogs.character_dialog(self.parent)
            if not result["cancelled"] and result["character"]:
                self.manager.add_character(result["character"])
                self.update_character_list()
    
    def edit_selected_character(self):
        """Edita el personaje seleccionado"""
        if not self.parent.check_campaign():
            return
            
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Selección requerida", "Por favor selecciona un personaje", parent=self.parent)
            return
        
        # Obtener índice del personaje seleccionado
        index = self.tree.index(selected[0])
        campaign = self.manager.get_current_campaign()
        if campaign and 0 <= index < len(campaign.characters):
            character = campaign.characters[index]
            result = Dialogs.character_dialog(self.parent, character)
            if not result["cancelled"] and result["character"]:
                self.manager.update_character(index, result["character"])
                self.update_character_list()
    
    def delete_selected_character(self):
        """Elimina el personaje seleccionado"""
        if not self.parent.check_campaign():
            return
            
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Selección requerida", "Por favor selecciona un personaje", parent=self.parent)
            return
        
        # Confirmar eliminación
        if Dialogs.confirm_dialog(self.parent, "Confirmar", "¿Eliminar este personaje?"):
            # Obtener índice del personaje seleccionado
            index = self.tree.index(selected[0])
            campaign = self.manager.get_current_campaign()
            if campaign and 0 <= index < len(campaign.characters):
                del campaign.characters[index]
                self.manager.save_data()
                self.update_character_list()