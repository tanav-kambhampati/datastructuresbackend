import csv3

with open("rocket_launch_data.csv", mode = "w") as csvfile:
    fieldnames = ['payload_mass', 'origin_country', 'company', 'engine_strength', 'success_rate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"payload_mass": "50", "origin_country": "USA", "company": "NASA", "engine_strength": "37", "success_rate": "Success"})
    writer.writerow({"payload_mass": "20", "origin_country": "USA", "company": "NASA", "engine_strength": "45", "success_rate": "Success"})
    writer.writerow({"payload_mass": "74", "origin_country": "Taiwan", "company": "Firefly", "engine_strength": "56", "success_rate": "Failure"})
    writer.writerow({"payload_mass": "23", "origin_country": "India", "company": "ISRO", "engine_strength": "32", "success_rate": "Failure"})
    writer.writerow({"payload_mass": "438", "origin_country": "USA", "company": "SpaceX", "engine_strength": "41", "success_rate": "Failure"})
    writer.writerow({"payload_mass": "2309", "origin_country": "USA", "company": "SpaceX", "engine_strength": "49", "success_rate": "Success"})
    writer.writerow({"payload_mass": "24", "origin_country": "USA", "company": "SpaceX", "engine_strength": "33","success_rate": "Failure"})
    writer.writerow({"payload_mass": "2", "origin_country": "India", "company": "ISRO", "engine_strength": "42","success_rate": "Success"})
   