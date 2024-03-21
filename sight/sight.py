from flask import Blueprint, render_template, url_for, redirect, request

from database import  Database
from models.sight import Sight
from models.sight_type import SightType
from models.sight_name import SightName

import json
from datetime import datetime as dt
from flask import redirect, url_for
import json
from flask import redirect, url_for
import json


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


# Handling cases where the inputbox is not empty and the age is selected
@sight.route("/sight/<string:category>/<string:age>")
def sight_by_category(category, age):
    user_input = category

    age_categories = {
        "children": 1,
        "family_friendly": 2,
        "teenagers": 3,
        "young_adults": 4,
        "adults": 5,
        "seniors": 6
    }
    age_category_id = age_categories[age]

    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sights = sight_model.getSightByCategory(category)

        sight_type_meta = SightType(db)
        sight_types = sight_type_meta.getAllSightTypes()

        sight_name_model = SightName(db)
        sight_names = sight_name_model.getAllSightNames()

        if sights is not None:
            # We need to check the value of "age" parameter
            # If it's "all" by default (it means age == "family_friendly"), just return the sights
            if age_category_id == 2:
                return render_template("sight/sights.html", sights=sights,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input
                                )    
            # If it's not "all", we need to filter the sights by age
            else:
                filtered_sights = [sight for sight in sights if sight["age_id"] == age_category_id]
                
                if not filtered_sights:
                    message = "No sights found"
                    return render_template("sight/sights.html", message=message,
                                        sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                        sight_names = [sight_name["name"] for sight_name in sight_names],
                                        user_input=user_input
                                    )
                else:
                    return render_template("sight/sights.html", sights=filtered_sights,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input
                                )

        # Check if the "category" parameter matches any sight name
        # If it does, redirect to the sight details page
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
                return render_template("sight/sights.html", message=message,
                                       sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                       sight_names = [sight_name["name"] for sight_name in sight_names],
                                       user_input=user_input
                                    )


# Handling cases where the inputbox is empty but the age is selected
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

    else:
        age_category_id = age_categories[age]
        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sights = sight_model.getSightByAge(age_category_id)

            sight_name_model = SightName(db)
            sight_names = sight_name_model.getAllSightNames()

            sight_type_meta = SightType(db)
            sight_types = sight_type_meta.getAllSightTypes()
            
            return render_template("sight/sights.html",
                                sights=sights, 
                                sight_names = [sight_name["name"] for sight_name in sight_names], 
                                sight_type_names=[sight_type["name"] for sight_type in sight_types]
                            )
