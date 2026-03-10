import csv
import random
import os

# Karnataka Districts (Districts usually serve as cities in this context)
KARNATAKA_DISTRICTS = [
    "Bangalore", "Mysore", "Hubli-Dharwad", "Mangalore", "Belgaum", 
    "Gulbarga", "Davanagere", "Bellary", "Shimoga", "Tumkur", 
    "Raichur", "Bidar", "Hassan", "Hospet", "Gadag", "Udupi", 
    "Bhadravati", "Chitradurga", "Kolar", "Mandya"
]

# Areas within common Karnataka districts to make it realistic
DISTRICT_AREAS = {
    "Bangalore": ["Indiranagar", "Koramangala", "Jayanagar", "Whitefield", "HSR Layout", "Malleshwaram", "Rajajinagar", "Electronic City"],
    "Mysore": ["Gokulam", "Jayalakshmipuram", "Vijayanagar", "Kuvempunagar", "Siddhartha Layout"],
    "Hubli-Dharwad": ["Vidyanagar", "Keshwapur", "Gokul Road", "Saptapur", "Line Bazaar"],
    "Mangalore": ["Bejai", "Kodialbail", "Kandak", "Surathkal", "Ullal"],
    "Udupi": ["Manipal", "Malpe", "Ambalpady", "Diana Circle"],
    "Belgaum": ["Tilakwadi", "Shahapur", "Camp", "Hindwadi"],
}

DEFAULT_AREAS = ["Main Road", "City Center", "Market Area", "Station Road", "Green Park"]

# Realistic Name Templates
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

def generate_business_name(category):
    name = random.choice(NAMES)
    category_templates = TEMPLATES.get(category, ["{name}'s Services", "{name} Solutions"])
    template = random.choice(category_templates)
    return template.format(name=name)

def migrate_to_karnataka():
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
            
            # 1. Update Name (ensure professional)
            row['full_name'] = generate_business_name(category)
            
            # 2. Update Location to Karnataka
            district = random.choice(KARNATAKA_DISTRICTS)
            row['city'] = district
            
            # 3. Update Area based on District
            areas = DISTRICT_AREAS.get(district, DEFAULT_AREAS)
            row['area'] = random.choice(areas)
            
            updated_rows.append(row)

    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Successfully migrated {len(updated_rows)} providers to Karnataka districts.")

if __name__ == "__main__":
    migrate_to_karnataka()
