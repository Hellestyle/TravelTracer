from flask import Blueprint, render_template, url_for, redirect, request

from database import  Database
from models.sight import Sight
from models.sight_type import SightType
from models.sight_name import SightName

import json
import os

from datetime import datetime as dt


sight = Blueprint("sight", __name__, template_folder="templates", static_folder="static")


@sight.route("/sights")
def sights():
    
    with Database(dict_cursor=True) as db:
        
        sight_model = Sight(db)
        sights = sight_model.getAllSights()

        sight_type_model = SightType(db)
        sight_types = sight_type_model.getAllSightTypes()

        sight_name_model = SightName(db)
        sight_names = sight_name_model.getAllSightNames()

    return render_template(
        "sight/sights.html",
        sights=sights,
        sight_type_names=[sight_type["name"] for sight_type in sight_types],
        sight_names = [sight_name["name"] for sight_name in sight_names]
    )

@sight.route("/sight/id/<int:sight_id>")
def sight_details(sight_id):
    
    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sight = sight_model.getSight(sight_id)

    if sight is not None:
        now = dt.now().time()

        is_open = sight["open_time"] is None and sight["close_time"] is None or \
            sight["open_time"] <= now and sight["close_time"] >= now

        images = [url_for('static', filename=f"images/sight/{sight_photo}") for sight_photo in sight["photos"]]

        return render_template(
            "sight/sight.html",
            sight=sight, images=json.dumps(images),
            is_open=is_open
        )
    else:
        message = "No sights found"
        return render_template("sight/sights.html", message=message)


@sight.route("/sight/<string:category>/<string:age>")
def sight_by_category(category, age):
        
        with Database(dict_cursor=True) as db:

            sight_model = Sight(db)
            sights = sight_model.getSightByCategory(category)

            sight_type_meta = SightType(db)
            sight_types = sight_type_meta.getAllSightTypes()

            if sights is not None:
                return render_template("sight/sights.html", sights=sights, sight_type_names=[sight_type["name"] for sight_type in sight_types], age=age)
            else:
                sight_model = Sight(db)
                sights = sight_model.getAllSights()

                sight_id = None
                for sight in sights:
                    if category.lower() == sight['name'].lower():
                        sight_id = sight['id']
                        break
                
                if sight_id is not None:
                    return redirect(url_for("sight.sight_details", sight_id=sight_id))
                else:
                    message = "No sights found"
                    return render_template("sight/sights.html", message=message)


@sight.route("/sight/<string:age>")
def sight_by_age(age):
    age_categories = {
        "children": 1,
        "family_friendly": 2,
        "teenagers": 3,
        "young_adults": 4,
        "adults": 5,
        "seniors": 6
    }

    if age == "family_friendly":
        return redirect(url_for("sight.sights"))
    
    # get sights by age category from database
    else:
        # Saw this in the database
        age_category_id = age_categories[age]
        
        return render_template("sight/sights.html", age=age)
