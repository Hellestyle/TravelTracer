from flask import Blueprint, render_template
from database import  Database
from models.sight_name import SightName
from models.sight_location import Sight_location
from forms import EditSight

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/admin")
def admin_page():
    with Database(dict_cursor=True) as db:

        sight_name = SightName(db)
        sight_names = sight_name.getAllSightNames()

        sight_location = Sight_location(db)
        sight_locations = sight_location.get_all_sight_locations()
    
    return render_template(
        "admin.html",
        sight_names = [sight_name["name"] for sight_name in sight_names],
        sight_locations = [sight_location["name"] for sight_location in sight_locations]
    )




@admin.route("/admin/edit/<int:sight_id>")
def admin_edit(sight_id):
    
    edit_sight_form = EditSight()
    