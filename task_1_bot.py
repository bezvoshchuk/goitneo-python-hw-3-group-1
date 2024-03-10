from task_2_bot_classes import (Name, Phone, Record, AddressBook,\
                    Birthday, IsCorrectPhoneFormat, \
                    IsCorrectDateFormat, IsRecordInContacts, IsBirthdayInRecord)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Give me name and/or phone please."
        except KeyError:
            return 'User does not exists.'
        except IsCorrectPhoneFormat as error:
            return error
        except IsCorrectDateFormat as error:
            return error
        except IsRecordInContacts as error:
            return error
        except IsBirthdayInRecord as error:
            return error
    return inner

def hello_command(args, contacts):
    return 'How can I help you?'

@input_error
def add_contact(args, contacts: AddressBook):
    name = Name(args[0])
    phone = Phone(args[1])

    contacts.add_record(Record(name, phone))
    return 'Contact added.'

@input_error
def change_contact(args, contacts: AddressBook):
    name = Name(args[0])
    new_phone = Phone(args[1])

    old_record = contacts.find(name)
    old_phone = old_record.phones[0]
    old_record.edit_phone(old_phone, new_phone)
    return 'Contact changed.'

@input_error
def get_phone(args, contacts: AddressBook):
    name = args

    record = contacts[name[0]]
    return record.phones

def get_all_phones(args, contacts: AddressBook):
    return contacts

@input_error
def add_birthday(args, contacts: AddressBook):
    name = Name(args[0])
    birthday = Birthday(args[1])

    record = contacts.find(name)
    record.add_birthday(name, birthday)
    return 'Birthday added.'

@input_error
def get_birthday(args, contacts: AddressBook):
    name = Name(args[0])

    record = contacts.find(name)
    return record.show_birthday()

def get_birthdays_per_week(args, contacts: AddressBook):
    return contacts.get_birthdays_per_week(contacts)

def exit_command(args, contacts):
    return 'Good bye!'

def list_commands(args, contacts):
    command_list = "Available commands:\n"
    for commands in COMMAND_HANDLER.values():
        command_list += ", ".join(commands) + "\n"
    return command_list

def unknown_command(args, contacts):
    return 'Unknown command'

COMMAND_HANDLER = {
    hello_command: ['hello', 'hi', 'привіт'],
    add_contact: ['add', 'додати'],
    change_contact: ['change', 'змінити'],
    get_phone: ['phone', 'number', 'телефон', 'номер'],
    get_all_phones: ['all', 'усі контакти'],
    add_birthday: ['add-birthday', 'додати день народження'],
    get_birthday: ['show-birthday', 'дізнатись день народження'],
    get_birthdays_per_week: ['birthdays', 'дні народження'],
    exit_command: ['exit', 'close', 'quit', 'вийти'],
    list_commands: ['list', 'команди']
}

def parser(user_input: str):
    for cmd, words in COMMAND_HANDLER.items():
        for word in words:
            if user_input.startswith(word):
                return cmd, user_input[len(word):].split()
    return unknown_command, []

def main():
    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command: ')
        cmd, data = parser(user_input)
        print(cmd(data, contacts))

        if cmd == exit_command:
            contacts.dump('address_book.pickle')
            break

if __name__ == '__main__':
    contacts = AddressBook()

    contacts.load('address_book.pickle')
    main()