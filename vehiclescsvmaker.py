import csv

with open("carsalarydata.csv", mode = "w") as csvfile:
    fieldnames = ['Salary', 'Car', 'Affordability']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"Salary": "500000", "Car": "Phantom", "Affordability": "True"})
    writer.writerow({"Salary": "200000", "Car": "Continental", "Affordability": "False"})
    writer.writerow({"Salary": "740000", "Car": "720s", "Affordability": "True"})
    writer.writerow({"Salary": "230000", "Car": "Roadster", "Affordability": "True"})
    writer.writerow({"Salary": "438000", "Car": "Quattroporte", "Affordability": "True"})
    writer.writerow({"Salary": "139000", "Car": "Chiron", "Affordability": "False"})
    writer.writerow({"Salary": "840000", "Car": "A8","Affordability": "True"})
    writer.writerow({"Salary": "180000", "Car": "Huracán", "Affordability": "False"})
   