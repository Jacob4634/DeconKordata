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
    width=25
)
machine.pack()
machine.current(0)

# Serie
create_label("Verktygsserie")

series = ttk.Combobox(
    frame,
    values=list(TOOLS.keys()),
    state="readonly",
    width=25
)
series.pack()
series.current(0)

# Diameter
create_label("Diameter (mm)")

diameter = ttk.Combobox(
    frame,
    state="readonly",
    width=25
)
diameter.pack()

# Skärdjup
create_label("Skärdjup (AP mm)")

ap_entry = tk.Entry(
    frame,
    width=28,
    justify="center"
)
ap_entry.insert(0, "5")
ap_entry.pack()

# Skärbredd
create_label("Skärbredd (AE mm)")

ae_entry = tk.Entry(
    frame,
    width=28,
    justify="center"
)
ae_entry.insert(0, "2")
ae_entry.pack()


rpm_label = tk.Label(
    root,
    text="RPM: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 24, "bold")
)

rpm_label.pack(pady=(30, 10))

feed_label = tk.Label(
    root,
    text="MATNING: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 24, "bold")
)

feed_label.pack()

status_label = tk.Label(
    root,
    text="KLAR",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 14, "bold")
)

status_label.pack(pady=20)


def update_diameters(event=None):

    serie = series.get()

    diameter["values"] = TOOLS[serie]["diameters"]

    if len(diameter["values"]) > 0:
        diameter.current(0)


def calculate():

    mat = material.get()
    mach = machine.get()
    ser = series.get()

    d = float(diameter.get())
    ap = float(ap_entry.get())

    vc = MATERIALS[mat]["vc"]
    fz = MATERIALS[mat]["fz"]

    teeth = TOOLS[ser]["teeth"]
    ap_max = TOOLS[ser]["ap_max"]

    rpm_rec = (1000 * vc) / (pi * d)

    max_rpm = MACHINES[mach]

    rpm_actual = min(
        rpm_rec,
        max_rpm
    )

    feed = rpm_actual * fz * teeth

    rpm_label.config(
        text=f"RPM: {rpm_actual:.0f}"
    )

    feed_label.config(
        text=f"MATNING: {feed:.0f} mm/min"
    )

    warnings = []

    if rpm_rec > max_rpm:
        warnings.append("MASKINENS MAXVARV NÅTT")

    if ap > ap_max:
        warnings.append(
            f"SKÄRDJUP ÖVER MAX ({ap_max} mm)"
        )

    if warnings:

        status_label.config(
            text=" | ".join(warnings),
            fg="#ff4444"
        )

    else:

        status_label.config(
            text="OK",
            fg="#00ff66"
        )


button = tk.Button(
    root,
    text="BERÄKNA",
    command=calculate,
    bg="#1e88e5",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=20,
    height=2
)

button.pack(pady=20)

series.bind(
    "<<ComboboxSelected>>",
    update_diameters
)

update_diameters()
calculate()

root.mainloop()
