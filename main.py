from re import split
from TeamMember import TeamMember
import csv
import tkinter as tk
from constants import pits_limit, scouting_limit, drive_limit, member_pits_max, leads_pits_max, scouting_max
# Main factors to consider
# Position - are lead or normal member?
# Timings - When are they available?

# Scheduling algorithm

# For each time slot, you have to return a 2D list. 
# Prerequisite - you have a list of TeamMember objects
# Create a list of all of the time slots
# Use for loops to loop through all the time slots
# Use for loops to get each element of a TeamMember and loop through their list of available timings to see if one matches the current time slot in the main loop 


# team_members = [  
# {"name": "Aryan", "time_slots": ["4-5", "5-6", "8-9"]},
# {"name": "Kush", "time_slots": ["1-2", "2-3", "5-6"]},
# {"name": "Vatsal", "time_slots": ["1-2", "2-3", "3-4"]},
# ]
# current_time_slot == "5-6"
# drive_team = []
# pits = []
# scouting = []
# for member in team_members:
# if current_time_slot in member.time_slots:
# role = member["time_slots"][current_time_slot]
# if role == "drive team":
# drive_team.append(member["name"])
# elif role == "pits":
# pits.append(member["name"])
# elif role == "scouting":
# scouting.append(member["name"])

# result = [drive_team, pits, scouting]

# print(result)


# Final return for the program: for each time slot, return a 2D list with this format [[All of the people in the drive team], [all of the people in pits], [all of the people who are scouting]


# STEP 1: Find all available members for a specific time slot

# available_members = []


# for time_slot in time_slots:
#   for member in team_members:
#     if time_slot in member.available_timings:
#       available_members.append(member)
#   print(f"members available at {time_slot}")
#   for member in available_members:
#     print(f"{member.name} - {member.position}")



# Step 2 (7/9): Assign members to lists of roles based on their position, experience, and times used. Start to program this for homework




# Filter the available members based on their position so that you can populate the drive team list

# Difference between pop and remove: pop goes by index and remove goes by value
# ex. list = [1, 2, 3, 4, 5]
# If you want to remove 3, you can do list.remove(3) or list.pop(2)

  # Factors we need to consider to put people in pits. Goal: prioritize leads when you choose who is in pits. HINT: PUT THEM INTO THE PITS LIST FIRST
  # Position 
    # put them in pits for the first time
    # add it to an increment counter
    # from there, we cannot put the lead into pits for more than 4 times.
  # Experience
  # Times Used (difference in threshold for normal member and lead)

  # Comments on homework
  # You don't just want to put people who are leads into pits. You want to prioritize them. You want to put them into pits first before you put normal members into pits. Also, pits are limited, so you want to make sure that you don't put more than a certain amount of people into pits.

# Homework: populate the return dictionary with the return list for each time slot.
# Reference: https://www.w3schools.com/python/python_dictionaries.asp
team_members = []

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

# This function should read the data from the csv file and distribute it into different TeamMember objects, which are then put into one ultimate list to be used with your program
def process_csv():
    with open('response.csv', mode = 'r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            name = line[1]
            position = line[2]
            available_timings = line[3].split(",") # spliting it based off the comma
            team_members.append(TeamMember(name, available_timings, position)) 
            # creating the team member object from each line


# OBJECTIVE: make a team member object from each line - done
# OBJECTIVE: split the timings into a list of strings - done
# Hint link: https://www.w3schools.com/python/ref_string_split.asp



def schedule_teammates():
    for time_slot in finished_dict.keys():
        available_members = []
        pits = []
        scouting = []
        drive_team = []
        
        for member in team_members:
            if time_slot in member.available_timings:
                available_members.append(member)
    
        for member in available_members:
            if member.position == "Drive Team" and len(drive_team) < drive_limit:
                drive_team.append(member)
                available_members.remove(member)
    
        for member in available_members:
            if member.position == "Lead" and member.times_used < leads_pits_max and len(pits) < pits_limit:
                pits.append(member)
                available_members.remove(member)
                member.increment_times_used()
    
        for member in available_members:
            if member.position == "Member" and member.times_used < member_pits_max and len(pits) < pits_limit:
                pits.append(member)
                member.increment_times_used()
                available_members.remove(member)
    
        for member in available_members:
            if len(scouting) < scouting_limit and member.times_used < scouting_max:
                scouting.append(member)
                member.increment_times_used()

        
        finished_dict[time_slot] = [
            [member.name for member in pits],
            [member.name for member in scouting],
            [member.name for member in drive_team]
        ]


process_csv()
schedule_teammates()

def show_schedule():
    window = tk.Tk()
    window.title("Schedule")

    for key, value in finished_dict.items():
        pits, scouting, drive_team = value
        tk.Label(window, text =f"Time Slot: {key}", font=("Arial", 14, "bold")).pack()
        tk.Label(window, text = f"Pits:{pits}").pack()
        tk.Label(window, text = f"Scouting:{scouting}").pack()
        tk.Label(window, text =f"Drive_team: {drive_team}").pack()

    window.mainloop()
show_schedule()
# tkinter documentation: https://docs.python.org/3/library/tkinter.html