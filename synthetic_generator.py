import pandas as pd
import random


data = []
names = ["John Doe", "Jane Doe", "Michael Smith", "Emily Johnson", "Chris O'Neil", "Sophia Brown", "Liam Wilson",
         "Emma Davis", "Olivia Garcia", "Noah Martinez", "Isabella Lee", "James White", "Benjamin Harris",
         "Charlotte Clark", "Lucas Lewis", "Mia Walker", "Ethan Hall", "Amelia Allen", "Alexander Young", 
         "Harper King", "Daniel Wright", "Ella Scott", "Mason Green", "Ava Adams", "Logan Baker"]

companies = ["Google", "Google Inc.", "Amazon", "Amazon Corp.", "Microsoft", "Microsoft LLC", "Tesla", "Tesla Motors",
             "OpenAI", "Open AI", "Meta", "Facebook", "IBM", "International Business Machines", "Apple", "Apple Inc."]

for i in range(50):
    name = random.choice(names)
    address = f"{random.randint(100, 999)} {random.choice(['Main St', '1st Ave', 'Broadway', 'Elm St', 'Market St'])}, {random.choice(['Los Angeles, CA', 'New York, NY', 'San Francisco, CA', 'Austin, TX'])}"
    email = f"{name.lower().replace(' ', '')}{random.randint(1, 100)}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'invalid'])}"
    phone = f"{random.choice(['(123) 456-7890', '123-456-7890', '123.456.7890', '1234567890'])}"
    date = random.choice(["01-02-2024", "2024/02/01", "Feb 1, 2024", "1st Feb 2024"])
    salary = random.choice([55000, 65000, 75000, 120000, 150000, "N/A", 500000])  # 500k is an outlier
    company = random.choice(companies)
    messy_text = random.choice([
        "thsi is an exampl of a txt with erors.",
        "I lovee to wrk at google!",
        "tesla is a great cmpany but I wud prefer Meta.",
        "IBM is old but still strong.",
        "Can yu pleas clarrify ur qustion?",
    ])

    data.append([name, address, email, phone, date, salary, company, messy_text])


columns = ["Name", "Address", "Email", "Phone Number", "Date", "Salary", "Company", "Messy Text"]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
file_path = "synthetic_data.csv"
df.to_csv(file_path, index=False)
file_path
