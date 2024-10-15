import sqlite3

def get_file_by_code(download_code):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute('SELECT file, filename FROM code_file_db WHERE code = ?', (download_code,))
    selected_data = cursor.fetchone()

    conn.close()

    if selected_data:
        return selected_data[0], selected_data[1]  # file data and filename
    else:
        return None, None