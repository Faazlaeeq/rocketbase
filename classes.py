import mysql.connector

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
        try:
            self.cursor.execute(query, params)
            if query.strip().lower().startswith(("insert", "update", "delete")):
                self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
db=Database()

class SpaceCraft:
    def __init__(self, name, type, capacity,current_fuel=80,isNew=True):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.current_fuel = current_fuel # Ensure current_fuel is properly initialized
        if isNew:
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
    def __init__(self, name, payload_cap, currentfuel=80,isNew=True):
        super().__init__(name, "Rocket", payload_cap,current_fuel=currentfuel,isNew=isNew)
        self.payload=0
    def add_payload(self, weight_in_tons):
        print(f"payload {self.payload}")
        if weight_in_tons <= self.capacity - self.payload:
            self.payload += weight_in_tons
            return "Weight Added"
        else:
            raise Exception(f"Payload weight limit exceeded, current capacity: {self.capacity-self.payload} tons")

# class Shuttle(SpaceCraft):
#     def __init__(self, name, passenger_cap):
#         super().__init__(name, "Shuttle", passenger_cap)

#     def board_passenger(self, number):
#         if number <= self.capacity:
#             return f"{number} Passengers added on board"
#         else:
#             raise Exception("Passenger on board limit exceeded")

class Astronaut:
    def __init__(self, name, rank, experience_years, weight,isNew=True):
        self.name = name
        self.rank = rank
        self.experience_years = experience_years
        self.weight = weight
        if isNew:
            db.execute("INSERT INTO Astronaut (name, _rank, experience_years, weight) VALUES (%s, %s, %s, %s)",
                   (self.name, self.rank, self.experience_years, self.weight))

    def assign_to_mission(self, mission):
        self.mission = mission

    def display_details(self):
        return f"Name: {self.name}\nRank: {self.rank}\nExperience: {self.experience_years}\nCurrent Mission: {self.mission}"

class Mission:
    def __init__(self, mission_name, spaceCraft, crew=None,isNew=True):
        self.mission_name = mission_name
        self.spaceCraft = spaceCraft
        self.crew = crew if crew is not None else []
        self.status = "Pending"
        if isNew:
            db.execute("INSERT INTO Mission (mission_name, spacecraft_id, status) VALUES (%s, %s, %s)",
                   (self.mission_name, self.spaceCraft.id, self.status))
        

    def add_crew(self, astronaut):
        if isinstance(self.spaceCraft, Rocket):
            try:
                self.spaceCraft.add_payload(astronaut.weight / 1000)
                self.crew.append(astronaut)
            except Exception as e:
                return str(e)
        # elif isinstance(self.spaceCraft, Shuttle):
        #     try:
        #         self.spaceCraft.board_passenger(len(self.crew) + 1)
        #         self.crew.append(astronaut)
        #     except Exception as e:
        #         return str(e)
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

class DbServer:
    def __init__(self):
        self.db = Database()
    def fetch_spacecrafts(self):
        try:
            self.db.execute("SELECT * FROM SpaceCraft")
            results = self.db.fetchall()
            if results:
                return results
            else:
                return "No spacecrafts found."
        except Exception as e:
            return str(e)
    def fetch_rockets(self):
        try:
            self.db.execute("SELECT * FROM SpaceCraft where type='Rocket'")
            results = self.db.fetchall()
            if results:
                return results
            else:
                return "No spacecrafts found."
        except Exception as e:
            return str(e)
    def fetch_shuttles(self):
        try:
            self.db.execute("SELECT * FROM SpaceCraft where type='Shuttle'")
            results = self.db.fetchall()
            if results:
                return results
            else:
                return "No spacecrafts found."
        except Exception as e:
            return str(e)

    def fetch_astronauts(self):
        self.db.execute("SELECT * FROM Astronaut")
        return self.db.fetchall()

    def fetch_missions(self):
        missions=[]
        self.db.execute("SELECT * FROM Mission")
        data=self.db.fetchall()
        # for i in data:
        #     missions.append(Mission(i[1],i[2],i[3]))
        return data
    def fetch_mission_objects(self) -> list:
        print("workign on fetch mission objects")
        missions = []
        self.db.execute("SELECT * FROM Mission")
        data = self.db.fetchall()
        print(f"missions {data}")
        for mission_data in data:
            self.db.execute("SELECT * FROM SpaceCraft WHERE id=%s", (mission_data[2],))
            spacecraft_data = self.db.fetchone()
            print(f"spacecraft {spacecraft_data}")
            spacecraft = Rocket(spacecraft_data[1], spacecraft_data[3],spacecraft_data[4],isNew=False)  # Adjust indices as per your DB schema

           

            # Create Mission object
            mission = Mission(mission_data[1], spacecraft,isNew=False)
            missions.append(mission)
        return missions
    def fetch_astronaut_objects(self) -> list:
        print("workign on fetch astronaut objects")
        astronauts = []
        self.db.execute("SELECT * FROM Astronaut")
        data = self.db.fetchall()
        for astronaut_data in data:
            astronaut = Astronaut(astronaut_data[1], astronaut_data[2], astronaut_data[3], astronaut_data[4],isNew=False)
            astronauts.append(astronaut)
        return astronauts
    
    def fetch_spacecraft_objects(self) -> list:
        print("workign on fetch spacecraft objects")
        spacecrafts = []
        self.db.execute("SELECT * FROM SpaceCraft")
        data = self.db.fetchall()
        for spacecraft_data in data:
            spacecraft = Rocket(spacecraft_data[1], spacecraft_data[3], spacecraft_data[4],isNew=False)
            spacecrafts.append(spacecraft)
        return spacecrafts
    
    def checkifExists(self,table,column,value):
        self.db.execute(f"SELECT * FROM {table} WHERE {column}=%s",(value,))
        data=self.db.fetchall()
        if data:
            return True
        else:
            return False
