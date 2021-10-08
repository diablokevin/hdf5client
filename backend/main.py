import os
import time
from random import randint
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder='../dist')
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.debug = True


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


# 允许的扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'hdf5'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload_hdf5file', methods=['POST'])
def upload_hdf5file():
    f = request.files.get('file')
    result = False
    if f and allowed_file(f.filename):
        f.save('../hdf5files/' + f.filename)
        result = True
    response = {
        'result': result
    }
    return jsonify(response)


@app.route('/api/get_hdf5_file_list')
def get_hdf5_file_list():
    fileList = []
    domain = '../hdf5files'
    files = os.listdir(domain)
    for info in files:
        info = os.path.join(domain, info)
        file_name = os.path.basename(info)
        file_alter_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(info)))
        file_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(info)))
        # file_alter_time = time.asctime(time.localtime(os.path.getmtime(info)))
        fileList.append({'name': file_name, 'create_time':file_create_time, 'alter_time':file_alter_time})
    response = {
        'fileList': fileList
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
    # webview.create_window('Flask example', app)
    # webview.start()
