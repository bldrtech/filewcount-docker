import re
import collections
import glob
from datetime import datetime

from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from flask.views import MethodView


basePath = ""
staticBasePath = "/static"
uploadsPath = '/opt/upload/uploads'

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 10485760  # 10 MB


class Upload(MethodView):
    @staticmethod
    def get():
        return render_template("upload.html", title='File Upload', basePath=basePath)

    @staticmethod
    def post():
        errors = []
        output_text = None
        files = request.files['new_file']
        if files:
            try:
                new_file = files.read()
                data = new_file.decode()
                text_data = re.split("\W+", data)
                words_count = len(text_data) - 1
                coll_counted = collections.Counter(text_data)
                key_count = len(coll_counted.keys()) - 1
                if words_count == 0 and key_count == 0:
                    output_text = "File Received... But it was empty. Word Count:{}, Uniq-Word Count:{}".format(words_count, key_count)
                else:
                    output_text = "File Received. Thanks! Word Count:{}, Uniq-Word Count:{}".format(words_count, key_count)
                now = datetime.utcnow()
                file_name = "{0:%Y}{0:%m}{0:%d}.{0:%H}{0:%M}{0:%S}-{1}-{2}.txt".format(now, words_count, key_count)
                file_path = uploadsPath + '/' + file_name
                with open(file_path, 'wb') as output_file:
                    output_file.write(new_file)
                all_file_match = uploadsPath + "/*.txt"
                files_list = glob.glob(all_file_match)
            except:
                errors.append("Problem parsing uploaded file. Is it TEXT?")
        else:
            errors.append("Missing File")
        if not errors and output_text is not None and files_list is not None:
            return render_template("upload.html", title='File Received', output_text=output_text, files_list=files_list, basePath=basePath)
        else:
            return render_template("upload.html", title='File Upload', errors=errors, basePath=basePath)


app.add_url_rule("/file_upload", view_func=Upload.as_view('users'))


@app.route("/<path:path>")
def send_static_asset(path):
    return send_from_directory(app.static_folder, path)

@app.route("/", methods=('GET',))
def index():
    return render_template("upload.html", title='File Upload', basePath=basePath)

if __name__ == "__main__":
    app.run(debug=True)
