from flask import Blueprint, render_template, url_for, request, redirect, flash, current_app
from database import Database
from models.sight import Sight
from models.sight_name import SightName
from models.sight_type import SightType
from forms import Edit_sight_detail, Add_sight_form, get_age_categories, get_categories
from datetime import datetime as dt
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, shutil


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/main-page")
@login_required
def admin_main():
    with Database(dict_cursor=True) as db:

        sight_model = Sight(db)
        sights = sight_model.getAllSights(active_only=False)

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
    edit_sight_form = Edit_sight_detail()
    if request.method == "GET":
        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sight = sight_model.getSight(sight_id)
            sight["active"] = bool(sight["active"])
            
            edit_sight_form.sight_type.choices = sort_dropdown_by_id(sight["sight_type_id"],get_categories())
            edit_sight_form.age_category_id.choices = sort_dropdown_by_id(sight["age_category_id"],get_age_categories())
            

            return render_template(
                "edit_sight.html",
                sight=sight,
                sight_id=sight_id, edit_sight_form=edit_sight_form
            )
    
    else:
        
        if edit_sight_form.validate():
            active = edit_sight_form.active.data
            sight_name = edit_sight_form.sight_name.data
            age_category_id = edit_sight_form.age_category_id.data
            address = edit_sight_form.address.data
            google_maps_url = edit_sight_form.google_maps_url.data
            open_time = edit_sight_form.open_time.data
            close_time = edit_sight_form.close_time.data
            description = edit_sight_form.description.data

            old_sight_type_id = edit_sight_form.old_sight_type.data
            sight_type_id = edit_sight_form.sight_type.data

            images = edit_sight_form.image.data
            
            if images[0]:
                    image_names = fix_image_filename(images, sight_id=sight_id)
                    number_of_images = len(image_names)
                    try:
                        for i in range(number_of_images):
                            images[i].save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_names[i]))
                            sight_model.add_sight_image(sight_id, image_names[i])
                    except Exception as e:
                        return str(e)
            else:
                image_names =""
            

            
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)
                result, message = sight_model.update_sight(sight_id, sight_name, age_category_id, address, google_maps_url, active, open_time, close_time, description, image_names, sight_type_id, old_sight_type_id)

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
            return redirect(url_for("admin.edit_sight" , sight_id=sight_id,edit_sight_form=edit_sight_form))


@admin.route("/add-sight", methods=["GET", "POST"])
@login_required
def add_sight():
    edit_sight_form = Add_sight_form()
    if request.method == "GET":
        return render_template("add_sight.html", edit_sight_form=edit_sight_form)
    else:
        
        if edit_sight_form.validate():
            active = edit_sight_form.active.data
            sight_name = edit_sight_form.sight_name.data
            age_category_id = edit_sight_form.age_category_id.data
            address = edit_sight_form.address.data
            google_maps_url = edit_sight_form.google_maps_url.data
            open_time = edit_sight_form.open_time.data
            close_time = edit_sight_form.close_time.data
            description = edit_sight_form.description.data
            sight_type_id = edit_sight_form.sight_type.data
            
            images = edit_sight_form.image.data
            

        
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)
                result, message = sight_model.add_sight(sight_name, age_category_id, address, google_maps_url, active, open_time, close_time, description,sight_type_id)
                
                sight_id = db.query("SELECT LAST_INSERT_ID();")[0]['LAST_INSERT_ID()']

                if images[0]:
                    image_names = fix_image_filename(images, sight_id=sight_id)
                    number_of_images = len(image_names)
                    try:
                        for i in range(number_of_images):
                            images[i].save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_names[i]))
                            sight_model.add_sight_image(sight_id, image_names[i])
                    except Exception as e:
                        return str(e)
                else:
                    image_name = str(sight_id)+'/1.png'
                    upload_folder_path = f"{current_app.config['UPLOAD_FOLDER']}"
                    exists = os.path.isdir(upload_folder_path+str(sight_id))
                    if not exists:
                        os.mkdir(upload_folder_path+str(sight_id))
                    shutil.copy("static/images/TravelTracer.png", upload_folder_path + image_name)
                    sight_model.add_sight_image(sight_id, image_name)

                if result:
                    flash(message)
                    return render_template("add_sight.html", edit_sight_form=edit_sight_form)
                else:
                    flash(message)
                    return render_template("add_sight.html", edit_sight_form=edit_sight_form)
        
        else:
            return render_template("add_sight.html", edit_sight_form=edit_sight_form)
        

def fix_image_filename(images,sight_id):
    image_names = []
    path = f"{current_app.config['UPLOAD_FOLDER']}/{sight_id}"
    exists = os.path.isdir(path)
    if not exists:
        os.mkdir(path)
    image_id = len([name for name in os.listdir(path)])
    for image in images:
        image_name = secure_filename(image.filename)
        image_extention = os.path.splitext(image_name)[1]
        if image_extention == '':
            continue
            
        image_names.append(f"{sight_id}/{image_id+1}{image_extention}")
        image_id += 1
            
    return image_names


def sort_dropdown_by_id(id,options):
    new = []
    selected = options.pop(id-1)
    new.append(selected)
    for option in options:
        new.append(option)
    return new