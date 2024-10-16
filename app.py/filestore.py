import sqlite3

def binaryconverter(insert_file):

    if hasattr(insert_file, 'read'):
        return insert_file.read()

    else:
        with open(insert_file, 'rb') as file:
            blobdata = file.read()
        return blobdata


def insertdata(download_code, upload_time, filename, file_data):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS code_file_db (code TEXT, file_time TEXT, filename TEXT, file BLOB)') 
    cursor.execute('INSERT INTO code_file_db (code, file_time, filename, file) VALUES (?, ?, ?, ?)', (download_code, upload_time, filename, file_data))
    conn.commit()
    conn.close()
