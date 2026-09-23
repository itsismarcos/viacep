import customtkinter as ctk


COLORS = {
    "background": "#09111F",
    "sidebar": "#0D1728",
    "sidebar_hover": "#172A46",
    "card": "#111F33",
    "card_hover": "#162940",
    "input": "#0B1729",
    "primary": "#2F80ED",
    "primary_hover": "#2368C4",
    "primary_soft": "#15345D",
    "success": "#35C98B",
    "success_soft": "#123D35",
    "warning": "#F2B84B",
    "warning_soft": "#493617",
    "danger": "#F07178",
    "danger_soft": "#4B202B",
    "text": "#F5F8FC",
    "text_secondary": "#A8B8CC",
    "text_muted": "#70829A",
    "border": "#20344E",
    "border_light": "#2B4564",
}


FONTS = {
    "brand": ("Segoe UI", 18, "bold"),

    "title": ("Segoe UI", 30, "bold"),
    "subtitle": ("Segoe UI", 13),

    "heading": ("Segoe UI", 17, "bold"),
    "body": ("Segoe UI", 13),
    "small": ("Segoe UI", 11),

    "button": ("Segoe UI", 12, "bold"),

    "number": ("Segoe UI", 25, "bold"),
}


def configure_theme():

    ctk.set_appearance_mode("dark")

    ctk.set_default_color_theme("blue")