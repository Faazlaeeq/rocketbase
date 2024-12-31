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
    def __init__(self, mission_name, spaceCraft, crew=None):
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
