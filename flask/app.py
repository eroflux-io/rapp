"""
Basic Web App
"""
import logging
from typing import Any

import arrow
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    make_response,
    session,
)
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve

from models import Reminder

TITLE = 'Reminder App'

log = logging.getLogger(__name__)

# Create a new app
app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def index():
    """
    A BASIC / INDEX ROUTE
    """
    # Going to get the lists of instances associated with a user and their costs
    # to display.
    today = arrow.now()
    current_year = today.year

    # First day of the current year
    first_day_of_year = today.floor('year')
    # The number of days since the first of the year
    days_since_first_of_year = (today - first_day_of_year).days

    # End of the current year
    end_of_year = today.replace(month=12, day=31)
    # The number of days remaining in the year
    days_remaining = (end_of_year - today).days

    try:
        dbsession = Session()

        # Get something out of the database
        reminders = dbsession.query(Reminder).all()

    except SQLAlchemyError as e:
        dbsession.rollback()
        log.error(e)
    finally:
        dbsession.close()

    return render_template(
        "index.html",
        title=TITLE,
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80)
