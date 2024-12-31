import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="faaz123",
            database="Space"
        )
        self.cursor = self.conn.cursor(buffered=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()
        while self.cursor.nextset():
                pass
    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    
db = Database()

class SpaceCraft:
    def __init__(self, name, type, capacity):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.current_fuel = 80  # Ensure current_fuel is properly initialized
        db.execute("INSERT INTO SpaceCraft (name, type, capacity, current_fuel) VALUES (%s, %s, %s, %s)",
                   (self.name, self.type, self.capacity, self.current_fuel))
        db.cursor.execute("SELECT id, current_fuel FROM SpaceCraft WHERE name = %s", (self.name,))
        result = db.fetchone()
        self.id = result[0]
        self.current_fuel = result[1]

    def refuel(self, amount):
        if amount <= 100 - self.current_fuel:
            self.current_fuel += amount
            db.execute("UPDATE SpaceCraft SET current_fuel = %s WHERE name = %s", (self.current_fuel, self.name))
        else:
            raise Exception("Invalid fuel amount")

    def launch(self):
        if self.current_fuel >= 80:
            return f"{self.name} SpaceCraft launched successfully"
        else:
            raise Exception("Insufficient Fuel")

class Rocket(SpaceCraft):
    def __init__(self, name, payload_cap):
        super().__init__(name, "Rocket", payload_cap)

    def add_payload(self, weight_in_tons):
        if weight_in_tons <= self.capacity:
            return "Weight Added"
        else:
            raise Exception("Payload weight limit exceeded")

class Shuttle(SpaceCraft):
    def __init__(self, name, passenger_cap):
        super().__init__(name, "Shuttle", passenger_cap)

    def board_passenger(self, number):
        if number <= self.capacity:
            return f"{number} Passengers added on board"
        else:
            raise Exception("Passenger on board limit exceeded")

class Astronaut:
    def __init__(self, name, rank, experience_years, weight):
        self.name = name
        self.rank = rank
        self.experience_years = experience_years
        self.weight = weight
        db.execute("INSERT INTO Astronaut (name, _rank, experience_years, weight) VALUES (%s, %s, %s, %s)",
                   (self.name, self.rank, self.experience_years, self.weight))

    def assign_to_mission(self, mission):
        self.mission = mission

    def display_details(self):
        return f"Name: {self.name}\nRank: {self.rank}\nExperience: {self.experience_years}\nCurrent Mission: {self.mission}"

class Mission:
    def __init__(self, mission_name, spaceCraft, crew = None):
        self.mission_name = mission_name
        self.spaceCraft = spaceCraft
        self.crew = crew if crew is not None else []
        self.status = "Pending"
        db.execute("INSERT INTO Mission (mission_name, spacecraft_id, status) VALUES (%s, %s, %s)",
                   (self.mission_name, self.spaceCraft.id, self.status))

    def add_crew(self, astronaut):
        if isinstance(self.spaceCraft, Rocket):
            try:
                self.spaceCraft.add_payload(astronaut.weight / 1000)
                self.crew.append(astronaut)
            except Exception as e:
                return str(e)
        elif isinstance(self.spaceCraft, Shuttle):
            try:
                self.spaceCraft.board_passenger(len(self.crew) + 1)
                self.crew.append(astronaut)
            except Exception as e:
                return str(e)
        else:
            raise Exception("Unexpected input")
        return "Crew added successfully"
    def launch(self):
        if self.spaceCraft.current_fuel >= 80:
            self.spaceCraft.launch()
            self.status = "Launched"
            db.execute("UPDATE Mission SET status = %s WHERE mission_name = %s", (self.status, self.mission_name))
        else:
            raise Exception("Insufficient fuel for launch")

# smallRocket = Rocket("Small Rocket", 20)
# largeRocket = Rocket("Large Rocket", 80)

# smallShuttle = Shuttle("Small Shuttle", 2)
# largeShuttle = Shuttle("Large Shuttle", 15)

# as01 = Astronaut("John", "Worker", 2, 70)
# as02 = Astronaut("Alice", "Commander", 10, 75)
# as03 = Astronaut("Bob", "Engineer", 5, 80)
# as04 = Astronaut("Charlie", "Scientist", 7, 85)
# as05 = Astronaut("Diana", "Pilot", 3, 90)

# mission01 = Mission("Mars Mission", smallRocket, [as01, as02, as03])

# print("Test refueling:")
# smallRocket.refuel(10)
# print(smallRocket.current_fuel)  # Expected: 90

# print("\nTest exceeding capacity:")
# try:
#     smallRocket.refuel(50)
# except Exception as e:
#     print(e)  # Expected: "Invalid fuel amount"

# print("\nTest launch:")
# try:
#     print(smallRocket.launch())
# except Exception as e:
#     print(e)  # Expected: "Small Rocket SpaceCraft launched successfully"

# print("\nTesting launch with insufficient fuel:")
# smallRocket.current_fuel = 50
# try:
#     print(smallRocket.launch())
# except Exception as e:
#     print(e)  # Expected: "Insufficient Fuel"

# print("\nTesting add payload:")
# try:
#     print(smallRocket.add_payload(10))
# except Exception as e:
#     print(e)  # Expected: "Weight Added"

# print("\nTesting add payload exceeding limit:")
# try:
#     print(smallRocket.add_payload(30))
# except Exception as e:
#     print(e)  # Expected: "Payload weight limit exceeded"

# print("\nTesting add passenger:")
# try:
#     print(smallShuttle.board_passenger(5))
# except Exception as e:
#     print(e)  # Expected: "5 Passengers added on board"

# print("\nTesting add passenger exceeding limit:")
# try:
#     print(smallShuttle.board_passenger(15))
# except Exception as e:
#     print(e)  # Expected: "Passenger on board limit exceeded"

# print("\nAssign astronaut to mission and display details:")
# as01.assign_to_mission("Mars Mission")
# print(as01.display_details())
# # Expected:
# # Name: John
# # Rank: Worker
# # Experience: 2
# # Current Mission: Mars Mission

# print("\nAdd crew to mission:")
# print(mission01.add_crew(as05))
# # Expected: "Crew added successfully"

# print("\nAdd crew exceeding payload limit:")
# as06 = Astronaut("Eve", "Engineer", 6, 30000)
# print(mission01.add_crew(as06))
# # Expected: "Payload weight limit exceeded"

# print("\nAdd crew to shuttle mission:")
# mission02 = Mission("Lunar Mission", smallShuttle, [])
# print(mission02.add_crew(as02))
# # Expected: "2 Passengers added on board"

# print("\nAdd crew exceeding passenger limit:")
# try:
#     print(mission02.add_crew(as03))
#     print(mission02.add_crew(as01))
#     print(mission02.add_crew(as05))
# except Exception as e:
#     print(e)  # Expected: "Passenger on board limit exceeded"
