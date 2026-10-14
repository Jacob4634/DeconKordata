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
root.geometry("850x700")

title = tk.Label(
    root,
    text="DECON KÖRDATA",
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=20)

# Material

tk.Label(root, text="Material").pack()

material = ttk.Combobox(
    root,
    values=list(MATERIALS.keys()),
    state="readonly"
)

material.pack()
material.current(0)

# Maskin

tk.Label(root, text="Maskin").pack()

machine = ttk.Combobox(
    root,
    values=list(MACHINES.keys()),
    state="readonly"
)

machine.pack()
machine.current(0)

# Serie

tk.Label(root, text="Verktygsserie").pack()

series = ttk.Combobox(
    root,
    values=["S610", "S611", "S650"],
    state="readonly"
)

series.pack()
series.current(0)

# Diameter

tk.Label(root, text="Diameter (mm)").pack()

diameter = ttk.Combobox(
    root,
    state="readonly"
)

diameter.pack()

# AP

tk.Label(root, text="AP (mm)").pack()

ap_entry = tk.Entry(root)
ap_entry.insert(0, "5")
ap_entry.pack()

# Resultat

result = tk.Text(
    root,
    width=80,
    height=18,
    font=("Consolas", 10)
)

result.pack(pady=15)

def update_diameters(event=None):

    selected = series.get()

    diameter["values"] = TOOLS[selected]["diameters"]

    if len(diameter["values"]) > 0:
        diameter.current(0)

def calculate():

    mat = material.get()
    mach = machine.get()
    ser = series.get()

    d = float(diameter.get())

    ap_value = float(ap_entry.get())

    vc = MATERIALS[mat]["vc"]
    fz = MATERIALS[mat]["fz"]

    teeth = TOOLS[ser]["teeth"]
    ap_max = TOOLS[ser]["ap_max"]

    max_rpm = MACHINES[mach]

    rpm_recommended = (
        1000 * vc
    ) / (
        pi * d
    )

    rpm_actual = min(
        rpm_recommended,
        max_rpm
    )

    actual_vc = (
        rpm_actual *
        pi *
        d
    ) / 1000

    feed = (
        rpm_actual *
        fz *
        teeth
    )

    result.delete(
        "1.0",
        tk.END
    )

    output = f"""
MATERIAL
{mat}

MASKIN
{mach}

VERKTYG
{ser}

DIAMETER
{d:.1f} mm

AP
{ap_value:.1f} mm

-----------------------------------

REKOMMENDERAD Vc
{vc:.1f} m/min

REKOMMENDERAT RPM
{rpm_recommended:.0f}

MASK
