import sqlite3

def get_files_by_code(download_code):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file, filename FROM code_file_db WHERE code = ?', (download_code,))
    selected_data = cursor.fetchall()
    conn.close()

    if selected_data:
        return selected_data  # List of tuples (file_data, filename)
    else:
        return None
