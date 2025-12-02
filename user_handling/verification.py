import secrets
import re
import bcrypt
from pathlib import Path
import sqlite3
from user_handling.schema import create_users_table
from user_handling.db import connect_database


#FINDING USER IN DATABASE
def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
        )
    user = cursor.fetchone()
    conn.close()
    return user


#ADDING USER TO THE DATABASE
def insert_user(username, password_hash, role):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
         (username, password_hash, role)
    )
    conn.commit()
    conn.close()


def hash_password(plain_text_password):
    """Returns a hashed password, created from plain text password."""
# TODO:Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
# TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
# TODO: Hash the password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
# TODO: Decode the hash back to a string to store in a text file
    hashed_str = hashed_password.decode('utf-8')
    return hashed_str


def register_user(username, password, role):
    """Returns if the user has been registered."""
    conn = connect_database()
    create_users_table(conn)
    #Checking if the username already exists
    if get_user_by_username(username):
        return False
    #validating user credentials
    valid_username = validate_username(username)
    valid_password = validate_password(password)
    if valid_username == False:
        return "username"
    if valid_password == False:
        return "password"
    #Hashing the password
    hashed_str = hash_password(password)
    #inserting user into database
    insert_user(username, hashed_str, role)
    return True


def verify_password(username, plain_text_password):
    """It returns True, if password matches and False, if not."""
    conn = connect_database()
    create_users_table(conn)
    #finding the user in database
    user = get_user_by_username(username)
    if not user:
        return "username"
    hashed_password = user[2]
    # TODO: Encode both the plaintext password and the stored hash to byt
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    # TODO: Use bcrypt.checkpw() to verify the password
    match = bcrypt.checkpw(password_bytes, hashed_password)
    # This function extracts the salt from the hash and compares
    return match


def login_user(username, password):
    """Returns if the user is loged in."""
    return verify_password(username, password)


def change_password(username, new_password):
    """Changes password of the user."""
    #hashing the new password
    new_password_hashed = hash_password(new_password)
    #connecting to the database
    conn = connect_database()
    cursor = conn.cursor()
    #changing the password
    cursor.execute("""UPDATE users SET password_hash = ? WHERE username = ?""", (new_password_hashed, username))
    conn.commit()
    #how many rows were updated
    updated = cursor.rowcount
    conn.close()
    return updated == 1


def validate_username(username):
    """Returns if the username is valid."""
    # checking the username
    if (len(username) < 3) | (not username.isalnum()) | (len(username) > 20):
        return False
    return True


def validate_password(password):
    """Returns if the password is valid."""
    if (len(password) < 8) | (len(password) >= 24) | (not re.search(r"[A-Z]", password)) | (not re.search(r"[a-z]", password)) | (not re.search(r"\d", password)) | (not re.search(r"[!@#$%^&*(),.?/\"':{}|<>]", password)):
        return False
    return True


def check_password_strength(password):
    """Returns how strong the password is(weak, medium, strong)."""
    # Implement logic based on:
    # creating variable to store score for password strenght
    score = 0
    # - Length
    # checking length
    if len(password) > 16:
        if len(password) > 20:
            score += 10
        else:
            score += 5

    # creating variables for checking what characters are in the password
    numb = 0
    sc = 0
    ul = 0
    # - Presence of uppercase, lowercase, digits, special characters
    # counting how many of each characters are in the password
    for digit in password:
        if digit.isdigit():
            numb += 1
        if digit.isupper():
            ul += 1
        if not digit.isalnum():
            sc += 1

    # adding to score based on each character variable value
    if numb > 2:
        score += 10
    if sc > 1:
        score += 10
    if ul > 2:
        score += 10

# - Common password patterns
    common_passwords = [
        "Password1!",
        "Welcome123!",
        "Admin@123",
        "Qwerty123!",
        "Summer2024!",
        "Winter2023@",
        "HelloWorld1!",
        "Test@1234",
        "ILoveYou2!",
        "Sunshine@9",
        "Abc12345!",
        "Football2025#",
        "London2024$",
        "Chocolate1!",
        "MyPass@123",
        "Secure123#",
        "HappyDay7@",
        "Dragon99!",
        "Freedom#22",
        "Monkey@88",
        "StarLight7!",
        "Galaxy2025!",
        "BlueSky@11",
        "Rainbow#123"
    ]

    # checking if password match one of the most common ones
    for item in common_passwords:
        if password == item:
            return "Your password is one of the most used. Try another."

    if score >= 25:
        return "Strong password"
    elif score >= 10:
        return "Medium password"
    else:
        return "Weak password"


def create_session(username):
    """Returns token for the user."""
    token = secrets.token_hex(16)
    # Store token with timestamp
    return token


def get_user_role(username):
    """Returns a role of user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
        )
    user = cursor.fetchone()
    conn.close()
    role = user[3]
    return role
