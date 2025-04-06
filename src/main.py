from collections import UserDict
from typing import List


class Field:
    """
    Base class for record fields.

    :param value: The value of the field.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Class for storing a contact's name. This is a required field.

    :param value: The contact's name.
    """

    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    """
    Class for storing a phone number with validation (must be exactly 10 digits).

    :param value: The phone number as a string.
    """

    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must consist of exactly 10 digits.")
        super().__init__(value)


class Record:
    """
    Class for storing information about a contact, including a name and a list of phone numbers.

    :param name: The contact's name.
    """

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        """
        Add a phone number to the record.

        :param phone: The phone number as a string.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """
        Remove a phone number from the record.

        :param phone: The phone number as a string.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Edit an existing phone number in the record.

        :param old_phone: The existing phone number to be replaced.
        :param new_phone: The new phone number as a string.
        """
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                break

    def find_phone(self, phone: str) -> str:
        """
        Find a phone number in the record.

        :param phone: The phone number to search for.
        :return: The phone number if found; otherwise an empty string.
        """
        for p in self.phones:
            if p.value == phone:
                return p.value
        return ""

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Class for managing and storing contact records.
    """

    def add_record(self, record: Record) -> None:
        """
        Add a record to the address book.

        :param record: The Record object to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Find a record by contact name.

        :param name: The name to search for.
        :return: The Record object if found; otherwise None.
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Delete a record from the address book by contact name.

        :param name: The name of the record to delete.
        """
        if name in self.data:
            del self.data[name]


if __name__ == '__main__':
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
