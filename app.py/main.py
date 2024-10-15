from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from codegen import generate_code
from filestore import insertdata
from filerelease import get_file_by_code
from filedel import delete_file, database_time, check_for_deletion
from flask_apscheduler import APScheduler
import io
import os

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/test')
def test_page():
    return render_template('mainpage.html')


@app.route('/download')
def download_page():
    return render_template('downloadpage.html')


@app.route('/upload')
def upload_page():
    return render_template('uploadpage.html')


@app.route('/download', methods=['POST'])
def download_file():
    download_code = request.form['download_file']
    file_data, original_filename = get_file_by_code(download_code)

    if file_data and original_filename:
        
        delete_file(download_code)
        return send_file(
            io.BytesIO(file_data),
            as_attachment=True,
            download_name=original_filename,
            mimetype='application/octet-stream'
        )
    else:
        return "File not found", 404


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['upload_file']
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_data = uploaded_file.read()
        download_code = generate_code()
        file_time = database_time()
        insertdata(file_data, download_code, filename, file_time)
        print(download_code)
        return render_template('downloadcode.html', download_code=download_code)
    

@scheduler.task('interval', id='check_for_deletion', hours=1)
def scheduled_check_for_deletion():
    with app.app_context():
        deleted_count = check_for_deletion()
        print(f"Scheduled task ran. Deleted {deleted_count} files.")


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
