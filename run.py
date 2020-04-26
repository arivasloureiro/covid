from app import app
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    path_graph = 'static/images/image.png'
    return render_template('index.html', img_path=path_graph)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

