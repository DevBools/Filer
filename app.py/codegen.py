import random
import string
import sqlite3

CHARACTERS = string.ascii_uppercase + string.digits*2

def generate_random_char():
    return random.choice(CHARACTERS)

def check_database_for_code(code):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS code_file_db (code TEXT, file BLOB, filename TEXT, file_time TEXT)')
    cursor.execute('SELECT COUNT(*) FROM code_file_db WHERE code = ?', (code,))
    code_exists = cursor.fetchone()[0] > 0
    conn.close()
    return code_exists

def generate_code(length=6):
    generated_code = "".join(generate_random_char() for _ in range(length))
    exists = check_database_for_code(generated_code)

    if exists:
        return generate_code(6)
    else:
        return generated_code
