import tkinter as tk
from tkinter import ttk, messagebox
from classes import *

class SpaceMissionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Mission Management")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")  # Light background color
        
        # Create a style
        self.style = ttk.Style()
        self.style.configure("TButton", foreground="black", padding=(10, 1), font=("Segoe UI", 12))
        self.style.map("TButton", background=[("active", "#d9d9d9"), ("!disabled", "#f0f0f0")])        
        self.style.configure("TLabel", background="#f0f0f0", foreground="black", font=("Segoe UI", 12))
        self.style.configure("TEntry", font=("Segoe UI", 16))
        self.style.configure("TRadiobutton", background="#f0f0f0", foreground="black", font=("Segoe UI", 12))
        self.style.configure("Custom.TMenubutton", background="#ffffff", foreground="black", font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.style.map("Custom.TMenubutton", 
                       fieldbackground=[('!active', '#ffffff'), ('active', '#d9d9d9')],
                       bordercolor=[('!active', '#000000'), ('active', '#ff0000')])
        
        # Variables
        self.spacecrafts = DbServer().fetch_spacecraft_objects()
        self.astronauts = DbServer().fetch_astronaut_objects()
        self.missions = DbServer().fetch_mission_objects()
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
        
        # Create frames
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        self.separator = ttk.Separator(self.root, orient="vertical")
        self.separator.grid(row=0, column=1, sticky="ns")
        
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=3)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_main_screen()

    def create_main_screen(self):
        self.log_text = tk.Text(self.input_frame, height=100, wrap="word", state="disabled")
        self.log_text.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

        # Tabs
        self.create_button("Add Spacecraft", self.add_spacecraft_screen, 0)
        self.create_button("Add Astronaut", self.add_astronaut_screen, 1)
        self.create_button("Create Mission", self.create_mission_screen, 2)
        self.create_button("Refuel Spacecraft", self.refuel_spacecraft_screen, 3)
        # self.create_button("Add Payload", self.add_payload_screen, 4)
        # self.create_button("Add Passenger", self.add_passenger_screen, 5)
        self.create_button("Launch Mission", self.launch_mission_screen, 6)
        self.create_button("View Data", self.view_data_screen, 7)
       


    def view_data_screen(self):
        self.clear_screen()
        self.create_label("Select Table:", 1, 0)
        tables = ["Astronauts", "Missions", "Spacecrafts"]
        self.selected_table = tk.StringVar(value=tables[0])
        self.create_option_menu(self.selected_table, tables, 1, 1, 2)
        self.create_button("View Data", self.view_data, 2, self.input_frame)

    def view_data(self):
        table = self.selected_table.get()
        db = DbServer()
        if table == "Astronauts":
            data = db.fetch_astronauts()
            headers = ["Id","Name", "Rank", "Experience", "Weight"]
        elif table == "Missions":
            data = db.fetch_missions()
            headers = ['Id' "Mission Name", "Spacecraft", "Crew","Status"]
        elif table == "Spacecrafts":
            data = db.fetch_spacecrafts()
            headers = ["ID", "Name", "Type", "Capacity", "Current Fuel"]
        else:
            data = []
            headers = []

        if hasattr(self, 'data_tree'):
            self.data_tree.destroy()

        self.data_tree = ttk.Treeview(self.input_frame, columns=headers, show="headings", height=20)
        for header in headers:
            self.data_tree.heading(header, text=header)
            self.data_tree.column(header, width=150)
        for row in data:
            self.data_tree.insert("", "end", values=row)
        self.data_tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    def create_button(self, text, command, row,frame=None):
        if frame:
            button = ttk.Button(frame, text=text, command=command, style="TButton")
        else:
            button = ttk.Button(self.button_frame, text=text, command=command, style="TButton")
        button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")

    def create_label(self, text, row, column):
        label = ttk.Label(self.input_frame, text=text, style="TLabel")
        label.grid(row=row, column=column, sticky="w", padx=10, pady=5)

    def create_entry(self, textvariable, row, column, columnspan=1):
        entry = ttk.Entry(self.input_frame, textvariable=textvariable, style="TEntry",font=("Segoe UI", 14))
        entry.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky="ew")

    def create_option_menu(self, variable, options, row, column, columnspan=1):
        if options:  # Ensure options list is not empty
            variable.set(options[0])  # Set the first option as the default value
        else:
            variable.set("")  # Set to an empty string if no options available

        option_menu = ttk.OptionMenu(self.input_frame, variable, variable.get(), *options, style="Custom.TMenubutton")
        option_menu.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky="ew")

    def add_spacecraft_screen(self):
        self.clear_screen()
        self.create_label("Spacecraft Name:", 3, 0)
        self.create_entry(self.spacecraft_name, 3, 1, 2)
        self.create_label("Payload Capacity(tons):", 4, 0)
        self.create_entry(self.capacity, 4, 1, 2)
        self.create_button("Create Spacecraft", self.create_spacecraft, 5,self.input_frame)
        
    def add_astronaut_screen(self):
        self.clear_screen()
        self.create_label("Astronaut Name:", 1, 0)
        self.create_entry(self.astronaut_name, 1, 1, 2)
        self.create_label("Rank:", 2, 0)
        self.create_entry(self.astronaut_rank, 2, 1, 2)
        self.create_label("Experience (Years):", 3, 0)
        self.create_entry(self.astronaut_experience, 3, 1, 2)
        self.create_label("Weight (kg):", 4, 0)
        self.create_label("Weight (kg):", 4, 0)
        self.create_entry(self.astronaut_weight, 4, 1, 2)
        self.create_button("Add Astronaut", self.add_astronaut, 5,self.input_frame)

    def create_mission_screen(self):
        self.clear_screen()
        self.create_label("Mission Name:", 1, 0)
        self.create_entry(self.mission_name, 1, 1, 2)
        self.create_label("Select Spacecraft:", 2, 0)
        spacecraft_names = [row[1] for row in DbServer().fetch_spacecrafts()]

        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 2, 1, 2)
        self.create_button("Create Mission", self.create_mission, 3,self.input_frame)

    def launch_mission_screen(self):
        self.clear_screen()
        self.create_label("Available Missions:", 1, 0)
        self.missions = DbServer().fetch_mission_objects()
        mission_names = [row[1] for row in DbServer().fetch_missions()]
        self.selected_mission.set(mission_names[0] if mission_names else "")
        self.create_option_menu(self.selected_mission, mission_names, 1, 1, 2)
        self.create_label("Select Astronaut:", 4, 0)
        astronaut_names = [row[1] for row in DbServer().fetch_astronauts()]
        self.selected_astronaut.set(astronaut_names[0] if astronaut_names else "")
        self.create_option_menu(self.selected_astronaut, astronaut_names, 4, 1, 2)
        
        self.create_button("Add Astronaut to Mission", self.add_astronaut_to_mission, 6, self.input_frame)
        
        
        self.create_label("Payload Weight (tons) (enter negative to remove):", 2, 0)
        self.create_entry(self.payload_weight, 2, 1, 2)
        self.create_button("Add Payload", self.add_payload, 3,self.input_frame)

        self.create_button("Launch Mission", self.launch_mission, 7,self.input_frame)

    def refuel_spacecraft_screen(self):
        self.clear_screen()
        self.create_label("Select Spacecraft:", 1, 0)
        spacecraft_names = [row[1] for row in DbServer().fetch_rockets()]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 1, 1, 2)
        self.create_label("Refuel Amount:", 2, 0)
        self.create_entry(self.refuel_amount, 2, 1, 2)
        self.create_button("Refuel Spacecraft", self.refuel_spacecraft, 3,self.input_frame)

    def add_passenger_screen(self):
        self.clear_screen()
        self.create_label("Select Shuttle:", 1, 0)
        spacecraft_names = [row[1] for row in DbServer().fetch_shuttles()]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 1, 1, 2)
        self.create_label("Passengers:", 2, 0)
        astronouts = [row[1] for row in DbServer().fetch_astronauts()]
        self.selected_astronaut.set(astronouts[0] if astronouts else "")
        self.create_option_menu(self.selected_astronaut, astronouts, 2, 1, 2)
        self.create_button("Add Passenger", self.add_payload, 3,self.input_frame)
    def add_payload_screen(self):
        self.clear_screen()
        self.create_label("Select Rocket:", 1, 0)
        spacecraft_names = [row[1] for row in DbServer().fetch_spacecrafts()]
        self.selected_spacecraft.set(spacecraft_names[0] if spacecraft_names else "")
        self.create_option_menu(self.selected_spacecraft, spacecraft_names, 1, 1, 2)
        self.create_label("Payload Weight (tons):", 2, 0)
        self.create_entry(self.payload_weight, 2, 1, 2)
        self.create_button("Add Payload", self.add_payload, 3,self.input_frame)

    def create_spacecraft(self):
        name = self.spacecraft_name.get()
        capacity = self.capacity.get()
        if DbServer().checkifExists('SpaceCraft','name',name):
            messagebox.showerror("Error", "Spacecraft already exists")
            self.add_log("Spacecraft already exists")
            return
        if capacity <= 0:
            messagebox.showerror("Error", "Capacity should be greater than 0")
            self.add_log("Capacity should be greater than 0")
            return
        try:
            spacecraft = Rocket(name, capacity)

            
            self.spacecrafts.append(spacecraft)
            messagebox.showinfo("Success", f"{name} created successfully!")
            self.add_log(f"{name} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_astronaut(self):
        if DbServer().checkifExists('Astronaut','name',self.astronaut_name.get()):
            messagebox.showerror("Error", "Astronaut already exists")
            return
        try:
            astronaut = Astronaut(
                self.astronaut_name.get(),
                self.astronaut_rank.get(),
                self.astronaut_experience.get(),
                self.astronaut_weight.get()
            )
            self.astronauts.append(astronaut)
            messagebox.showinfo("Success", f"Astronaut {astronaut.name} added successfully!")
            self.add_log(f"Astronaut {astronaut.name} added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(str(e))

    def create_mission(self):
        if DbServer().checkifExists('Mission','mission_name',self.mission_name.get()):
            messagebox.showerror("Error", "Mission already exists")
            return
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            mission = Mission(self.mission_name.get(), spacecraft, [])
            
            self.missions.append(mission)
            messagebox.showinfo("Success", f"Mission {mission.mission_name} created successfully!")
            self.add_log(f"Mission {mission.mission_name} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(str(e))

    def launch_mission(self):
        try:
            mission_name = self.selected_mission.get()
            mission = next(m for m in self.missions if m.mission_name == mission_name)
            if mission.spaceCraft.current_fuel >= 80:  
                mission.launch()
                messagebox.showinfo("Success", f"Mission {mission.mission_name} launched with {len(mission.crew)} crew members and {mission.spaceCraft.payload} tons of payload!")
                self.add_log(f"Mission {mission.mission_name} launched with {len(mission.crew)} crew members and {mission.spaceCraft.payload} tons of payload!")
            else:
                messagebox.showerror("Error", "Insufficient fuel for launch")
                self.add_log("Insufficient fuel for launch")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(str(e))

    def add_astronaut_to_mission(self):
        try:
            mission_name = self.selected_mission.get()
            astronaut_name = self.selected_astronaut.get()
            print(f"astronaut_name: {astronaut_name}")
            mission = next(m for m in self.missions if m.mission_name == mission_name)
            print(f"mission: {mission}")
            astronaut = next(a for a in self.astronauts if a.name == astronaut_name)
          
            result = mission.add_crew(astronaut)
            if result == "Crew added successfully":
                messagebox.showinfo("Success", f"Astronaut {astronaut.name} added to mission {mission.mission_name}!")
                self.add_log(f"Astronaut {astronaut.name} added to mission {mission.mission_name}!")
            else:
                messagebox.showerror("Error", result)
                self.add_log(result)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(f"Something went wrong {e}")

    def refuel_spacecraft(self):
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            amount = int(self.refuel_amount.get())
            spacecraft.refuel(amount)
            messagebox.showinfo("Success", f"{spacecraft.name} refueled successfully! Current fuel: {spacecraft.current_fuel}")
            self.add_log(f"{spacecraft.name} refueled successfully! Current fuel: {spacecraft.current_fuel}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(str(e))

    def add_passenger(self):
        try:
            spacecraft_name = self.selected_spacecraft.get()
            spacecraft = next(sc for sc in self.spacecrafts if sc.name == spacecraft_name)
            astronaut_name = self.selected_astronaut.get()
            astronaut = next(a for a in self.astronauts if a.name == astronaut_name)
            if isinstance(spacecraft, Shuttle):
                spacecraft.board_passenger(astronaut)
                messagebox.showinfo("Success", f"{astronaut.name} added to {spacecraft.name}!")
            else:
                messagebox.showerror("Error", "Passengers can only be added to Shuttles")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_payload(self):
        weight = self.payload_weight.get()
       
        try:
            spacecraft = next(m for m in self.missions if m.mission_name == self.selected_mission.get()).spaceCraft
            print(f"spacecraft: {spacecraft}")
            
            spacecraft.add_payload(weight)
            messagebox.showinfo("Success", f"Payload added successfully to {spacecraft.name}!")
            self.add_log(f"{weight} tons Payload added successfully to {spacecraft.name}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.add_log(str(e))

    def clear_screen(self):
        for widget in self.input_frame.winfo_children():
            if  isinstance(widget, tk.Text)==False:
                widget.grid_forget()
                widget.destroy()
    def add_log(self, log):
        self.log_text.config(state="normal")
        self.log_text.insert("1.0", f"{log}\n") 
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceMissionApp(root)
    root.mainloop()
