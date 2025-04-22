import random

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker

from gs_tools_django.users.models import User

fake = Faker()


def generate_random_iran_mobile():
    """Generate a random valid Iranian mobile number.

    Format: +98 9XX XXX XXXX
    Valid operators: 91X, 92X, 93X, 90X, etc.
    """
    valid_operators = [
        "90",
        "91",
        "92",
        "93",
        "94",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
    ]
    operator = random.choice(valid_operators)  # noqa: S311
    remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])  # noqa: S311
    return f"+989{operator}{remaining_digits}"


def generate_unique_phone(max_retries=100):
    """Generate unique phone numbers."""
    for _ in range(max_retries):
        phone = generate_random_iran_mobile()
        if not User.objects.filter(phone_number=phone).exists():
            return phone
    msg = f"Could not generate unique phone number after {max_retries} attempts"
    raise ValueError(msg)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    phone_number = factory.LazyFunction(generate_unique_phone)
    is_active = True
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    password_changed_at = factory.LazyFunction(timezone.now)
