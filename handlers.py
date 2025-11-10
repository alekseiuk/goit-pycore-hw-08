from models import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"[{func.__name__}] → Missing arguments. Please provide all required values."
        except KeyError:
            return f"[{func.__name__}] → The specified contact does not exist."
        except ValueError as e:
            return f"[{func.__name__}] → Invalid value: {e}"
    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find_record(name)
    messages = []
    if record is None:
        record = Record(name)
        book.add_record(record)
        messages.append('Contact added.')
    if phone:
        result = record.add_phone(phone)
        if result:
            messages.append(result)
    return ' '.join(messages) if messages else 'Nothing to add.'


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find_record(name)
    if record is None:
        raise KeyError
    return record.edit_phone(old_phone, new_phone)


@input_error
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find_record(name)
    if record is None:
        raise KeyError
    return f'contact name: {record.name.value}, phones: {"; ".join(p.value for p in record.phones)}'


@input_error
def print_all_contacts(book: AddressBook):
    book.print_book()


@input_error
def add_birthday(args, book: AddressBook):
    name, date, *_ = args
    record = book.find_record(name)
    if record is None:
        raise KeyError
    return record.add_birthday(date)


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find_record(name)
    if record is None:
        raise KeyError
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    for item in upcoming_birthdays:
        print(f'name: {item['name']}, congratulation_date: {item['congratulation_date']}')
