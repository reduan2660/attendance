import csv
import json

def read_csv_and_convert_to_json(csv_file_path):
    data = []
    
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        sorted_rows = sorted(csv_reader, key=lambda x: int(x["Roll"]))
        for row in sorted_rows:
            student_data = {
                "registration_no": row["RegNo"],
                "student_card_id": row["SmardIdCardNo"],
                "name": row["Name"],
                "roll": int(row["Roll"]),
                "batch": 27,
            }
            data.append(student_data)

    return data

def main():
    csv_file_path = '27_students.csv'
    output_data = read_csv_and_convert_to_json(csv_file_path)

    # Output the formatted data as JSON
    output_json = json.dumps(output_data, indent=4)
    print(output_json)

if __name__ == "__main__":
    main()
