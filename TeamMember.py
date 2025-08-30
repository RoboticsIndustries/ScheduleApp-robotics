    # teammember.py
    # TeamMember class
    # Properties: name (string), available_timings (list of strings),
    # position (string), times_used (int), last_task (string)

class TeamMember:
        def __init__(self, name, available_timings, position):
            self.name = name
            # ensure timings are normalized, e.g. "8-9" (no spaces)
            self.available_timings = [t.strip() for t in available_timings]
            # normalize position strings to Title Case for comparisons
            self.position = position.strip().title()
            self.times_used = 0
            # track how many times assigned to pits and scouting separately
            self.pits_count = 0
            self.scouting_count = 0
            # last task assigned (None, "Pits", "Scouting", "Drive Team", "Stands")
            self.last_task = None

        def increment_times_used(self):
            self.times_used += 1

        def assign_pits(self):
            self.pits_count += 1
            self.increment_times_used()
            self.last_task = "Pits"

        def assign_scouting(self):
            self.scouting_count += 1
            self.increment_times_used()
            self.last_task = "Scouting"

        def assign_drive(self):
            self.increment_times_used()
            self.last_task = "Drive Team"

        def assign_stands(self):
            self.increment_times_used()
            self.last_task = "Stands"

        # Returns True if member can do role now (not same role twice in a row except Stands)
        def can_do(self, role):
            role = role.title()
            if role == "Stands":
                return True
            # do not allow same non-stands task twice in a row
            if self.last_task == role:
                return False
            # drive team members should only be Drive Team (you can tweak this)
            if self.position == "Drive Team" and role != "Drive Team":
                return False
            return True
