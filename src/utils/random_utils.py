import random
import string

# Common valid US area codes (major cities/areas)
US_AREA_CODES = ["212", "213", "310", "312", "404", "408", "415", "469", "512", "617", "702", "713", "714", "818", "919"]

# Common valid Thai mobile prefixes
THAI_MOBILE_PREFIXES = [
    "061", "062", "063", "064", "065",  # AIS
    "081", "082", "083", "084", "085", "086", "087", "088", "089",  # AIS & DTAC
    "091", "092", "093", "094", "095", "096", "097", "098", "099"  # True & DTAC
]


def random_userid() -> str:
    """Format: 10 digits number"""
    return ''.join(random.choices(string.digits, k=10))


def random_password() -> str:
    """Format: 12 characters including uppercase, lowercase, numbers, and special characters"""
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = '!@#$%^&*()_+-=[]{}|;:,.<>?'

    # Ensure at least one character from each set
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]

    # Fill the rest with random characters from all sets
    all_chars = uppercase + lowercase + digits + special
    password.extend(random.choices(all_chars, k=8))

    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)


def random_email() -> str:
    """Generate a random email address with some popular domain."""
    # Generate random username (8-12 characters)
    domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
        "aol.com",
        "proton.me",
        "aquriux.com"
    ]
    username_length = random.randint(8, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return f"{username}@{random.choice(domains)}"


def random_phone_number(country_code: int | str) -> str:
    """Generate a random realistic phone number based on the country code. Focuses on common patterns only."""
    match str(country_code):
        case '84':  # Vietnam - most common is 09x
            number = '09' + ''.join(random.choices(string.digits, k=8))
            return number

        case '65':  # Singapore - most common is 9
            return '9' + ''.join(random.choices(string.digits, k=7))

        case '1':  # United States - 10 digits
            area = random.choice(US_AREA_CODES)
            prefix = ''.join(random.choices(string.digits, k=3))
            line = ''.join(random.choices(string.digits, k=4))
            return f"{area}{prefix}{line}"

        case '86':  # China - most common starts with 13
            return '13' + ''.join(random.choices(string.digits, k=9))

        case '66':  # Thailand - 10 digits starting with valid prefix
            prefix = random.choice(THAI_MOBILE_PREFIXES)
            line = ''.join(random.choices(string.digits, k=7))
            return f"{prefix}{line}"

        case _:
            raise ValueError(f"Not supported country code for {country_code!r}!")


def random_username() -> str:
    """Generate a random username with prefix 'Auto'. Format: Auto + random string of 8 characters (letters and numbers)"""
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"Auto {random_suffix}"


def random_invalid_email() -> str:
    """Generate an invalid email address randomly."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


def random_number_by_length(length: int = 20) -> str:
    """Generate a random number with specified length."""
    if length <= 0:
        return ""
    return ''.join(random.choices(string.digits, k=length))


def random_invalid_password(amount=1):
    """
    Generate an invalid password by randomly choosing one of several invalid patterns:
    1. Too short (less than 8 characters)
    2. Missing uppercase letters
    3. Missing lowercase letters
    4. Missing numbers
    5. Missing special characters
    6. Empty string
    7. Only whitespace
    8. Only one type of character
    """
    invalid_patterns = [
        # Too short
        ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=random.randint(1, 7))),
        # Missing uppercase
        ''.join(random.choices(string.ascii_lowercase + string.digits + '!@#$%^&*', k=12)),
        # Missing lowercase
        ''.join(random.choices(string.ascii_uppercase + string.digits + '!@#$%^&*', k=12)),
        # Missing numbers
        ''.join(random.choices(string.ascii_letters + '!@#$%^&*', k=12)),
        # Missing special characters
        ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
        # Only one type of character
        random.choice([
            ''.join(random.choices(string.ascii_lowercase, k=12)),  # Only lowercase
            ''.join(random.choices(string.ascii_uppercase, k=12)),  # Only uppercase
            ''.join(random.choices(string.digits, k=12)),  # Only numbers
            ''.join(random.choices('!@#$%^&*', k=12))  # Only special chars
        ])
    ]

    return random.choices(invalid_patterns, k=amount)
