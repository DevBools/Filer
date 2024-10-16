from flask import Flask, render_template, request, redirect, send_file, abort
from werkzeug.utils import secure_filename
from codegen import generate_code
from filestore import insertdata
from filerelease import get_files_by_code
from filedel import delete_file, database_time, check_for_deletion
from flask_apscheduler import APScheduler
import io
import os
from io import BytesIO
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

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
def download_files():
    download_code = request.form['unique_code']
    files = get_files_by_code(download_code)

    if files:
        if len(files) == 1:
            file_data, original_filename = files[0]
            delete_file(download_code)
            return send_file(
                BytesIO(file_data),
                as_attachment=True,
                download_name=original_filename,
                mimetype='application/octet-stream'
            )
        else:
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for file_data, original_filename in files:
                    zf.writestr(original_filename, file_data)
            
            memory_file.seek(0)
            delete_file(download_code)
            return send_file(
                memory_file,
                as_attachment=True,
                download_name=f'{download_code}.zip',
                mimetype='application/zip'
            )
    else:
        return "File not found", 404


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('upload_files')
    
    if not uploaded_files or all(file.filename == '' for file in uploaded_files):
        return "No files uploaded", 400

    total_size = sum(file.content_length for file in uploaded_files)
    if total_size > app.config['MAX_CONTENT_LENGTH']:
        abort(413)

    download_code = generate_code()
    upload_time = database_time()

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_data = file.read()
        insertdata(download_code, upload_time, filename, file_data)
    
    return render_template('downloadcode.html', download_code=download_code)
    

@scheduler.task('interval', id='check_for_deletion', hours=1)
def scheduled_check_for_deletion():
    with app.app_context():
        deleted_count = check_for_deletion()
        print(f"Scheduled task ran. Deleted {deleted_count} files.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
