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


# Encrypting credential and storing encrypted values
print("\nEncrypting credential:")
credentials = ["username"] # MetatraderID
for credential in credentials:
    encrypted_username = encrypt_and_print(credential)
    print(encrypted_username)