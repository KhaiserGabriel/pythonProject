from app.gui import MainWindow
import tkinter as tk

if __name__ == "__main__":
    try:
        app = MainWindow()
        app.protocol("WM_DELETE_WINDOW", app.confirm_exit)
        app.mainloop()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")