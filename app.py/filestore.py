import sqlite3

def binaryconverter(insert_file):

    if hasattr(insert_file, 'read'):
        return insert_file.read()

    else:
        with open(insert_file, 'rb') as file:
            blobdata = file.read()
        return blobdata


def insertdata(file_data, download_code, filename, file_time):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS code_file_db (code TEXT, file BLOB, filename TEXT, file_time TEXT)')
    cursor.execute('INSERT INTO code_file_db (code, file, filename, file_time) VALUES (?, ?, ?, ?)', (download_code, file_data, filename, file_time))
    conn.commit()
    conn.close()
