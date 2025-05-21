from flask import redirect, render_template, request, session, url_for
from src.db_connection import app
from src.pages.pages_by_users_service import PagesByUsers

@app.route("/pages/<int:user_id>", methods=["GET"])
def page_by_user_id(user_id: int):
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    page = None
    if request.method == 'GET':
        try:
            page = PagesByUsers().get_page_by_user_id(user_id)
        except ValueError as e:
            error = str(e.__str__())

    return render_template('page.html', page=page, error=error)
