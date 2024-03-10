from flask import Blueprint, render_template

from database import  Database
from models.sight import Sight

import json
import os


sight = Blueprint("sight", __name__, template_folder="templates", static_folder="static")


@sight.route("/sights")
def sights():
    
    with Database(dict_cursor=True) as db:
        
        sight_model = Sight(db)

        sights = sight_model.getAllSights()

    return render_template(
        "sight/sights.html",
        sights=sights
    )

@sight.route("/sight/<int:sight_id>")
def sight_details(sight_id):
    
    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sight = sight_model.getSight(sight_id)

    images = [
        "/sight/static/images/tromso-night.jpg",
        "/sight/static/images/brige.jpg",
        "/sight/static/images/sign.jpeg",
        "/sight/static/images/tromso.jpeg"
    ]

    return render_template("sight/sight.html", sight=sight, images=json.dumps(images))


@sight.route("/sight/<string:category>")
def sight_category(category):
        
        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sights = sight_model.getSightByCategory(category)

            if sights is not None:
                return render_template("sight/sights.html", sights=sights)
            else:
                message = "No sights found for this category"
                return render_template("sight/sights.html", message=message)
