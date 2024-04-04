from flask import Blueprint, render_template, url_for
from database import  Database
from models.sight_name import SightName
from models.sight_location import Sight_location
from forms import EditSight
from models.sight import Sight
from models.sight_type import SightType
from datetime import datetime as dt


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/main-page")
def admin_main():
    with Database(dict_cursor=True) as db:

        sight_model = Sight(db)
        sights = sight_model.getAllSights()

        sight_type_model = SightType(db)
        sight_types = sight_type_model.getAllSightTypes()

        sight_name_model = SightName(db)
        sight_names = sight_name_model.getAllSightNames()
    
    return render_template(
        "admin.html",
        sights=sights,
        sight_type_names=[sight_type["name"] for sight_type in sight_types],
        sight_names=[sight_name["name"] for sight_name in sight_names]
    )


@admin.route("/sight/id/<int:sight_id>")
def edit_sight(sight_id):
    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sight = sight_model.getSight(sight_id)

    if sight is not None:
        now = dt.now().time()
        is_open = sight["open_time"] is None and sight["close_time"] is None or \
            sight["open_time"] <= now and sight["close_time"] >= now

        return render_template(
            "edit_sight.html",
            sight=sight
        )