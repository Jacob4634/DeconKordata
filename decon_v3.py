import sqlite3
import sys
import tkinter as tk
from contextlib import closing
from math import pi
from pathlib import Path
from tkinter import messagebox, ttk


MATERIALS = {
    "6082-T6": {"vc": 350, "fz": 0.22},
    "7075-T6": {"vc": 300, "fz": 0.18},
    "S235JR": {"vc": 180, "fz": 0.12},
    "304L": {"vc": 120, "fz": 0.08},
    "316L": {"vc": 100, "fz": 0.07},
}

MACHINES = {
    "Doosan DNM400": 8000,
    "HAAS TM-3": 4000,
    "Doosan Lynx 220LM": 6000,
}

TOOLS = {
    "S610": {"teeth": 2, "diameters": [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20]},
    "S611": {"teeth": 2, "diameters": [3, 4, 5, 6, 8, 10, 12, 14, 16, 20]},
    "S650": {
        "teeth": 3,
        "diameters": [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20],
    },
}


def database_path():
    app_path = Path(sys.executable if getattr(sys, "frozen", False) else __file__)
    return app_path.resolve().with_name("decon.db")


def initialize_database(path):
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS custom_data (
                    material TEXT,
                    machine TEXT,
                    series TEXT,
                    diameter REAL,
                    rpm REAL,
                    feed REAL,
                    ap REAL,
                    ae REAL,
                    PRIMARY KEY (material, machine, series, diameter)
                )
                """
            )


def save_custom_data(path, material, machine, series, diameter, values):
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO custom_data
                    (material, machine, series, diameter, rpm, feed, ap, ae)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (material, machine, series, diameter) DO UPDATE SET
                    rpm = excluded.rpm,
                    feed = excluded.feed,
                    ap = excluded.ap,
                    ae = excluded.ae
                """,
                (
                    material,
                    machine,
                    series,
                    diameter,
                    values["rpm"],
                    values["feed"],
                    values["ap"],
                    values["ae"],
                ),
            )


def load_custom_data(path, material, machine, series, diameter):
    with closing(sqlite3.connect(path)) as connection:
        row = connection.execute(
            """
            SELECT rpm, feed, ap, ae
            FROM custom_data
            WHERE material = ? AND machine = ? AND series = ? AND diameter = ?
            """,
            (material, machine, series, diameter),
        ).fetchone()

    if row is None:
        return None
    return dict(zip(("rpm", "feed", "ap", "ae"), row))


def calculate_optimal_values(recommended_rpm, max_rpm, fz, teeth):
    optimal_rpm = min(recommended_rpm, max_rpm)
    return optimal_rpm, optimal_rpm * fz * teeth


def run_app():
    root = tk.Tk()
    root.title("DeconKordata V5")
    root.geometry("850x950")
    root.configure(bg="#1e1e1e")

    db_path = database_path()
    try:
        initialize_database(db_path)
    except sqlite3.Error as error:
        messagebox.showerror("Databasfel", f"Kunde inte skapa eller öppna decon.db: {error}")
        root.destroy()
        return

    def create_label(parent, text):
        tk.Label(
            parent,
            text=text,
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 10),
        ).pack(pady=(8, 2))

    title = tk.Label(
        root,
        text="DECON KÖRDATA",
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 24, "bold"),
    )
    title.pack(pady=20)

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack()

    create_label(frame, "Material")
    material = ttk.Combobox(
        frame, values=list(MATERIALS.keys()), width=25, state="readonly"
    )
    material.pack()
    material.current(0)

    create_label(frame, "Maskin")
    machine = ttk.Combobox(
        frame, values=list(MACHINES.keys()), width=25, state="readonly"
    )
    machine.pack()
    machine.current(0)

    create_label(frame, "Verktygsserie")
    series = ttk.Combobox(
        frame, values=list(TOOLS.keys()), width=25, state="readonly"
    )
    series.pack()
    series.current(0)

    create_label(frame, "Diameter (mm)")
    diameter = ttk.Combobox(frame, width=25, state="readonly")
    diameter.pack()

    separator = tk.Frame(root, bg="#444444", height=2)
    separator.pack(fill="x", pady=20)

    rpm_rec_label = tk.Label(
        root,
        text="OPTIMALT RPM: -",
        bg="#1e1e1e",
        fg="#00ff66",
        font=("Segoe UI", 18, "bold"),
    )
    rpm_rec_label.pack()

    feed_rec_label = tk.Label(
        root,
        text="OPTIMAL MATNING: -",
        bg="#1e1e1e",
        fg="#00ff66",
        font=("Segoe UI", 18, "bold"),
    )
    feed_rec_label.pack(pady=(0, 12))

    values_frame = tk.LabelFrame(
        root,
        text="MINA VÄRDEN",
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=12,
        pady=5,
    )
    values_frame.pack(pady=4)

    def create_entry(label, initial=""):
        create_label(values_frame, label)
        entry = tk.Entry(
            values_frame,
            width=20,
            justify="center",
            font=("Segoe UI", 12),
        )
        if initial:
            entry.insert(0, initial)
        entry.pack()
        return entry

    rpm_entry = create_entry("Mitt RPM")
    feed_entry = create_entry("Min Matning (mm/min)")
    ap_entry = create_entry("Mitt AP (mm)", "5")
    ae_entry = create_entry("Mitt AE (mm)", "2")

    rpm_actual_label = tk.Label(
        root,
        text="KÖR RPM: -",
        bg="#1e1e1e",
        fg="#4fc3f7",
        font=("Segoe UI", 18, "bold"),
    )
    rpm_actual_label.pack(pady=(14, 5))

    feed_actual_label = tk.Label(
        root,
        text="KÖR MATNING: -",
        bg="#1e1e1e",
        fg="#4fc3f7",
        font=("Segoe UI", 18, "bold"),
    )
    feed_actual_label.pack()

    status_label = tk.Label(
        root,
        text="KLAR",
        bg="#1e1e1e",
        fg="#00ff66",
        font=("Segoe UI", 14, "bold"),
    )
    status_label.pack(pady=12)

    def selected_key():
        return (
            material.get(),
            machine.get(),
            series.get(),
            float(diameter.get()),
        )

    def calculate(event=None):
        try:
            mat = material.get()
            mach = machine.get()
            ser = series.get()
            tool_diameter = float(diameter.get())

            vc = MATERIALS[mat]["vc"]
            fz = MATERIALS[mat]["fz"]
            teeth = TOOLS[ser]["teeth"]
            max_rpm = MACHINES[mach]

            recommended_rpm = (1000 * vc) / (pi * tool_diameter)
            optimal_rpm, optimal_feed = calculate_optimal_values(
                recommended_rpm, max_rpm, fz, teeth
            )

            rpm_rec_label.config(text=f"OPTIMALT RPM: {optimal_rpm:.0f}")
            feed_rec_label.config(
                text=f"OPTIMAL MATNING: {optimal_feed:.0f} mm/min"
            )

            custom_rpm = rpm_entry.get().strip()
            actual_rpm = float(custom_rpm) if custom_rpm else optimal_rpm
            custom_feed = feed_entry.get().strip()
            actual_feed = (
                float(custom_feed)
                if custom_feed
                else actual_rpm * fz * teeth
            )

            rpm_actual_label.config(text=f"KÖR RPM: {actual_rpm:.0f}")
            feed_actual_label.config(
                text=f"KÖR MATNING: {actual_feed:.0f} mm/min"
            )

            if actual_rpm > max_rpm:
                status_label.config(text=f"MAX RPM {max_rpm}", fg="#ff4444")
            else:
                status_label.config(text="OK", fg="#00ff66")
        except (ValueError, KeyError):
            return

    def load_selected_values(event=None):
        try:
            key = selected_key()
            values = load_custom_data(db_path, *key)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Databasfel", f"Kunde inte läsa sparade värden: {error}"
            )
            return
        except (ValueError, KeyError):
            return

        for entry, value, default in (
            (rpm_entry, values["rpm"] if values else None, None),
            (feed_entry, values["feed"] if values else None, None),
            (ap_entry, values["ap"] if values else None, 5),
            (ae_entry, values["ae"] if values else None, 2),
        ):
            entry.delete(0, tk.END)
            value = default if values is None else value
            if value is not None:
                entry.insert(0, str(value))
        calculate()

    def update_diameters(event=None):
        diameters = TOOLS[series.get()]["diameters"]
        diameter["values"] = diameters
        if diameters:
            diameter.current(0)
        load_selected_values()

    def entry_value(entry):
        text = entry.get().strip()
        return float(text) if text else None

    def save_values():
        try:
            key = selected_key()
            values = {
                "rpm": entry_value(rpm_entry),
                "feed": entry_value(feed_entry),
                "ap": entry_value(ap_entry),
                "ae": entry_value(ae_entry),
            }
        except (ValueError, KeyError) as error:
            messagebox.showerror(
                "Ogiltigt värde", f"Ange numeriska värden. {error}"
            )
            return

        try:
            save_custom_data(db_path, *key, values)
        except sqlite3.Error as error:
            messagebox.showerror(
                "Databasfel", f"Kunde inte spara värdena: {error}"
            )
            return

        status_label.config(text="EGNA VÄRDEN SPARADE", fg="#00ff66")

    calculate_button = tk.Button(
        root,
        text="BERÄKNA",
        command=calculate,
        bg="#1e88e5",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=20,
        height=2,
    )
    calculate_button.pack()

    save_button = tk.Button(
        root,
        text="SPARA MINA VÄRDEN",
        command=save_values,
        bg="#43a047",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=20,
        height=2,
    )
    save_button.pack(pady=(8, 0))

    series.bind("<<ComboboxSelected>>", update_diameters)
    material.bind("<<ComboboxSelected>>", load_selected_values)
    machine.bind("<<ComboboxSelected>>", load_selected_values)
    diameter.bind("<<ComboboxSelected>>", load_selected_values)
    rpm_entry.bind("<KeyRelease>", calculate)
    feed_entry.bind("<KeyRelease>", calculate)

    update_diameters()
    root.mainloop()


if __name__ == "__main__":
    run_app()
