import customtkinter as ctk

from app.ui.dashboard import Dashboard
from app.ui.theme import configure_theme


class CEPManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        configure_theme()

        self.title("CEP Manager")
        self.geometry("1280x760")
        self.minsize(1100, 680)

        # Centraliza a janela
        self.update_idletasks()

        width = 1280
        height = 760

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = CEPManagerApp()
    app.mainloop()