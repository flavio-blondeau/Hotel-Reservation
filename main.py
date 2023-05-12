import pandas as pd

# import csv files
df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df['id'] == self.hotel_id, "available"] = 'no'
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df['id'] == self.hotel_id, "available"].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self):
        """Print on screen customer name and hotel reserved"""
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.the_customer_name}
        Hotel: {self.hotel_object.name}
        """
        return content

    @property
    def the_customer_name(self):
        cust_name = self.customer_name.strip()
        cust_name = cust_name.title()
        return cust_name


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        """Check if given credit card data are stored in the csv file"""
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        """Check if given credit card password is stored in the csv file"""
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


# Script
print("Welcome to Hotel Reservation App!\n")
while True:
    # Ask for number of people (only numbers > 0)
    nr_people = input("For how many people do you want to book? ")
    if nr_people.isdigit():
        nr_people = int(nr_people)
        if nr_people > 0:
            break
        else:
            print("Please insert a positive number.")
    else:
        print("Please insert a valid number.")

# Show hotels with enough capacity
print(f"Hotels list with {nr_people} places:")
print(df.loc[df['capacity'] >= nr_people])

while True:
    # Choose a hotel (if not available can retry)
    hotel_ID = input("Enter the id of the hotel: ")
    hotel = Hotel(hotel_ID)

    if hotel.available():
        # Ask for card data (if not available can retry)
        print("\nPayment with Credit Card.")
        card_number = input("Please insert your card number: ")
        credit_card = SecureCreditCard(number=card_number)
        card_holder = input("Insert holder name and surname: ").upper()
        card_exp = input("Insert expiration date(mm/yy): ")
        card_cvc = input("Insert card CVC: ")

        if credit_card.validate(expiration=card_exp, holder=card_holder, cvc=card_cvc):
            # Ask for card password (if not available can retry)
            card_password = input("Insert your card password: ")
            if credit_card.authenticate(given_password=card_password):
                print("Payment has been successful.\n")
                hotel.book()
                name = input("Enter your name: ")
                reservation_ticket = ReservationTicket(name, hotel)
                print(reservation_ticket.generate())
                print("\nThank you for choosing our App.")
                break
            else:
                print("Credit card authentication failed.")
                question = input("Do you want to retry?(y/n) ")
                if question not in ('y', 'Y', 'yes', 'Yes', 'YES'):
                    break
        else:
            print("Credit card not accepted.")
            question = input("Do you want to retry?(y/n) ")
            if question not in ('y', 'Y', 'yes', 'Yes', 'YES'):
                break
    else:
        print("Hotel is not free.")
        question = input("Do you want to retry?(y/n) ")
        if question not in ('y', 'Y', 'yes', 'Yes', 'YES'):
            break

print("\nGoodbye!")
