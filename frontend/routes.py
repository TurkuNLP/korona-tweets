from flask import Blueprint
from flask import request, render_template
from werkzeug.exceptions import abort

from .db import get_db


bp = Blueprint('frontend', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/search', methods=['GET', 'POST'])
def search():
    q = str(request.values['q'])
    db = get_db()
    response = db.query(q)
    return render_template('search.html', response=response)
