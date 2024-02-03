from collections import UserDict

class NotValidPhoneNumber(Exception):
    pass

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotValidPhoneNumber:
            return "Phone number should contain only 10 digits."
        except IndexError:
            return "Phone not found."
        except:
            return "Something went wrong."
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise NotValidPhoneNumber
        self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def find_idx(self, phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                return i
        raise IndexError

    @error_handler
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return 'Phone added.'

    @error_handler
    def remove_phone(self, phone):
        idx = self.find_idx(phone)
        self.phones.pop(idx)
        return 'Phone removed.'

    @error_handler
    def edit_phone(self, phone, new_phone):
        idx = self.find_idx(phone)
        self.phones[idx].value = new_phone
        return 'Phone edited.'

    @error_handler
    def find_phone(self, phone):
        idx = self.find_idx(phone)
        return self.phones[idx]
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return 'Contact added.'
    
    def find(self, name):
        contact = self.data.get(name)
        return contact if contact else 'Contact not found.'

    def delete(self, name):
        contact = self.data.pop(name, None)
        return contact if contact else 'Contact not found.'
    
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")