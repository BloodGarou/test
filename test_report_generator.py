import pytest
import csv
import tempfile
import os
from report_generator import read_csv_files, median_coffee_report


@pytest.fixture
def test_files():
    data1 = [
        ['student', 'coffee_spent'],
        ['Иван Петров', '500'],
        ['Иван Петров', '600'],
        ['Мария Иванова', '200'],
    ]
    
    data2 = [
        ['student', 'coffee_spent'],
        ['Иван Петров', '700'],
        ['Петр Сидоров', '300'],
    ]
    
    files = []
    for data in [data1, data2]:
        fd, path = tempfile.mkstemp(suffix='.csv', text=True)
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        files.append(path)
    
    yield files
    
    for path in files:
        os.unlink(path)

def test_read_csv_files(test_files):
    data = read_csv_files(test_files)
    assert len(data) == 5 

def test_median_coffee_report(test_files):
    data = read_csv_files(test_files)
    result = median_coffee_report(data)
    
    assert result[0]['Студент'] == 'Иван Петров'
    assert result[0]['Медианные траты на кофе'] == 600.0  
    
    students = [r['Студент'] for r in result]
    assert 'Мария Иванова' in students
    assert 'Петр Сидоров' in students

def test_empty_file():
    data = read_csv_files(['not_exists.csv'])
    assert data == []

def test_malformed_data():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', encoding='utf-8', delete=False) as f:
        f.write("student,coffee_spent\n")
        f.write("Тест,abc\n")  
        f.write("Тест,100\n")
        path = f.name
    
    try:
        data = read_csv_files([path])
        result = median_coffee_report(data)
        assert result[0]['Медианные траты на кофе'] == 100.0
    finally:
        os.unlink(path)