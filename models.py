from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, date):
        try:
            self.value = datetime.strptime(date, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone_number):
        if self.validate(phone_number):
            self.value = phone_number
        else:
            raise ValueError(f'Invalid phone number: {phone_number}. Must be 10 digits.')

    @staticmethod
    def validate(number):
        return number.isdigit() and len(number) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        try:
            self.birthday = Birthday(date)
            return 'Birthday added.'
        except ValueError as error:
            return f'{error}'

    def add_phone(self, phone_number):
        if not self.find_phone(phone_number):
            try:
                phone = Phone(phone_number)
                self.phones.append(phone)
                return 'Phone added.'
            except ValueError as error:
                return f'{error}'

    def edit_phone(self, old_phone, new_phone):
        old_phone_exists = self.find_phone(old_phone)
        if old_phone_exists:
            index = self.phones.index(old_phone_exists)
            try:
                new_phone = Phone(new_phone)
                self.phones[index] = new_phone
                return 'Phone changed.'
            except ValueError as error:
                return f'{error}'

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def __str__(self):
        name = self.name.value
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else '-'
        phones = ', '.join(p.value for p in self.phones)
        return f'contact name: {name} | birthday: {birthday} | phones: {phones}'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def find_record(self, name):
        for n in self.data:
            if n.value == name:
                return self.data[n]
        return None

    def delete_record(self, name):
        record = self.find_record(name)
        if record:
            del self.data[record.name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if not record.birthday:
                continue

            user_birthday = record.birthday.value.replace(year=today.year)

            if user_birthday < today:
                user_birthday = user_birthday.replace(year=today.year + 1)

            time_to_birthday = (user_birthday - today).days

            if 0 <= time_to_birthday <= 7:
                congratulation_date = user_birthday
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    'name': name.value,
                    'congratulation_date': congratulation_date.strftime('%d.%m.%Y')
                })

        return upcoming_birthdays

    def print_book(self):
        for _, record in self.data.items():
            print(record)
