import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from .models import Character

class Dialogs:
    @staticmethod
    def create_campaign_dialog(parent):
        """Diálogo para crear una nueva campaña"""
        name = simpledialog.askstring("Nueva Campaña", "Nombre de la campaña:", parent=parent)
        return name
    
    @staticmethod
    def character_dialog(parent, character=None):
        """Diálogo para editar/añadir personaje"""
        dialog = tk.Toplevel(parent)
        dialog.title("Editar Personaje" if character else "Nuevo Personaje")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Variables para los campos
        player_name = tk.StringVar(value=character.player_name if character else "")
        character_name = tk.StringVar(value=character.character_name if character else "")
        experience = tk.StringVar(value=character.experience if character else 0)
        level = tk.StringVar(value=character.level if character else 1)
        
        # Formulario
        ttk.Label(dialog, text="Jugador:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        player_entry = ttk.Entry(dialog, textvariable=player_name, width=30)
        player_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(dialog, text="Personaje:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        char_entry = ttk.Entry(dialog, textvariable=character_name, width=30)
        char_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(dialog, text="Experiencia:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        exp_entry = ttk.Entry(dialog, textvariable=experience)
        exp_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Nivel:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        level_entry = ttk.Entry(dialog, textvariable=level)
        level_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botones
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        result = {"character": None, "cancelled": True}
        
        def save_character():
            try:
                result["character"] = Character(
                    player_name.get(),
                    character_name.get(),
                    int(experience.get()),
                    int(level.get())
                )
                result["cancelled"] = False
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Experiencia y nivel deben ser números", parent=dialog)
        
        ttk.Button(btn_frame, text="Guardar", command=save_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configuración de la ventana
        dialog.resizable(False, False)
        dialog.columnconfigure(1, weight=1)
        dialog.wait_window()
        
        return result
    
    @staticmethod
    def confirm_dialog(parent, title, message):
        """Diálogo de confirmación"""
        return messagebox.askyesno(title, message, parent=parent)