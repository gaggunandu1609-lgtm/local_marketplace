import csv
import random
import os

TEMPLATES = {
    'Photographer': ["{name} Clicks", "{name} Photography", "Pixel Perfect {name}", "Royal {name} Studio", "Focus {name} Studio"],
    'Bike Mechanic': ["{name} Puncture Shop", "{name} Motors", "Quick Fix {name}", "Master Mechanic {name}", "{name} Auto Tech"],
    'Electrician': ["{name} Electricals", "Sparky {name}", "Power Solution {name}", "Bright {name} Services", "Volt {name} Pro"],
    'Carpenter': ["{name} Woodworks", "Creative {name} Interiors", "{name} Furniture", "Elite Wood {name}", "{name} Craft House"],
    'AC Repair Technician': ["Cool {name} AC Services", "{name} Air Care", "Frosty {name} Tech", "Chill Zone {name}", "{name} Cooling"],
    'Beautician (Home Service)': ["{name} Beauty Studio", "Glow {name} Parlour", "Elegant {name} Spa", "{name} Makeover", "{name} Bridal Care"],
    'Laptop/Computer Repair': ["{name} PC Hub", "Tech Fix {name}", "Laptop Doctor {name}", "{name} Digital Care", "{name} IT Solutions"],
    'Plumber': ["{name} Plumbing", "Flow Specialist {name}", "Leak Fix {name}", "Urban {name} Plumbers", "{name} Water Care"],
    'Home Cleaner': ["Shine {name} Cleaners", "Sparkle {name}", "Fresh Home {name}", "Elite {name} Cleaning", "{name} Eco Clean"],
    'Home Tutor': ["{name} Academics", "Smart {name} Tuition", "Elite {name} Learning", "{name} Knowledge Hub", "{name} Tutors"],
}

NAMES = ["Arjun", "Rohan", "Siddharth", "Ishaan", "Vihaan", "Aditya", "Sai", "Aanya", "Ananya", "Diya", "Kavya", "Myra", "Sana", "Zoya", "Ravi", "Suresh", "Ramesh", "Priya", "Sneha", "Vikram", "Rahul", "Zaid", "Vijay", "Karan", "Simran", "Neha", "Varun", "Deepak", "Sunita", "Anita"]

def generate_name(category):
    name = random.choice(NAMES)
    category_templates = TEMPLATES.get(category, ["{name}'s Services", "{name} Solutions"])
    template = random.choice(category_templates)
    return template.format(name=name)

def update_csv():
    file_path = 'services_data.csv'
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    updated_rows = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            category = row['service_category']
            row['full_name'] = generate_name(category)
            updated_rows.append(row)

    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Successfully updated {len(updated_rows)} provider names in {file_path}")

if __name__ == "__main__":
    update_csv()
