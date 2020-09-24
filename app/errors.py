from flask import render_template
from app import db, app


@app.errorhandler(404)
def error_manager(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def database_error(error):
    db.session.rollback()
    return rennder_template('500.html'), 500
