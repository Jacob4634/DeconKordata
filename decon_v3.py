import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("DeconKordata V3")
root.geometry("700x500")

title = tk.Label(
    root,
    text="DECON KÖRDATA",
    font=("Segoe UI", 20, "bold")
)

title.pack(pady=20)

tk.Label(root, text="Material").pack()

material = ttk.Combobox(
    root,
    values=[
        "6082-T6",
        "7075-T6",
        "S235JR",
        "304L",
        "316L"
    ]
)

material.pack()

tk.Label(root, text="Maskin").pack()

machine = ttk.Combobox(
    root,
    values=[
        "Doosan DNM400",
        "HAAS TM-3",
        "Doosan Lynx 220LM"
    ]
)

machine.pack()

tk.Label(root, text="Verktygsserie").pack()

series = ttk.Combobox(
    root,
    values=[
        "S610",
        "S611",
        "S650"
    ]
)

series.pack()

button = tk.Button(
    root,
    text="BERÄKNA",
    height=2,
    width=20
)

button.pack(pady=20)

root.mainloop()
