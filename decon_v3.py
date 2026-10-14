import tkinter as tk
from tkinter import ttk
from math import pi

MATERIALS = {
    "6082-T6": {"vc": 350, "fz": 0.06},
    "7075-T6": {"vc": 300, "fz": 0.05},
    "S235JR": {"vc": 180, "fz": 0.04},
    "304L": {"vc": 120, "fz": 0.03},
    "316L": {"vc": 100, "fz": 0.025}
}

MACHINES = {
    "Doosan DNM400": 8000,
    "HAAS TM-3": 4000,
    "Doosan Lynx 220LM": 6000
}

TOOLS = {
    "S610": {
        "teeth": 2,
        "ap_max": 22,
        "diameters": [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20]
    },
    "S611": {
        "teeth": 2,
        "ap_max": 22,
        "diameters": [3, 4, 5, 6, 8, 10, 12, 14, 16, 20]
    },
    "S650": {
        "teeth": 3,
        "ap_max": 22,
        "diameters": [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20]
    }
}

root = tk.Tk()
root.title("DeconKordata V3")
root.geometry("800x700")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="DECON KÖRDATA",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=20)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()


def create_label(text):
    tk.Label(
        frame,
        text=text,
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 10)
    ).pack(pady=(8, 2))


# Material
create_label("Material")

material = ttk.Combobox(
    frame,
    values=list(MATERIALS.keys()),
    state="readonly",
    width=25
)
material.pack()
material.current(0)

# Maskin
create_label("Maskin")

machine = ttk.Combobox(
    frame,
    values=list(MACHINES.keys()),
    state="readonly",
   
