import argparse
import json
import calendar
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
    subparser = parser.add_subparsers(dest='command', help='Команды')

    add_parser = subparser.add_parser('add', help='Add new expense')
    add_parser.add_argument('--description', type=str, help='Description of expense')
    add_parser.add_argument('--amount', type=int, help='Used money')

    list_parser = subparser.add_parser('list', help='Show list of expenses')

    summary_parser = subparser.add_parser('summary', help='Summary of all expenses')
    summary_parser.add_argument('--month', type=int, help='Summary of chosen month')

    delete_parser = subparser.add_parser('delete', help='Delete parser')
    delete_parser.add_argument('--id', type=int, help='ID of expense to delete')

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
    print(f'Expense added successfully (ID: {get_id})')


def show_expenses():
    """Listing all expenses"""
    tasks = load_file()

    print('# ID  Date               Description   Amount')
    for task in tasks:
        print(f'# {task['id']:<2}  {task['date']:<10}   {task['description']:<12}  ${task['amount']}')


def sum_expenses(args):
    """Summary of all expenses or filtrating by month"""
    tasks = load_file()
    month_converted = f'{args.month:02d}'
    month_name = calendar.month_name[int(month_converted)]

    # You can format DATE in JSON using strptime which is better, but I decided to shortcut and make List Comprehension
    summary_by_month = sum([task['amount'] for task in tasks if task['date'].split('.')[1] == month_converted])
    if args.month:
        print(f'Total expenses for {month_name}: ${summary_by_month}')
    else:
        summary = sum(task['amount'] for task in tasks)
        print(f'Total expenses: ${summary}')


def delete_expense_by_id(args):
    """Deleting expense by its ID"""
    tasks = load_file()
    for i, task in enumerate(tasks):
        if task['id'] == args.id:
            del tasks[i]
            save_file(tasks)
            print('Expense deleter successfully')


def main():
    """Initializing parser"""
    args = parse_args()
    if args.command == 'add':
        add_tracker(args)
    if args.command == 'list':
        show_expenses()
    if args.command == 'summary':
        sum_expenses(args)
    if args.command == 'delete':
        delete_expense_by_id(args)


main()
