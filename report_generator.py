import argparse
import csv
import statistics
from collections import defaultdict
from tabulate import tabulate

def read_csv_files(files):
    data = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned = {k.strip(): v.strip() for k, v in row.items()}
                    data.append(cleaned)
        except FileNotFoundError:
            print(f"Файл {file} не найден, пропускаем...")
    return data

def median_coffee_report(data):
    student_spends = defaultdict(list)
    for row in data:
        try:
            student = row['student']
            coffee = float(row['coffee_spent'])
            student_spends[student].append(coffee)
        except (KeyError, ValueError):
            continue
    
    result = []
    for student, spends in student_spends.items():
        median = statistics.median(spends)
        result.append({
            'Студент': student,
            'Медианные траты на кофе': round(median, 2)
        })
    
    return sorted(result, key=lambda x: x['Медианные траты на кофе'], reverse=True)

def main():
    parser = argparse.ArgumentParser(description='Обработка данных студентов')
    parser.add_argument('--files', nargs='+', required=True, help='CSV файлы для обработки')
    parser.add_argument('--report', required=True, choices=['median-coffee'], help='Тип отчёта')
    args = parser.parse_args()
    
    data = read_csv_files(args.files)
    
    if not data:
        print("Нет данных для обработки")
        return
    

    if args.report == 'median-coffee':
        report_data = median_coffee_report(data)
        print(tabulate(report_data, headers='keys', tablefmt='grid', stralign='left'))
    else:
        print(f"Неизвестный тип отчёта: {args.report}")

if __name__ == '__main__':
    main()