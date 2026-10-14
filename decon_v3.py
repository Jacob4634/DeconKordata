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
        "diameters": [2,3,4,5,6,8,10,12,14,16,20]
    },

    "S611": {
        "teeth": 2,
        "diameters": [3,4,5,6,8,10,12,14,16,20]
    },

    "S650": {
        "teeth": 3,
        "diameters": [1,1.5,2,2.5,3,4,5,6,8,10,12,14,16,20]
    }
}


root = tk.Tk()

root.title("DeconKordata V3")
root.geometry("800x600")

title = tk.Label(
    root,
    text="DECON KÖRDATA",
    font=("Segoe UI", 22, "bold")
)

title.pack(pady=20)

# Material

tk.Label(
    root,
    text="Material"
).pack()

material = ttk.Combobox(
    root,
    values=list(MATERIALS.keys()),
    state="readonly"
)

material.pack()

material.current(0)

# Maskin

tk.Label(
    root,
    text="Maskin"
).pack()

machine = ttk.Combobox(
    root,
    values=list(MACHINES.keys()),
    state="readonly"
)

machine.pack()

machine.current(0)

# Serie

tk.Label(
    root,
    text="Verktygsserie"
).pack()

series = ttk.Combobox(
    root,
    values=["S610", "S611", "S650"],
    state="readonly"
)

series.pack()

series.current(0)

# Diameter

tk.Label(
    root,
    text="Diameter"
).pack()

diameter = ttk.Combobox(
    root,
    state="readonly"
)

diameter.pack()

# Resultat

result = tk.Text(
    root,
    height=15,
    width=70
)

result.pack(
    pady=20
)

def update_diameters(event=None):

    selected = series.get()

    values = TOOLS[selected]["diameters"]

    diameter["values"] = values

    diameter.current(0)

def calculate():

    mat = material.get()
    mach = machine.get()
    ser = series.get()

    d = float(diameter.get())

    vc = MATERIALS[mat]["vc"]
    fz = MATERIALS[mat]["fz"]

    teeth = TOOLS[ser]["teeth"]

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

    text = f"""
MATERIAL
{mat}

MASKIN
{mach}

VERKTYG
{ser}

DIAMETER
{d} mm

----------------------------

REK Vc
{vc:.1f} m/min

REK RPM
{rpm_recommended:.0f}

KÖR RPM
{rpm_actual:.0f}

FAKTISK Vc
{actual_vc:.1f}

Fz
{fz}

SKÄR
{teeth}

MATNING
{feed:.0f} mm/min
"""

    if rpm_recommended > max_rpm:

        text += f"""

VARNING

Maskinen begränsar RPM.

Maskin max:
{max_rpm}
"""

    result.insert(
        tk.END,
        text
    )

button = tk.Button(
    root,
    text="BERÄKNA",
    command=calculate,
    height=2,
    width=20
)

button.pack(pady=10)

series.bind(
    "<<ComboboxSelected>>",
    update_diameters
)

update_diameters()

root.mainloop()
``
