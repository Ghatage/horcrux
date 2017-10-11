from flask import Flask, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"


@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass

    read_and_encrypt(save_path)

    return "successful_upload"


@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir("./static/uploads/")

    #modify_time_sort = lambda f: os.stat("./static/uploads/{}".format(f)).st_atime

    def modify_time_sort(file_name):
        file_path = "./static/uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    filesizes = []
    for file in filenames:
        file_path = "./static/uploads/{}".format(file)
        file_stats = os.stat(file_path)
        filesizes.append(file + " " + str(file_stats.st_size) + " KB")
      #  filesizes.append(file)
    
    return_dict = dict(filesizes=filesizes)
    
    print(return_dict)
    return jsonify(return_dict)

if __name__ == '__main__':
    app.run(debug=False)
