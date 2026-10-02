"""Static test data: users, the product catalog and checkout details."""
import os
from decimal import Decimal

from .models import Customer, Product, User

PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")


class Users:
    STANDARD = User("standard_user", PASSWORD)
    LOCKED_OUT = User("locked_out_user", PASSWORD)
    PROBLEM = User("problem_user", PASSWORD)
    PERFORMANCE_GLITCH = User("performance_glitch_user", PASSWORD)
    ERROR = User("error_user", PASSWORD)
    VISUAL = User("visual_user", PASSWORD)


class Products:
    BACKPACK = Product("Sauce Labs Backpack", Decimal("29.99"))
    BIKE_LIGHT = Product("Sauce Labs Bike Light", Decimal("9.99"))
    BOLT_TSHIRT = Product("Sauce Labs Bolt T-Shirt", Decimal("15.99"))
    FLEECE_JACKET = Product("Sauce Labs Fleece Jacket", Decimal("49.99"))
    ONESIE = Product("Sauce Labs Onesie", Decimal("7.99"))
    RED_TSHIRT = Product("Test.allTheThings() T-Shirt (Red)", Decimal("15.99"))

    ALL = [BACKPACK, BIKE_LIGHT, BOLT_TSHIRT, FLEECE_JACKET, ONESIE, RED_TSHIRT]


CUSTOMER = Customer("Ivan", "Tester", "12345")
PAYMENT_INFO = "SauceCard #31337"
SHIPPING_INFO = "Free Pony Express Delivery!"
