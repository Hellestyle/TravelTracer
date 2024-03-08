from flask import Blueprint, render_template

from database import  Database
from models.sight import Sight


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

    return render_template(
        "sight/sight.html",
        sight=sight
    )
