from __init__ import db

# Define the "Car" model
class Car(db.Model):
    # Define the table name in the database
    __tablename__ = "Car"

    # This defines all of the attributes of a car that we will display
    id = db.Column(db.Integer, primary_key=True)  
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    fuel = db.Column(db.String, nullable=False)
    cylinders = db.Column(db.String, nullable=False)

    # Constructor to initialize a new car object
    def __init__(self, make, model, year, fuel, cylinders):
        self.make = make #initialize make
        self.model = model #initialize model
        self.year = year #initialize year
        self.fuel = fuel #initialize fuel
        self.cylinders = cylinders #initialize cylinders

    def to_dict(self):
        return {"make": self.make, "model": self.model, "year": self.year, "fuel": self.fuel, "cylinders": self.cylinders}
    # Create method to let users add a song to the DB
    def create(self):
        try:
            db.session.add(self)  # add prepares to persist object to table
            db.session.commit()  # SQLAlchemy requires a manual commit to get it working
            return self
        except: 
            db.session.remove() # remove object from table if invalid, if the car doesn't exist, then the car is removed. 
            return None

    # Method to return car details for API response
    def read(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "fuel": self.fuel,
            "cylinders": self.cylinders
        }

def initCars(): #This is the library full of cars and their attributes
    BugattiChiron = Car(make="Bugatti", model="Chiron", year="2021", fuel="Gas", cylinders="16"); db.session.add(BugattiChiron)
    TeslaRoadster = Car(make="Tesla", model="Roadster", year="2024", fuel="Electricity", cylinders="None"); db.session.add(TeslaRoadster)
    RollsRoycePhantom = Car(make="Rolls Royce", model="Phantom", year="2021", fuel="Gas", cylinders="8"); db.session.add(RollsRoycePhantom)
    MercedesBenzGClass = Car(make="Mercedes Benz", model="G Class", year="2022", fuel="Gas", cylinders="10"); db.session.add(MercedesBenzGClass)
    AstonMartinDB11 = Car(make="Aston Martin", model="DB11", year="2023", fuel="Gas", cylinders="14"); db.session.add(AstonMartinDB11)
    Ferrari488GTB = Car(make="Ferrari", model="488GTB", year="2023", fuel="Gas", cylinders="9"); db.session.add(Ferrari488GTB)
    BentleyContinentalGT = Car(make="Bentley", model="Continental GT", year="2023", fuel="Gas", cylinders="10"); db.session.add(BentleyContinentalGT)
    Porsche911Targa = Car(make="Porsche", model="911 Targa", year="2023", fuel="Gas", cylinders="8"); db.session.add(Porsche911Targa)
    McLaren720S = Car(make="McLaren", model="720 S", year="2024", fuel="Gas", cylinders="6"); db.session.add(McLaren720S)
    MaseratiQuattroporte = Car(make="Maserati", model="Quattroporte", year="2021", fuel="CNG", cylinders="None"); db.session.add(MaseratiQuattroporte)
    AudiR8Spyder = Car(make="Audi", model="R8 Spyder", year="2022", fuel="Hydrogen Powered", cylinders="8"); db.session.add(AudiR8Spyder)
    MercedesBenz300SLGullwing = Car(make="Mercedes Benz", model="300 SL Gullwing", year="2021", fuel="Gas", cylinders="6"); db.session.add(MercedesBenz300SLGullwing)
    Ferrari250GTCalifornia = Car(make="Ferrari", model="250 GT California", year="2023", fuel="Gas", cylinders="8"); db.session.add(Ferrari250GTCalifornia)
    BentleyFlyingSpur = Car(make="Bentley", model="Flying Spur", year="2021", fuel="Gas", cylinders="4"); db.session.add(BentleyFlyingSpur)
    AudiA8 = Car(make="Audi", model="A8", year="2022", fuel="Gas", cylinders="8"); db.session.add(AudiA8)
    JaguarFType = Car(make="Jaguar", model="F-Type", year="2020", fuel="Gas", cylinders="10"); db.session.add(JaguarFType)
    LamborghiniHuracan = Car(make="Lamborghini", model="Huracan", year="2024", fuel="Hydrogen Powered", cylinders="12"); db.session.add(LamborghiniHuracan)
    RivianR1S = Car(make="Rivian", model="R1S", year="2023", fuel="Electricity", cylinders="None"); db.session.add(RivianR1S)
    MercedesBenzMaybachSClass = Car(make="Mercedes Benz", model="Maybach S Class", year="2022", fuel="Gas", cylinders="6"); db.session.add(MercedesBenzMaybachSClass)
    BMW7Series = Car(make="BMW", model="7 Series", year="2021", fuel="Hydrogen Powered", cylinders="8"); db.session.add(BMW7Series)
    LincolnContinental = Car(make="Lincoln", model="Continental", year="2020", fuel="Gas", cylinders="4"); db.session.add(LincolnContinental)
    RivianR1T = Car(make="Rivian", model="R1T", year="2022", fuel="Electricity", cylinders="None"); 
    TeslaCybertruck = Car(make="Tesla", model="Cybertruck", year="2023", fuel="Electricity", cylinders="None")
    db.session.add(TeslaCybertruck)
    LamborghiniUrus = Car(make="Lamborghini", model="Urus", year="2023", fuel="Gas", cylinders="8")
    db.session.add(LamborghiniUrus)
    db.session.add(RivianR1T)
    db.session.commit()