import tkinter as tk
from tkinter import ttk
from math import pi

MATERIALS = {
    "6082-T6": {"vc": 350, "fz": 0.22},
    "7075-T6": {"vc": 300, "fz": 0.18},
    "S235JR": {"vc": 180, "fz": 0.12},
    "304L": {"vc": 120, "fz": 0.08},
    "316L": {"vc": 100, "fz": 0.07}
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
root.title("DeconKordata V4")
root.geometry("850x850")
root.configure(bg="#1e1e1e")


def create_label(parent, text):
    tk.Label(
        parent,
        text=text,
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 10)
    ).pack(pady=(8, 2))


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

create_label(frame, "Material")

material = ttk.Combobox(
    frame,
    values=list(MATERIALS.keys()),
    width=25,
    state="readonly"
)
material.pack()
material.current(0)

create_label(frame, "Maskin")

machine = ttk.Combobox(
    frame,
    values=list(MACHINES.keys()),
    width=25,
    state="readonly"
)
machine.pack()
machine.current(0)

create_label(frame, "Verktygsserie")

series = ttk.Combobox(
    frame,
    values=list(TOOLS.keys()),
    width=25,
    state="readonly"
)
series.pack()
series.current(0)

create_label(frame, "Diameter (mm)")

diameter = ttk.Combobox(
    frame,
    width=25,
    state="readonly"
)
diameter.pack()

create_label(frame, "Skärdjup AP (mm)")

ap_entry = tk.Entry(
    frame,
    width=28,
    justify="center"
)
ap_entry.insert(0, "5")
ap_entry.pack()

create_label(frame, "Skärbredd AE (mm)")

ae_entry = tk.Entry(
    frame,
    width=28,
    justify="center"
)
ae_entry.insert(0, "2")
ae_entry.pack()

separator = tk.Frame(
    root,
    bg="#444444",
    height=2
)
separator.pack(fill="x", pady=20)

rpm_rec_label = tk.Label(
    root,
    text="REK RPM: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 18, "bold")
)
rpm_rec_label.pack()

feed_rec_label = tk.Label(
    root,
    text="REK MATNING: -",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 18, "bold")
)
feed_rec_label.pack(pady=(0, 20))

create_label(root, "Eget RPM")

rpm_entry = tk.Entry(
    root,
    width=20,
    justify="center",
    font=("Segoe UI", 12)
)
rpm_entry.pack()

rpm_actual_label = tk.Label(
    root,
    text="KÖR RPM: -",
    bg="#1e1e1e",
    fg="#4fc3f7",
    font=("Segoe UI", 18, "bold")
)
rpm_actual_label.pack(pady=(25, 5))

feed_actual_label = tk.Label(
    root,
    text="KÖR MATNING: -",
    bg="#1e1e1e",
    fg="#4fc3f7",
    font=("Segoe UI", 18, "bold")
)
feed_actual_label.pack()

status_label = tk.Label(
    root,
    text="KLAR",
    bg="#1e1e1e",
    fg="#00ff66",
    font=("Segoe UI", 14, "bold")
)
status_label.pack(pady=25)


def update_diameters(event=None):

    selected = series.get()

    vals = TOOLS[selected]["diameters"]

    diameter["values"] = vals

    if vals:
        diameter.current(0)

    calculate()


def calculate(event=None):

    try:

        mat = material.get()
        mach = machine.get()
        ser = series.get()

        d = float(diameter.get())

        vc = MATERIALS[mat]["vc"]
        fz = MATERIALS[mat]["fz"]

        teeth = TOOLS[ser]["teeth"]

        max_rpm = MACHINES[mach]

        rpm_recommended = (1000 * vc) / (pi * d)

        feed_recommended = (
            rpm_recommended *
            fz *
            teeth
        )

        rpm_rec_label.config(
            text=f"REK RPM: {rpm_recommended:.0f}"
        )

        feed_rec_label.config(
            text=f"REK MATNING: {feed_recommended:.0f} mm/min"
        )

        text_rpm = rpm_entry.get().strip()

        if text_rpm == "":
            actual_rpm = rpm_recommended
        else:
            actual_rpm = float(text_rpm)

        actual_feed = (
            actual_rpm *
            fz *
            teeth
        )

        rpm_actual_label.config(
            text=f"KÖR RPM: {actual_rpm:.0f}"
        )

        feed_actual_label.config(
            text=f"KÖR MATNING: {actual_feed:.0f} mm/min"
        )

        warnings = []

        if actual_rpm > max_rpm:
            warnings.append(
                f"MAX RPM {max_rpm}"
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

    except:
        pass


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

button.pack()

series.bind("<<ComboboxSelected>>", update_diameters)

material.bind("<<ComboboxSelected>>", calculate)
machine.bind("<<ComboboxSelected>>", calculate)
diameter.bind("<<ComboboxSelected>>", calculate)

rpm_entry.bind("<KeyRelease>", calculate)

update_diameters()

root.mainloop()
