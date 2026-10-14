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
        "diameters": [2,3,4,5,6,8,10,12,14,16,20]
    },
    "S611": {
        "teeth": 2,
        "ap_max": 22,
        "diameters": [3,4,5,6,8,10,12,14,16,20]
    },
    "S650": {
        "teeth": 3,
        "ap_max": 22,
        "diameters": [1,1.5,2,2.5,3,4,5,6,8,10,12,14,16,20]
    }
}

root = tk.Tk()
root.title("DeconKordata V3")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="DECON KÖRDATA",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=20)

top = tk.Frame(root, bg="#1e1e1e")
top.pack()

def label(txt):
    tk.Label(
        top,
        text=txt,
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 10)
    ).pack(pady=(8,2))

label("Material")

material = ttk.Combobox(
    top,
    values=list(MATERIALS.keys()),
    state="readonly",
    width=25
)
material.pack()
material.current(0)

label("Maskin")

machine = ttk.Combobox(
    top,
    values=list(MACHINES.keys()),
    state="readonly",
    width=25
)
machine.pack()
machine.current(0)

label("Verktygsserie")

series = ttk.Combobox(
    top,
    values=list(TOOLS.keys()),
    state="readonly",
    width=25
)
series.pack()
series.current(0)

label("Diameter")

diameter = ttk.Combobox(
    top,
    state="readonly",
    width=25
)
diameter.pack()

label("AP (mm)")

ap_entry = tk.Entry(
    top,
    width=28,
    justify="center"
)
ap_entry.insert(0, "5")
ap_entry.pack()

rpm_label = tk.Label(
    root,
    text="RPM: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 18, "bold")
)
rpm_label.pack(pady=15)

feed_label = tk.Label(
    root,
    text="MATNING: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 18, "bold")
)
feed_label.pack()

status_label = tk.Label(
    root,
    text="KLAR",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 12, "bold")
)
status_label.pack(pady=10)

result = tk.Text(
    root,
    width=90,
    height=15,
    bg="#111111",
    fg="white",
    font=("Consolas", 10)
)
result.pack(pady=20)

def update_diameters(event=None):

    selected = series.get()

    values = TOOLS[selected]["diameters"]

    diameter["values"] = values

    if values:
        diameter.current(0)

def calculate():

    result.delete("1.0", tk.END)

    mat = material.get()
    mach = machine.get()
    ser = series.get()

    d = float(diameter.get())
    ap = float(ap_entry.get())

    vc = MATERIALS[mat]["vc"]
    fz = MATERIALS[mat]["fz"]

    teeth = TOOLS[ser]["teeth"]
    ap_max = TOOLS[ser]["ap_max"]

    max_rpm = MACHINES[mach]

    rpm_rec = (1000 * vc) / (pi * d)
    rpm = min(rpm_rec, max_rpm)

    actual_vc = (rpm * pi * d) / 1000
    feed = rpm * fz * teeth

    rpm_label.config(
        text=f"RPM: {rpm:.0f}"
    )

    feed_label.config(
        text=f"MATNING: {feed:.0f} mm/min"
    )

    warning = False

    if rpm_rec > max_rpm:
        warning = True

    if ap > ap_max:
        warning = True

    if warning:
        status_label.config(
            text="VARNING",
            fg="#ff5555"
        )
    else:
        status_label.config(
            text="OK",
            fg="#00ff66"
        )

    result.insert(
        tk.END,
        f"""
Material: {mat}
Maskin: {mach}
Serie: {ser}

Diameter: {d} mm
AP: {ap} mm

Vc Rek: {vc}
Vc Faktisk: {actual_vc:.1f}

RPM Rek: {rpm_rec:.0f}
RPM Kör: {rpm:.0f}

Fz: {fz}
Skär: {teeth}

Matning: {feed:.0f} mm/min

AP Max: {ap_max}
"""
    )

    if rpm_rec > max_rpm:
        result.insert(
            tk.END,
            f"\nVARNING: Maskinen begränsar RPM ({max_rpm})"
        )

    if ap > ap_max:
        result.insert(
            tk.END,
            f"\nVARNING: AP över max ({ap_max})"
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

button.pack(pady=10)

series.bind(
    "<<ComboboxSelected>>",
    update_diameters
)

update_diameters()

root.mainloop()
