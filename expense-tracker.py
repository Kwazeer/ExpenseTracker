import argparse
import json
from datetime import datetime


def load_file():
    """Load JSON file or empty list"""
    try:
        with open('expenses.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_file(task):
    """Saving JSON file"""
    try:
        with open('expenses.json', 'w', encoding='utf-8') as file:
            json.dump(obj=task, fp=file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise e


def parse_args():
    """Parsing arguments from terminal"""
    parser = argparse.ArgumentParser('Expense Tracker')
    parser.add_argument('add', help='Add new expense')
    parser.add_argument('--description', type=str, help='Описание')
    parser.add_argument('--amount', type=int, help='Потраченная сумма')
    args = parser.parse_args()

    return args


def add_tracker(data):
    """Adding new expense"""
    tasks = load_file()
    get_id = len(tasks) + 1

    user_data = {
        'id': get_id,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
        'description': data.description,
        'amount': data.amount
    }

    tasks.append(user_data)
    save_file(tasks)


def main():
    """Initializing parser"""
    args = parse_args()
    if args.add:
        add_tracker(args)


main()

