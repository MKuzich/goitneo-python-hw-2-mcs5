class PhoneIsNumber(Exception):
    pass

class NameIsString(Exception):
    pass

class NoContacts(Exception):
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Contact not found."
        except KeyError:
            return "Contact not found."
        except PhoneIsNumber:
            return "Phone number should contain only digits."
        except NameIsString:
            return "Name should contain only letters."
        except NoContacts:
            return "No contacts."

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    if not phone.isdigit():
        raise PhoneIsNumber
    if not name.isalpha():
        raise NameIsString
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError
    if not phone.isdigit():
        raise PhoneIsNumber
    if not name.isalpha():
        raise NameIsString
    contacts[name] = phone
    return "Contact changed."


@input_error
def show_contact(args, contacts):
    name = args[0]
    if not name.isalpha():
        raise NameIsString
    return contacts[name]

@input_error
def all(contacts):
    if not contacts:
        raise NoContacts
    all_contacts = []
    for name, phone in contacts.items():
        all_contacts.append(f'{name}: {phone}')
    
    return '\n'.join(all_contacts)

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in ["add"]:
            print(add_contact(args, contacts))
        elif command in ["change"]:
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_contact(args, contacts))
        elif command == "all":
            print(all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()