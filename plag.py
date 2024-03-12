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

def save_password(service, username, password):
    if not os.path.exists("passwords.json"):
        with open("passwords.json", "w") as file:
            json.dump({}, file)
    with open("passwords.json", "r") as file:
        passwords = json.load(file)
    encrypted_password = encrypt_password(password)
    passwords[service] = {"username": username, "password": encrypted_password.decode()}
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

def get_password(service):
    if not os.path.exists("passwords.json"):
        return None
    with open("passwords.json", "r") as file:
        passwords = json.load(file)
    encrypted_password = passwords.get(service, {}).get("password", "").encode()
    if not encrypted_password:
        return None
    decrypted_password = decrypt_password(encrypted_password)
    return decrypted_password

def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def main():
    st.title("Password Manager")
    choice = st.selectbox("Select an action:", ["Save", "Retrieve", "Generate and Save"])
    
    if choice == "Save":
        service = st.text_input("Enter the service:")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        if st.button("Save Password"):
            save_password(service, username, password)
            st.success("Password saved successfully!")

    elif choice == "Retrieve":
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
        services = list(passwords.keys())
        service = st.selectbox("Select a service:", services)
        if st.button("Retrieve Password"):
            password = get_password(service)
            if password:
                st.success(f"Your password for {service} is: {password}")
            else:
                st.error("Password not found.")

    elif choice == "Generate and Save":
        service = st.text_input("Enter the service:")
        username = st.text_input("Enter your username:")
        password_length = st.slider("Select the length of the password:", 8, 32, 12)
        generated_password = generate_random_password(password_length)
        st.write(f"Generated Password: {generated_password}")
        if st.button("Save Generated Password"):
            save_password(service, username, generated_password)
            st.success(f"Generated password saved successfully! Your Password is: {generated_password}")

if __name__ == "__main__":
    main()
