from flask import Blueprint, render_template, url_for, request, redirect, flash
from database import  Database
from models.sight import Sight
from models.sight_name import SightName
from models.sight_type import SightType
from forms import Edit_sight_detail, Add_sight_form
from datetime import datetime as dt
from flask_login import login_required, current_user


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/main-page")
@login_required
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


@admin.route("/sight/id/<int:sight_id>", methods=["GET", "POST"])
@login_required
def edit_sight(sight_id):
    if request.method == "GET":
        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sight = sight_model.getSight(sight_id)

            return render_template(
                "edit_sight.html",
                sight=sight,
                sight_id=sight_id,
            )
    
    else:
        edit_sight_form = Edit_sight_detail(request.form)
        if edit_sight_form.validate():
            active = edit_sight_form.active.data
            sight_name = edit_sight_form.sight_name.data
            age_category_id = edit_sight_form.age_category_id.data
            address = edit_sight_form.address.data
            google_maps_url = edit_sight_form.google_maps_url.data
            open_time = edit_sight_form.open_time.data
            close_time = edit_sight_form.close_time.data
            description = edit_sight_form.description.data
        
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)
                result, message = sight_model.update_sight(sight_id, sight_name, age_category_id, address, google_maps_url, active, open_time, close_time, description)

                if result:
                    flash(message)
                    return redirect(url_for("admin.edit_sight" , sight_id=sight_id))
                else:
                    flash(message)
                    return redirect(url_for("admin.edit_sight" , sight_id=sight_id))
        
        else:
            for errors in edit_sight_form.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("admin.edit_sight" , sight_id=sight_id))


@admin.route("/add-sight", methods=["GET", "POST"])
@login_required
def add_sight():
    if request.method == "GET":
        return render_template("add_sight.html")
    else:
        edit_sight_form = Add_sight_form(request.form)
        if edit_sight_form.validate():
            sight_name = edit_sight_form.sight_name.data
            age_category_id = edit_sight_form.age_category_id.data
            address = edit_sight_form.address.data
            google_maps_url = edit_sight_form.google_maps_url.data
            open_time = edit_sight_form.open_time.data
            close_time = edit_sight_form.close_time.data
            description = edit_sight_form.description.data
        
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)
                result, message = sight_model.add_sight(sight_name, age_category_id, address, google_maps_url, open_time, close_time, description)

                if result:
                    flash(message)
                    return redirect(url_for("admin.add_sight"))
                else:
                    flash(message)
                    return redirect(url_for("admin.add_sight"))
        
        else:
            for errors in edit_sight_form.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for("admin.add_sight"))