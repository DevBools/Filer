import sqlite3
from datetime import datetime, timedelta

#Delete after download
def delete_file(download_code):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM code_file_db WHERE code = ?", (download_code,))
    conn.commit()
    conn.close()


#current time
def current_time():
    current_time = datetime.now()
    return current_time


#give current time
def database_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#delete after 6 hours
def check_for_deletion():
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    one_hour_ago = (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("DELETE FROM code_file_db WHERE file_time < ?", (one_hour_ago,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted_count