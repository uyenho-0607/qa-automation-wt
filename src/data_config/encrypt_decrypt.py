from cryptography.fernet import Fernet

"""Generate a new key """
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)

# #Print or store the key securely
# print("\nGenerated Key:", key.decode())


# Your fixed encryption key (replace with your actual key)
key = b'OnFEgT-DvjTC2J4kjxwZNsG9Timun_v9WQNodWdIPEk='

cipher_suite = Fernet(key)


def encrypt_and_print(data):
    encrypted_data = cipher_suite.encrypt(data.encode()).decode()
    # print(f"\nEncrypted: {data} -> {encrypted_data}")
    return encrypted_data

def decrypt_and_print(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
    # print(f"\nDecrypted: {encrypted_data} -> {decrypted_data}")
    return decrypted_data


# Encrypting usernames and storing encrypted values
print("\nEncrypting Usernames:")
encrypted_usernames = []
usernames = ["9093131"] # MetatraderID
for username in usernames:
    encrypted_username = encrypt_and_print(username)
    encrypted_usernames.append(encrypted_username)
    print(encrypted_username)


# Encrypting passwords and storing encrypted values
print("\nEncrypting Passwords:")
encrypted_passwords = []
passwords = ["Asd123"] # Password
for password in passwords:
    encrypted_password = encrypt_and_print(password)
    encrypted_passwords.append(encrypted_password)
    print(encrypted_password)


"""
# Decrypting usernames
print("\nDecrypting Usernames:")
for encrypted_username in encrypted_usernames:
    decrypt_and_print(encrypted_username)
    
    
# Decrypting passwords
print("\nDecrypting Passwords:")
for encrypted_password in encrypted_passwords:
    decrypt_and_print(encrypted_password)
"""

