import random
import string
from faker import Faker


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RANDOM GENERATE NAME / EMAIL / PHONE NUMBER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# generated_first_names = set()

# def generate_random_name_and_email():
#     """
#     Generates a random full name with a unique first name and email address using the Faker library.
    
#     Returns: 
#     - Tuple containing a unique first name, last name, and email address
#     """
#     fake = Faker()
    
#     while True:
#         full_name = fake.name()
#         first_name, last_name = full_name.split(" ", 1)
        
#         if first_name not in generated_first_names:
#             generated_first_names.add(first_name)
#             email = fake.email()
#             return first_name, last_name, email


def generate_random_name_and_email():
    """
    Generates a random full name with a unique (first name, last name) combination and a unique email address.

    Returns:
    - Tuple containing a unique first name, last name, and email address.
    """
    
    generated_names = set()
    fake = Faker()

    while True:
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name}_{last_name}"

        if full_name not in generated_names:
            generated_names.add(full_name)
            email = f"{full_name.lower()}{random.randint(1000, 9999)}@example.com"
            return full_name, first_name, last_name, email


# def generate_random_name_and_email():
#     """
#     Generates a random full name and email address using the Faker library.
    
#     Returns: 
#     - Tuple containing a random full name and email address
#     """
#     fake = Faker()
#     # Generate a random full name
#     full_name = fake.name()
    
#     # Split into first and last name
#     first_name, last_name = full_name.split(" ", 1)
    
#     # Generate a random email address using the name
#     email = fake.email()
#     return first_name, last_name, email



# def generate_random_credential(length=None):
    
#     # Set default length if not provided
#     if length is None:
#         # Randomly choose length between 6 and 20
#         length = random.randint(6, 20)
#     elif length < 6:
#         raise ValueError("Length must be at least 6 to include all required character types.")

#     # Define character sets
#     lowercase = string.ascii_lowercase
#     uppercase = string.ascii_uppercase
#     digits = string.digits
    
#     # Ensure at least one of each required character type
#     cred = [
#         random.choice(lowercase),  # at least 1 lowercase
#         random.choice(uppercase),  # at least 1 uppercase
#         random.choice(digits)      # at least 1 digit
#     ]
    
#     # Fill the remaining length with random characters
#     remaining_length = length - len(cred)
#     all_chars = lowercase + uppercase + digits
#     cred.extend(random.choice(all_chars) for _ in range(remaining_length))
    
#     # Shuffle the credential to make it random
#     random.shuffle(cred)
    
#     # Join the characters into a single string
#     return ''.join(cred)



def generate_random_credential(length=None):
    # Set default length if not provided
    if length is None:
        # Randomly choose length between 6 and 20
        length = random.randint(6, 20)
    elif length < 6:
        raise ValueError("Length must be at least 6 to include all required character types.")

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/"

    # Ensure at least one of each required character type
    cred = [
        random.choice(lowercase),  # at least 1 lowercase
        random.choice(uppercase),  # at least 1 uppercase
        random.choice(digits),     # at least 1 digit
        random.choice(special_chars) # at least 1 special character
    ]
    
    # Fill the remaining length with random characters
    remaining_length = length - len(cred)
    all_chars = lowercase + uppercase + digits + special_chars
    cred.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the credential to make it random
    random.shuffle(cred)
    
    # Join the characters into a single string
    return ''.join(cred)



def generate_singapore_phone_number():
    """
    Generates a random Singapore phone number (mobile) with a valid prefix (either 8 or 9).
    
    Returns:
    - A random 8-digit Singapore phone number as a string
    """
    # Prefix for Singapore mobile numbers (8 or 9)
    prefix = random.choice(['8', '9'])
    
    # Generate the remaining 7 digits of the phone number
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    
    # Return the full 8-digit phone number
    return prefix + number

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

