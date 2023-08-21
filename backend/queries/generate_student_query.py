import csv

csv_file        = "26_students.csv"
sql_template    = "INSERT INTO students (id, name, registration_no, student_card_id, roll, is_active) VALUES\n"

with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        id = (int)(row['Roll']) + 2600
        name = row['Name']
        registration_no = row['Registration No']
        student_card_id = row['Student Card ID']
        roll = row['Roll']
        sql_template += f"({id}, '{name}', '{registration_no}', '{student_card_id}', '{roll}', true),\n"

# Remove the trailing comma and newline
sql_query = sql_template.rstrip(",\n")

print(sql_query)