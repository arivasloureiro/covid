# from flask import send_file, Blueprint, current_app as app
from flask import render_template, Blueprint, current_app as app
from app.mod_print_covid.GetCovidDataModel import GetCovidDataModel

mod_print_covid = Blueprint('print_covid', __name__)


@mod_print_covid.route('/print', methods=['GET'])
def print_info():
    path_graph = 'static/images/image.png'
    cov = GetCovidDataModel(
        path_graph='{}/app/{}'.format(app.config['BASE_DIR'], path_graph), dpi=200
    )
    cov.get_covid_statistics()
    return render_template('land_page.html', img_path=path_graph)