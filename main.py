import streamlit as st
import json
from cryptography.fernet import Fernet
import os
import secrets
import string

def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def save_passwords(passwords):
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

def get_passwords():
    if not os.path.exists("passwords.json"):
        return {}
    with open("passwords.json", "r") as file:
        passwords = json.load(file)
    return passwords

def save_password(service, username, password, generate_password, password_length=None):
    if generate_password:
        password = generate_random_password(password_length)
        st.write(f"Generated Password: {password}")
    passwords = get_passwords()
    encrypted_password = encrypt_password(password)
    passwords[service] = {"username": username, "password": encrypted_password.decode()}
    save_passwords(passwords)

# def get_password(service):
#     passwords = get_passwords()
#     encrypted_password = passwords.get(service, {}).get("password", "").encode()
#     if not encrypted_password:
#         return None
#     decrypted_password = decrypt_password(encrypted_password)
#     return decrypted_password
def get_password(service):
    passwords = get_passwords()
    password_info = passwords.get(service, {})
    encrypted_password = password_info.get("password", "").encode()
    username = password_info.get("username", "")
    if not encrypted_password:
        return None, None
    decrypted_password = decrypt_password(encrypted_password)
    return decrypted_password, username


# def edit_password(service, new_password, generate_password, password_length):
#     if generate_password:
#         new_password = generate_random_password(password_length)
#         st.write(f"Generated Password: {new_password}")
#     passwords = get_passwords()
#     encrypted_password = encrypt_password(new_password)
#     passwords[service]["password"] = encrypted_password.decode()
#     save_passwords(passwords)

def edit_password(service, new_password, generate_password, password_length):
    if generate_password:
        new_password = generate_random_password(password_length)
        st.write(f"Generated Password: {new_password}")
    passwords = get_passwords()
    encrypted_password = encrypt_password(new_password)
    passwords[service]["password"] = encrypted_password.decode()
    save_passwords(passwords)

def delete_password(service):
    passwords = get_passwords()
    if service in passwords:
        del passwords[service]
        save_passwords(passwords)

def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def main():
    st.title("Password Manager")
    action = st.selectbox("Select an action:", ["Save", "Retrieve", "Edit", "Delete"])

    if action == "Save":
        service = st.text_input("Enter the service:")
        username = st.text_input("Enter your username:")
        password_choice = st.radio("Choose an option:", ["Write your own password", "Generate a password"])
        if password_choice == "Write your own password":
            password = st.text_input("Enter your password:", type="password")
            generate_password = False
        else:
            password_length = st.slider("Select the length of the password:", 8, 32, 12)
            password = None
            generate_password = True
        if st.button("Save Password"):
            if generate_password == True:
                save_password(service, username, password, generate_password, password_length)
                st.success("Password saved successfully!")
            else:
                save_password(service, username, password, generate_password)
                st.success("Password saved successfully!")

    elif action == "Retrieve":
        passwords = get_passwords()
        services = list(passwords.keys())
        service = st.selectbox("Select a service:", services)
        if st.button("Retrieve Password"):
            password, username = get_password(service)
            if password and username:
                st.success(f"The {service} password for {username} is: {password}")
            else:
                st.error("Password not found.")

    elif action == "Edit":
        passwords = get_passwords()
        services = list(passwords.keys())
        service = st.selectbox("Select a service to edit:", services)
        password_choice = st.radio("Choose an option:", ["Write your own password", "Generate a password"])
        if password_choice == "Write your own password":
            new_password = st.text_input("Enter the new password:", type="password")
            generate_password = False
        else:
            password_length = st.slider("Select the length of the password:", 8, 32, 12)
            new_password = None
            generate_password = True
        if st.button("Edit Password"):
            if generate_password == True:
                edit_password(service, new_password, generate_password, password_length)
                st.success("Password saved successfully!")
            else:
                edit_password(service, new_password, generate_password, 0)
                st.success("Password saved successfully!")

    elif action == "Delete":
        passwords = get_passwords()
        services = list(passwords.keys())
        service = st.selectbox("Select a service to delete:", services)
        if st.button("Delete Password"):
            delete_password(service)
            st.success("Password deleted successfully!")

if __name__ == "__main__":
    main()
