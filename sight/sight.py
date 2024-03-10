from flask import Blueprint, render_template, url_for

from database import  Database
from models.sight import Sight
from models.sight_type import SightType

import json
import os

from datetime import datetime as dt


sight = Blueprint("sight", __name__, template_folder="templates", static_folder="static")


@sight.route("/sights")
def sights():
    
    with Database(dict_cursor=True) as db:
        
        sight_model = Sight(db)

        sight_type_model = SightType(db)

        sights = sight_model.getAllSights()

        sight_types = sight_type_model.getAllSightTypes()

    return render_template(
        "sight/sights.html",
        sights=sights,
        sight_type_names=[sight_type["name"] for sight_type in sight_types]
    )

@sight.route("/sight/<int:sight_id>")
def sight_details(sight_id):
    
    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sight = sight_model.getSight(sight_id)

    now = dt.now().time()

    is_open = sight["open_time"] is None and sight["close_time"] is None or \
        sight["open_time"] <= now and sight["close_time"] >= now

    # We can change file amount here if we want to add more images
    images = [url_for('static', filename=f"images/sight/{sight_photo}") for sight_photo in sight["photos"]]

    return render_template(
        "sight/sight.html",
        sight=sight, images=json.dumps(images),
        is_open=is_open
    )


@sight.route("/sight/<string:category>")
def sight_category(category):
        
        with Database(dict_cursor=True) as db:

            sight_model = Sight(db)
            sights = sight_model.getSightByCategory(category)

            sight_type_meta = SightType(db)

            sight_types = sight_type_meta.getAllSightTypes()

            if sights is not None:
                return render_template("sight/sights.html", sights=sights, sight_type_names=[sight_type["name"] for sight_type in sight_types])
            else:
                message = "No sights found for this category"
                return render_template("sight/sights.html", message=message, sight_type_names=[sight_type["name"] for sight_type in sight_types])
