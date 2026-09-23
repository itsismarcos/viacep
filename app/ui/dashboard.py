import threading
from datetime import datetime

import customtkinter as ctk

from app.services.viacep import ViaCEPError, lookup_cep, search_address
from app.ui.theme import COLORS, FONTS


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["background"])
        self.history = []
        self.total_queries = 0
        self.found_queries = 0
        self.states = set()
        self.current_view = "dashboard"
        self._build_layout()
        self._update_clock()

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=236, corner_radius=0, fg_color=COLORS["sidebar"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(28, 38))
        ctk.CTkLabel(brand, text="◈", font=("Segoe UI", 28, "bold"), text_color=COLORS["primary"]).pack(side="left")
        ctk.CTkLabel(brand, text="ViaCEP", font=FONTS["brand"], text_color=COLORS["text"]).pack(side="left", padx=9)
        self.nav_buttons = {}
        for key, icon, label in (("dashboard", "⌂", "Visão geral"), ("cep", "⌕", "Consultar CEP"), ("address", "⌖", "Buscar endereço"), ("history", "◷", "Histórico")):
            self.nav_buttons[key] = self._nav_button(sidebar, key, icon, label)
        ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=25)
        info = ctk.CTkFrame(sidebar, fg_color=COLORS["card"], corner_radius=12)
        info.pack(side="bottom", fill="x", padx=15, pady=20)
        ctk.CTkLabel(info, text="SERVIÇO", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=15, pady=(13, 3))
        ctk.CTkLabel(info, text="●  ViaCEP online", font=FONTS["small"], text_color=COLORS["success"]).pack(anchor="w", padx=15, pady=(0, 13))

    def _nav_button(self, parent, key, icon, label):
        button = ctk.CTkButton(parent, text=f"{icon}    {label}", anchor="w", height=44, corner_radius=8, fg_color=COLORS["sidebar_hover"] if key == "dashboard" else "transparent", hover_color=COLORS["sidebar_hover"], text_color=COLORS["text"], font=FONTS["button"], command=lambda: self._select_view(key))
        button.pack(fill="x", padx=15, pady=4)
        return button

    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=36, pady=(30, 12))
        header.grid_columnconfigure(0, weight=1)
        self.title = ctk.CTkLabel(header, text="Visão geral", font=FONTS["title"], text_color=COLORS["text"])
        self.title.grid(row=0, column=0, sticky="w")
        self.subtitle = ctk.CTkLabel(header, text="Consulte endereços brasileiros com rapidez e clareza.", font=FONTS["subtitle"], text_color=COLORS["text_secondary"])
        self.subtitle.grid(row=1, column=0, sticky="w", pady=(3, 0))
        self.clock = ctk.CTkLabel(header, text="", font=FONTS["small"], text_color=COLORS["text_secondary"])
        self.clock.grid(row=0, column=1, rowspan=2, padx=15)
        self._build_stats()
        self.body = ctk.CTkFrame(self.content, fg_color="transparent")
        self.body.grid(row=2, column=0, sticky="nsew", padx=36, pady=(8, 30))
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(1, weight=1)
        self._render_dashboard()

    def _build_stats(self):
        self.stats = ctk.CTkFrame(self.content, fg_color="transparent")
        self.stats.grid(row=1, column=0, sticky="ew", padx=30, pady=8)
        for column in range(4):
            self.stats.grid_columnconfigure(column, weight=1)
        self.stat_labels = {}
        cards = (("total", "Consultas realizadas", "⌕", COLORS["primary"]), ("found", "CEPs encontrados", "✓", COLORS["success"]), ("missing", "Não encontrados", "!", COLORS["warning"]), ("states", "Estados consultados", "◉", COLORS["primary"]))
        for index, (key, label, icon, color) in enumerate(cards):
            card = self._card(self.stats, height=116)
            card.grid(row=0, column=index, sticky="ew", padx=6)
            card.grid_propagate(False)
            ctk.CTkLabel(card, text=icon, font=("Segoe UI", 21, "bold"), text_color=color).pack(anchor="w", padx=17, pady=(13, 0))
            value = ctk.CTkLabel(card, text="0", font=FONTS["number"], text_color=COLORS["text"])
            value.pack(anchor="w", padx=17)
            ctk.CTkLabel(card, text=label, font=FONTS["small"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=17)
            self.stat_labels[key] = value

    def _render_dashboard(self):
        self._clear_body()
        self.title.configure(text="Visão geral")
        self.subtitle.configure(text="Consulte endereços brasileiros com rapidez e clareza.")
        card = self._card(self.body)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text="Consulta rápida", font=FONTS["heading"], text_color=COLORS["text"]).grid(row=0, column=0, sticky="w", padx=20, pady=(17, 2))
        ctk.CTkLabel(card, text="Digite um CEP para preencher o endereço automaticamente.", font=FONTS["small"], text_color=COLORS["text_secondary"]).grid(row=1, column=0, sticky="w", padx=20)
        self.cep_entry = ctk.CTkEntry(card, height=44, placeholder_text="Ex.: 01001-000", font=FONTS["body"], fg_color=COLORS["input"], border_color=COLORS["border"])
        self.cep_entry.grid(row=2, column=0, sticky="ew", padx=(20, 10), pady=17)
        self.cep_entry.bind("<Return>", lambda _event: self._lookup_from_entry())
        ctk.CTkButton(card, text="CONSULTAR", height=44, width=155, corner_radius=8, font=FONTS["button"], fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=self._lookup_from_entry).grid(row=2, column=1, padx=(0, 20), pady=17)
        history = self._card(self.body)
        history.grid(row=1, column=0, sticky="nsew")
        history.grid_columnconfigure(0, weight=1)
        history.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(history, text="Consultas recentes", font=FONTS["heading"], text_color=COLORS["text"]).grid(row=0, column=0, sticky="w", padx=20, pady=17)
        self.history_frame = ctk.CTkScrollableFrame(history, fg_color="transparent")
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self._refresh_history()

    def _render_search_view(self, address_search=False):
        self._clear_body()
        self.title.configure(text="Buscar endereço" if address_search else "Consultar CEP")
        self.subtitle.configure(text="Encontre um endereço informando os dados disponíveis.")
        card = self._card(self.body)
        card.grid(row=0, column=0, sticky="new")
        card.grid_columnconfigure(1, weight=1)
        if address_search:
            fields = (("UF", "uf_entry", "SP"), ("Cidade", "city_entry", "São Paulo"), ("Logradouro", "street_entry", "Praça da Sé"))
            for row, (label, attribute, placeholder) in enumerate(fields):
                ctk.CTkLabel(card, text=label, font=FONTS["small"], text_color=COLORS["text_secondary"]).grid(row=row, column=0, sticky="w", padx=20, pady=(18 if row == 0 else 7, 3))
                entry = ctk.CTkEntry(card, height=42, placeholder_text=placeholder, fg_color=COLORS["input"], border_color=COLORS["border"])
                entry.grid(row=row, column=1, sticky="ew", padx=(12, 20), pady=(14 if row == 0 else 3, 3))
                setattr(self, attribute, entry)
            ctk.CTkButton(card, text="PESQUISAR ENDEREÇOS", height=42, font=FONTS["button"], command=self._search_address).grid(row=3, column=1, sticky="e", padx=20, pady=18)
        else:
            ctk.CTkLabel(card, text="CEP", font=FONTS["small"], text_color=COLORS["text_secondary"]).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 3))
            self.cep_entry = ctk.CTkEntry(card, height=44, placeholder_text="01001-000", fg_color=COLORS["input"], border_color=COLORS["border"])
            self.cep_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(2, 20))
            self.cep_entry.bind("<Return>", lambda _event: self._lookup_from_entry())
            ctk.CTkButton(card, text="CONSULTAR CEP", height=44, width=160, font=FONTS["button"], command=self._lookup_from_entry).grid(row=1, column=1, padx=(0, 20), pady=(2, 20))
        self.result_area = ctk.CTkFrame(self.body, fg_color="transparent")
        self.result_area.grid(row=1, column=0, sticky="nsew", pady=14)
        self.body.grid_rowconfigure(1, weight=1)
        self._show_result_message("Os resultados aparecerão aqui.", COLORS["text_muted"])

    def _render_history_page(self):
        self._clear_body()
        self.title.configure(text="Histórico de consultas")
        self.subtitle.configure(text="Acompanhe os CEPs consultados nesta sessão.")
        card = self._card(self.body)
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        self.history_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.history_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self._refresh_history()

    def _select_view(self, view):
        self.current_view = view
        for key, button in self.nav_buttons.items():
            button.configure(fg_color=COLORS["sidebar_hover"] if key == view else "transparent")
        if view == "dashboard":
            self._render_dashboard()
        elif view == "cep":
            self._render_search_view()
        elif view == "address":
            self._render_search_view(address_search=True)
        else:
            self._render_history_page()

    def _lookup_from_entry(self):
        self._run_async(lambda: lookup_cep(self.cep_entry.get()), self._display_address)

    def _search_address(self):
        self._run_async(lambda: search_address(self.uf_entry.get(), self.city_entry.get(), self.street_entry.get()), self._display_search_results)

    def _run_async(self, operation, success):
        self._show_result_message("Consultando o ViaCEP...", COLORS["primary"])
        threading.Thread(target=self._worker, args=(operation, success), daemon=True).start()

    def _worker(self, operation, success):
        try:
            result = operation()
            self.after(0, lambda: success(result))
        except ViaCEPError as error:
            self.after(0, lambda: self._show_result_message(str(error), COLORS["warning"]))

    def _display_address(self, address):
        self.total_queries += 1
        self.found_queries += 1
        self.states.add(address.uf)
        self.history.insert(0, address)
        self._update_stats()
        self._show_result_message(self._address_text(address), COLORS["success"])
        if self.current_view == "dashboard":
            self._refresh_history()

    def _display_search_results(self, addresses):
        self.total_queries += 1
        self.found_queries += len(addresses)
        self.states.update(address.uf for address in addresses)
        self.history = addresses[:10] + self.history
        self._update_stats()
        if not addresses:
            self._show_result_message("Nenhum endereço encontrado.", COLORS["warning"])
            return
        self._show_result_message("\n\n".join(self._address_text(address) for address in addresses[:8]), COLORS["success"])

    def _address_text(self, address):
        lines = [f"{address.cep}  •  {address.logradouro or 'Logradouro não informado'}", f"{address.bairro or 'Bairro não informado'}  •  {address.localidade}/{address.uf}"]
        details = [item for item in (address.estado, f"DDD {address.ddd}" if address.ddd else "", f"IBGE {address.ibge}" if address.ibge else "") if item]
        if details:
            lines.append("  |  ".join(details))
        return "\n".join(lines)

    def _refresh_history(self):
        if not hasattr(self, "history_frame"):
            return
        for child in self.history_frame.winfo_children():
            child.destroy()
        if not self.history:
            ctk.CTkLabel(self.history_frame, text="Nenhuma consulta nesta sessão.", font=FONTS["body"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=8, pady=12)
            return
        for address in self.history[:10]:
            row = ctk.CTkFrame(self.history_frame, fg_color=COLORS["input"], corner_radius=8)
            row.pack(fill="x", padx=2, pady=4)
            ctk.CTkLabel(row, text=address.cep, width=100, anchor="w", font=FONTS["button"], text_color=COLORS["primary"]).pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(row, text=f"{address.logradouro or 'Endereço não informado'} • {address.localidade}/{address.uf}", anchor="w", font=FONTS["small"], text_color=COLORS["text_secondary"]).pack(side="left", fill="x", expand=True, padx=8)

    def _update_stats(self):
        self.stat_labels["total"].configure(text=str(self.total_queries))
        self.stat_labels["found"].configure(text=str(self.found_queries))
        self.stat_labels["missing"].configure(text=str(max(0, self.total_queries - self.found_queries)))
        self.stat_labels["states"].configure(text=str(len(self.states)))

    def _show_result_message(self, message, color):
        if hasattr(self, "result_area"):
            for child in self.result_area.winfo_children():
                child.destroy()
            ctk.CTkLabel(self.result_area, text=message, justify="left", anchor="nw", font=FONTS["body"], text_color=color).pack(fill="both", expand=True, padx=12, pady=12)

    def _clear_body(self):
        for child in self.body.winfo_children():
            child.destroy()

    @staticmethod
    def _card(parent, height=None):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        if height:
            card.configure(height=height)
        return card

    def _update_clock(self):
        self.clock.configure(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
        self.after(1000, self._update_clock)