from re import split
from TeamMember import TeamMember
import csv
import tkinter as tk
from tkinter import ttk
from constants import pits_limit, scouting_limit, drive_limit, member_pits_max, leads_pits_max, scouting_max

# Master list of TeamMember objects
team_members = []

# Keep original finished_dict structure
finished_dict = {
    "8-9": [],
    "9-10": [],
    "10-11": [],
    "11-12": [],
    "12-1": [],
    "1-2": [],
    "2-3": [],
    "3-4": [],
    "4-5": [],
    "5-6": [],
}

# -----------------------------
# Read CSV and create TeamMember objects (merge duplicate names)
# -----------------------------
def process_csv():
    members_map = {}
    with open('response.csv', mode='r', newline='', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        first = next(csvFile, None)
        if first is None:
            return
        if any("name" in cell.lower() for cell in first):
            pass
        else:
            csvFile = [first] + list(csvFile)
        for line in csvFile:
            if not line or len(line) < 4:
                continue
            name = line[1].strip()
            position = line[2].strip()
            available_timings = [t.strip() for t in line[3].split(",") if t.strip()]

            if name in members_map:
                existing = members_map[name]
                for t in available_timings:
                    if t not in existing["timings"]:
                        existing["timings"].append(t)
                existing_pos = existing["position"].title()
                new_pos = position.title()
                priority = {"Drive Team": 3, "Lead": 2, "Member": 1}
                if priority.get(new_pos, 0) > priority.get(existing_pos, 0):
                    existing["position"] = new_pos
            else:
                members_map[name] = {"position": position.title(), "timings": available_timings}

    for name, info in members_map.items():
        team_members.append(TeamMember(name, info["timings"], info["position"]))

# -----------------------------
# Scheduling algorithm
# -----------------------------
def schedule_teammates():
    for time_slot in list(finished_dict.keys()):
        available_members = [m for m in team_members if time_slot in m.available_timings]

        pits = []
        scouting = []
        drive_team = []
        stands = []

        # Drive Team (permanent)
        drive_candidates = [m for m in available_members if m.position == "Drive Team"]
        picked = drive_candidates[:drive_limit]
        for m in picked:
            drive_team.append(m.name)
            m.assign_drive()
            available_members.remove(m)

        # Pits: Leads first
        lead_candidates = [m for m in available_members if m.position == "Lead" and m.can_do("Pits") and m.pits_count < leads_pits_max]
        for m in lead_candidates:
            if len(pits) >= pits_limit:
                break
            pits.append(m.name)
            m.assign_pits()
            available_members.remove(m)

        # Pits: Members next
        member_candidates = [m for m in available_members if m.position == "Member" and m.can_do("Pits") and m.pits_count < member_pits_max]
        for m in member_candidates:
            if len(pits) >= pits_limit:
                break
            pits.append(m.name)
            m.assign_pits()
            available_members.remove(m)

        # Scouting
        scouting_candidates = [m for m in available_members if m.can_do("Scouting") and m.scouting_count < scouting_max]
        for m in scouting_candidates:
            if len(scouting) >= scouting_limit:
                break
            scouting.append(m.name)
            m.assign_scouting()
            available_members.remove(m)

        # Stands
        for m in available_members:
            stands.append(m.name)
            m.assign_stands()

        finished_dict[time_slot] = [pits, scouting, drive_team, stands]

# -----------------------------
# Tkinter: list view
# -----------------------------
def show_schedule():
    window = tk.Tk()
    window.title("Schedule")

    canvas = tk.Canvas(window)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    row = 0
    for time_slot, roles in finished_dict.items():
        pits, scouting, drive_team, stands = roles

        tk.Label(scrollable_frame, text=f"{time_slot}", font=("Arial", 14, "bold")).grid(row=row, column=0, sticky="w", padx=5, pady=(8,2))
        row += 1

        tk.Label(scrollable_frame, text="  Drive Team:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=20)
        tk.Label(scrollable_frame, text=", ".join(drive_team) if drive_team else "None").grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(scrollable_frame, text="  Pits:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=20)
        tk.Label(scrollable_frame, text=", ".join(pits) if pits else "None").grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(scrollable_frame, text="  Scouting:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=20)
        tk.Label(scrollable_frame, text=", ".join(scouting) if scouting else "None").grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(scrollable_frame, text="  Stands:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=20)
        tk.Label(scrollable_frame, text=", ".join(stands) if stands else "None").grid(row=row, column=1, sticky="w")
        row += 1

    # Add button to open grid view
    tk.Button(window, text="Open Grid View", command=show_grid_view).pack(pady=10)

    window.mainloop()

# -----------------------------
# Tkinter: grid view
# -----------------------------
def show_grid_view():
    grid_window = tk.Toplevel()
    grid_window.title("Schedule Grid View")

    time_slots = list(finished_dict.keys())
    roles = ["Drive Team", "Pits", "Scouting", "Stands"]

    # Top row = time slots
    for col, time_slot in enumerate(time_slots, start=1):
        tk.Label(grid_window, text=time_slot, font=("Arial", 12, "bold"),
                 borderwidth=1, relief="solid", padx=5, pady=5).grid(row=0, column=col, sticky="nsew")

    # First col = role names
    for row, role in enumerate(roles, start=1):
        tk.Label(grid_window, text=role, font=("Arial", 12, "bold"),
                 borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row, column=0, sticky="nsew")

    # Fill cells with assigned names
    for col, time_slot in enumerate(time_slots, start=1):
        pits, scouting, drive_team, stands = finished_dict[time_slot]
        role_map = {
            "Drive Team": drive_team,
            "Pits": pits,
            "Scouting": scouting,
            "Stands": stands,
        }
        for row, role in enumerate(roles, start=1):
            names = ", ".join(role_map[role]) if role_map[role] else "None"
            tk.Label(grid_window, text=names, borderwidth=1, relief="solid",
                     padx=5, pady=5, wraplength=150, justify="left").grid(row=row, column=col, sticky="nsew")

    # Stretchable cells
    for col in range(len(time_slots) + 1):
        grid_window.grid_columnconfigure(col, weight=1)
    for row in range(len(roles) + 1):
        grid_window.grid_rowconfigure(row, weight=1)

# -----------------------------
# Run
# -----------------------------
process_csv()
schedule_teammates()
show_schedule()
