# TeamMember class
# Properties: Name: string, experience: integer, available timings: list of strings, position: string, amount of times they have been used: integer
class TeamMember: 
  def __init__(self, name, available_timings, position):
    self.name = name
    self.available_timings = available_timings
    self.position = position 
    self.times_used = 0

  def increment_times_used(self):
    self.times_used += 1