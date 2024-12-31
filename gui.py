import tkinter as tk
from tkinter import messagebox
from classes import SpaceCraft, Rocket, Shuttle, Astronaut, Mission

class SpaceMissionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Mission Management")
        self.root.geometry("900x600")
        self.root.configure(bg="black")
        
        # Variables
        self.spacecrafts = []
        self.astronauts = []
        self.missions = []
        self.spacecraft_type = tk.StringVar(value="Rocket")
        self.spacecraft_name = tk.StringVar()
        self.capacity = tk.IntVar()
        self.astronaut_name = tk.StringVar()
        self.astronaut_rank = tk.StringVar()
        self.astronaut_experience = tk.IntVar()
        self.astronaut_weight = tk.IntVar()
        self.mission_name = tk.StringVar()
        self.selected_spacecraft = tk.StringVar()
        self.selected_mission = tk.StringVar()
        self.selected_astronaut = tk.StringVar()
        self.refuel_amount = tk.IntVar()
        self.payload_weight = tk.IntVar()
        
        self.create_main_screen()

    def create_main_screen(self):
        # Tabs
        self.create_button("Add Spacecraft", self.add_spacecraft_screen, 0, 0)
        self.create_button("Add Astronaut", self.add_astronaut_screen, 0, 1)
        self.create_button("Create Mission", self.create_mission_screen, 0, 2)
        self.create_button("Refuel Spacecraft", self.refuel_spacecraft_screen, 0, 3)
        self.create_button("Add Payload", self.add_payload_screen, 0, 4)
        self.create_button("Launch Mission", self.launch_mission_screen, 0, 5)
        
   

    def create_button(self, text, command, row, column):
        button = tk.Button(self.root, text=text, command=command, bg="white", fg="black", font=("Arial", 12, "bold"))
        button.grid(row=row, column=column, padx=10, pady=10)

    def create_label(self, text, row, column):
        label = tk.Label(self.root, text=text, bg="black", fg="white", font=("Arial", 12))
        label.grid(row=row, column=column, sticky="w")

    def create_entry(self, textvariable, row, column, columnspan=1):
        entry = tk.Entry(self.root, textvariable=textvariable, bg="white", fg="black", font=("Arial", 12))
        entry.grid(row=row, column=column, columnspan=columnspan)

    def create_option_menu(self, variable, options, row, column, columnspan=1):
        option_menu = tk.OptionMenu(self.root, variable, *options)
        option_menu.config(bg="white", fg="black", font=("Arial", 12))
        option_menu.grid(row=row, column=column, columnspan=columnspan)

    def add_spacecraft_screen(self):
        self.clear_screen()
        self.create_label("Spacecraft Type:", 2, 0)
        tk.Radiobutton(self.root, text="Rocket", variable=self.spacecraft_type, value="Rocket", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=1)
        tk.Radiobutton(self.root, text="Shuttle", variable=self.spacecraft_type, value="Shuttle", bg="black", fg="white", font=("Arial", 12)).grid(row=2, column=2)
        self.create_label("Spacecraft Name:", 3, 0)
        self.create_entry(self.spacecraft_name, 3, 1, 2)
        self.create_label("Capacity:", 4, 0)
        self.create_entry(self.capacity, 4, 1, 2)
        self.create_button("Create Spacecraft", self.create_spacecraft, 5, 0)

    def add_astronaut_screen(self):
        self.clear_screen()
        self.create_label("Astronaut Name:", 1, 0)
        self.create_entry(self.astronaut_name, 1, 1, 2)
        self.create_label("Rank:", 2, 0)
        self.create_entry(self.astronaut_rank, 2, 1, 2)
        self.create_label("Experience (Years):", 3, 0)
        self.create_entry(self.astronaut_experience, 3, 1, 2)
        self.create_label("Weight (kg):", 4, 0)
        self.create_entry(self.astronaut_weight, 4, 1, 2)
        self.create_button("Add Astronaut", self.add_astronaut, 5, 0)

    def create_mission_screen(self):
        self.clear_screen()
        self.create_label("Mission Name:", 1, 0)
        self.create_entry(self.mission_name, 1, 1, 2)
        self.create_label("Select Spacecraft:", 2, 0)
        spacecraft_names = [sc.name for sc in self.spacecrafts]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 2, 1, 2)
        self.create_button("Create Mission", self.create_mission, 3, 0)

    def launch_mission_screen(self):
        self.clear_screen()
        self.create_label("Available Missions:", 1, 0)
        mission_names = [mission.mission_name for mission in self.missions]
        self.selected_mission.set(mission_names[0] if mission_names else "")
        self.create_option_menu(self.selected_mission, mission_names, 1, 1, 2)
        self.create_button("Launch Mission", self.launch_mission, 7, 0)
        self.create_label("Select Astronaut:", 4, 0)
        astronaut_names = [astronaut.name for astronaut in self.astronauts]
        self.selected_astronaut.set(astronaut_names[0] if astronaut_names else "")
        self.create_option_menu(self.selected_astronaut, astronaut_names, 4, 1, 2)
        self.create_button("Add Astronaut to Mission", self.add_astronaut_to_mission, 6, 0)

    def refuel_spacecraft_screen(self):
        self.clear_screen()
        self.create_label("Select Spacecraft:", 1, 0)
        spacecraft_names = [sc.name for sc in self.spacecrafts]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 1, 1, 2)
        self.create_label("Refuel Amount:", 2, 0)
        self.create_entry(self.refuel_amount, 2, 1, 2)
        self.create_button("Refuel Spacecraft", self.refuel_spacecraft, 3, 0)

    def add_payload_screen(self):
        self.clear_screen()
        self.create_label("Select Spacecraft:", 1, 0)
        spacecraft_names = [sc.name for sc in self.spacecrafts]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 1, 1, 2)
        self.create_label("Payload Weight (tons):", 2, 0)
        self.create_entry(self.payload_weight, 2, 1, 2)
        self.create_button("Add Payload", self.add_payload, 3, 0)

    def create_spacecraft(self):
        name = self.spacecraft_name.get()
        capacity = self.capacity.get()
        try:
            if self.spacecraft_type.get() == "Rocket":
                spacecraft = Rocket(name, capacity)
            elif self.spacecraft_type.get() == "Shuttle":
                spacecraft = Shuttle(name, capacity)
            else:
                raise Exception("Invalid Spacecraft Type")
            self.spacecrafts.append(spacecraft)
            messagebox.showinfo("Success", f"{name} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_astronaut(self):
        try:
            astronaut = Astronaut(
                self.astronaut_name.get(),
                self.astronaut_rank.get(),
                self.astronaut_experience.get(),
                self.astronaut_weight.get()
            )
            self.astronauts.append(astronaut)
            messagebox.showinfo("Success", f"Astronaut {astronaut.name} added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_mission(self):
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            mission = Mission(self.mission_name.get(), spacecraft, [])
            self.missions.append(mission)
            messagebox.showinfo("Success", f"Mission {mission.mission_name} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def launch_mission(self):
        try:
            mission_name = self.selected_mission.get()
            mission = next(m for m in self.missions if m.mission_name == mission_name)
            if mission.spaceCraft.current_fuel >= 80:  
                mission.launch()
                messagebox.showinfo("Success", f"Mission {mission.mission_name} launched with {len(mission.crew)} crew members!")
            else:
                messagebox.showerror("Error", "Insufficient fuel for launch")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_astronaut_to_mission(self):
        try:
            mission_name = self.selected_mission.get()
            astronaut_name = self.selected_astronaut.get()
            mission = next(m for m in self.missions if m.mission_name == mission_name)
            astronaut = next(a for a in self.astronauts if a.name == astronaut_name)
            result = mission.add_crew(astronaut)
            if result == "Crew added successfully":
                messagebox.showinfo("Success", f"Astronaut {astronaut.name} added to mission {mission.mission_name}!")
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refuel_spacecraft(self):
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            amount = int(self.refuel_amount.get())
            spacecraft.refuel(amount)
            messagebox.showinfo("Success", f"{spacecraft.name} refueled successfully! Current fuel: {spacecraft.current_fuel}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_payload(self):
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            weight = self.payload_weight.get()
            if isinstance(spacecraft, Rocket):
                spacecraft.add_payload(weight)
                messagebox.showinfo("Success", f"Payload added successfully to {spacecraft.name}!")
            else:
                messagebox.showerror("Error", "Payload can only be added to Rockets")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()
            widget.destroy()
        self.create_main_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceMissionApp(root)
    root.mainloop()
