import csv

with open("carsalarydata.csv", mode = "w") as csvfile:
    fieldnames = ['Salary', 'Car', 'Affordability']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"Salary": "500,000", "Car": "Phantom", "Affordability": "True"})
    writer.writerow({"Salary": "200,000", "Car": "Continental", "Affordability": "False"})
    writer.writerow({"Salary": "740,000", "Car": "720s", "Affordability": "True"})
    writer.writerow({"Salary": "230,000", "Car": "Roadster", "Affordability": "True"})
    writer.writerow({"Salary": "438,000", "Car": "Quattroporte", "Affordability": "True"})
    writer.writerow({"Salary": "139,000", "Car": "Chiron", "Affordability": "False"})
    writer.writerow({"Salary": "840,000", "Car": "A8","Affordability": "True"})
    writer.writerow({"Salary": "180,000", "Car": "Huracán", "Affordability": "False"})
   