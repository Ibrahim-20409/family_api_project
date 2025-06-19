import csv
import os

os.makedirs("data", exist_ok=True)

# Family table
family_data = [
    {"Fid": 1, "Fname": "Ali", "Faddress": "Karachi"},
    {"Fid": 2, "Fname": "Ahmed", "Faddress": "Lahore"},
    {"Fid": 3, "Fname": "Sara", "Faddress": "Islamabad"},
    {"Fid": 4, "Fname": "Umar", "Faddress": "Rawalpindi"},
    {"Fid": 5, "Fname": "Zeeshan", "Faddress": "Quetta"},
    {"Fid": 6, "Fname": "Hina", "Faddress": "Peshawar"},
    {"Fid": 7, "Fname": "Farhan", "Faddress": "Multan"},
    {"Fid": 8, "Fname": "Nida", "Faddress": "Hyderabad"},
    {"Fid": 9, "Fname": "Sajid", "Faddress": "Faisalabad"},
    {"Fid": 10, "Fname": "Areeba", "Faddress": "Sialkot"},
    {"Fid": 11, "Fname": "Tahir", "Faddress": "Gujranwala"},
    {"Fid": 12, "Fname": "iBRAHIM", "Faddress": "isl"},
]

with open("data/family.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Fid", "Fname", "Faddress"])
    writer.writeheader()
    writer.writerows(family_data)

# Person table
person_data = [
    {"Pid": 1, "Fid": 1, "PName": "Ayesha", "Qualification": "BS", "Gender": "F"},
    {"Pid": 2, "Fid": 1, "PName": "Usman", "Qualification": "MS", "Gender": "M"},
    {"Pid": 3, "Fid": 2, "PName": "Zainab", "Qualification": "PhD", "Gender": "F"},
    {"Pid": 4, "Fid": 3, "PName": "Bilal", "Qualification": "Intermediate", "Gender": "M"},
    {"Pid": 5, "Fid": 3, "PName": "Hassan", "Qualification": "Matric", "Gender": "M"},
    {"Pid": 6, "Fid": 4, "PName": "Ibrahim", "Qualification": "Bachelors", "Gender": "M"},
    {"Pid": 7, "Fid": 4, "PName": "Fatima", "Qualification": "MS", "Gender": "F"},
    {"Pid": 8, "Fid": 5, "PName": "Adeel", "Qualification": "PhD", "Gender": "M"},
    {"Pid": 9, "Fid": 5, "PName": "Maliha", "Qualification": "BS", "Gender": "F"},
    {"Pid": 10, "Fid": 6, "PName": "Saad", "Qualification": "Diploma", "Gender": "M"},
    {"Pid": 11, "Fid": 6, "PName": "Kiran", "Qualification": "BS", "Gender": "F"},
    {"Pid": 12, "Fid": 6, "PName": "Danish", "Qualification": "Matric", "Gender": "M"},
    {"Pid": 13, "Fid": 7, "PName": "Laiba", "Qualification": "MS", "Gender": "F"},
    {"Pid": 14, "Fid": 7, "PName": "Hamza", "Qualification": "BS", "Gender": "M"},
    {"Pid": 15, "Fid": 8, "PName": "Noor", "Qualification": "PhD", "Gender": "F"},
    {"Pid": 16, "Fid": 8, "PName": "Amaan", "Qualification": "Intermediate", "Gender": "M"},
    {"Pid": 17, "Fid": 8, "PName": "Rida", "Qualification": "Bachelors", "Gender": "F"},
    {"Pid": 18, "Fid": 9, "PName": "Tariq", "Qualification": "BS", "Gender": "M"},
    {"Pid": 19, "Fid": 9, "PName": "Fariha", "Qualification": "MS", "Gender": "F"},
    {"Pid": 20, "Fid": 9, "PName": "Noman", "Qualification": "Diploma", "Gender": "M"},
    {"Pid": 21, "Fid": 10, "PName": "Waleed", "Qualification": "PhD", "Gender": "M"},
    {"Pid": 22, "Fid": 10, "PName": "Nimra", "Qualification": "BS", "Gender": "F"},
    {"Pid": 23, "Fid": 10, "PName": "Imran", "Qualification": "MS", "Gender": "M"},
    {"Pid": 24, "Fid": 11, "PName": "Yusra", "Qualification": "Bachelors", "Gender": "F"},
    {"Pid": 25, "Fid": 11, "PName": "Zubair", "Qualification": "Matric", "Gender": "M"},
    {"Pid": 26, "Fid": 11, "PName": "Hoor", "Qualification": "Intermediate", "Gender": "F"},
    {"Pid": 27, "Fid": 12, "PName": "Rayyan", "Qualification": "BS", "Gender": "M"},
    {"Pid": 28, "Fid": 12, "PName": "Fiza", "Qualification": "MS", "Gender": "F"},
    {"Pid": 29, "Fid": 12, "PName": "Asad", "Qualification": "Diploma", "Gender": "M"},
    {"Pid": 30, "Fid": 12, "PName": "Hina", "Qualification": "BS", "Gender": "F"},
]

with open("data/person.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Pid", "Fid", "PName", "Qualification", "Gender"])
    writer.writeheader()
    writer.writerows(person_data)

print("✅ family.csv and person.csv files created successfully!")
