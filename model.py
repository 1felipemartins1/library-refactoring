from abc import ABC, abstractmethod

class Price(ABC):
    @abstractmethod
    def get_charge(self, days_rented: int) -> float:
        pass

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return 1


class RegularPrice(Price):
    def get_charge(self, days_rented: int) -> float:
        amount = 2
        if days_rented > 2:
            amount += (days_rented - 2) * 1.5
        return amount


class ChildrenPrice(Price):
    def get_charge(self, days_rented: int) -> float:
        amount = 1.5
        if days_rented > 3:
            amount += (days_rented - 3) * 1.5
        return amount


class NewReleasePrice(Price):
    def get_charge(self, days_rented: int) -> float:
        return days_rented * 3

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return 2 if days_rented > 1 else 1


class Book:
    REGULAR: int = 0
    NEW_RELEASE: int = 1
    CHILDREN: int = 2

    def __init__(self, title: str, price_code: int):
        self.title = title
        self.set_price_code(price_code)

    def set_price_code(self, price_code: int):
        self.price_code = price_code
        if price_code == Book.REGULAR:
            self._price = RegularPrice()
        elif price_code == Book.NEW_RELEASE:
            self._price = NewReleasePrice()
        elif price_code == Book.CHILDREN:
            self._price = ChildrenPrice()

    def get_charge(self, days_rented: int) -> float:
        return self._price.get_charge(days_rented)

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return self._price.get_frequent_renter_points(days_rented)


class Rental:
    def __init__(self, book: Book, days_rented: int):
        self.book = book
        self.days_rented = days_rented

    def get_charge(self) -> float:
        return self.book.get_charge(self.days_rented)

    def get_frequent_renter_points(self) -> int:
        return self.book.get_frequent_renter_points(self.days_rented)


class Client:
    def __init__(self, name: str):
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def get_total_charge(self) -> float:
        total = 0
        for rental in self.rentals:
            total += rental.get_charge()
        return total

    def get_total_frequent_renter_points(self) -> int:
        total = 0
        for rental in self.rentals:
            total += rental.get_frequent_renter_points()
        return total

    def statement(self) -> str:
        result = f"Rental summary for {self.name}\n"
        
        for rental in self.rentals:
            # show figures for this rental 
            result += f"- {rental.book.title}: {rental.get_charge()}\n"

        # add footer lines 
        result += f"Total: {self.get_total_charge()}\n"
        result += f"Points: {self.get_total_frequent_renter_points()}"

        return result

    def html_statement(self) -> str:
        result = f"<h1>Rental summary for <em>{self.name}</em></h1>\n<p>\n"
        
        for rental in self.rentals:
            # show figures for this rental 
            result += f"  {rental.book.title}: {rental.get_charge()}<br>\n"

        # add footer lines 
        result += f"</p>\n<p>Total: <em>{self.get_total_charge()}</em></p>\n"
        result += f"<p>Points: <em>{self.get_total_frequent_renter_points()}</em></p>\n"

        return result