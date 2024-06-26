from flask import Blueprint, render_template, url_for, request, redirect, flash, current_app
from database import Database
from models.sight import Sight
from models.sight_name import SightName
from models.sight_type import SightType
from models.achievement import Achievement
from forms import Edit_sight_detail, Add_sight_form, get_age_categories, get_categories, Edit_acheivements, Delete_achievement, EditOrAddSightType, Achievements_In_Sight
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

#Edit sight function
@admin.route("/sight/id/<int:sight_id>", methods=["GET", "POST"])
@login_required
def edit_sight(sight_id):
    
    achievement_sight_form = Achievements_In_Sight()
    edit_sight_form = Edit_sight_detail()

    if request.method == "GET":
        
        achievement_list = populate_form(sight_id)
        achievement_sight_form.achievements.choices = achievement_list
        
        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sight = sight_model.getSight(sight_id)
            sight["active"] = bool(sight["active"])
            sight["old_sight_type"] = sight["sight_type_id"]
            
            edit_sight_form.sight_type.choices = sort_dropdown_by_id(sight["sight_type_id"],get_categories())
            edit_sight_form.age_category_id.choices = sort_dropdown_by_id(sight["age_category_id"],get_age_categories())
            
            return render_template(
                "edit_sight.html",
                sight=sight,
                sight_id=sight_id, edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form
            )
    elif request.method == "POST":
        
        achievement_list = populate_form(sight_id)
        achievement_sight_form.achievements.choices = achievement_list

        with Database(dict_cursor=True) as db:
            sight_model = Sight(db)
            sight = sight_model.getSight(sight_id)
            sight["active"] = bool(sight["active"])
            
            edit_sight_form.sight_type.choices = sort_dropdown_by_id(sight["sight_type_id"],get_categories())
            edit_sight_form.age_category_id.choices = sort_dropdown_by_id(sight["age_category_id"],get_age_categories())
        
        if edit_sight_form.submit.data and edit_sight_form.validate():
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

            a_id_list= []
            for ids in achievement_sight_form.achievements.data:
                a_id_list.append(int(ids))
            with Database() as db:
                try:
                    db.query("DELETE FROM sight_has_achievement WHERE`sight_id` = %s",(sight_id,))
                    for achievement_ids in a_id_list:
                        db.query("INSERT INTO `sight_has_achievement` (`achievement_id`, `sight_id`) VALUES (%s, %s)",(achievement_ids,sight_id,))
                except Exception as e:
                    return f'{e=}'
                
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)

            if images[0]:
                image_names = fix_image_filename(images, sight_id=sight_id)
                number_of_images = len(image_names)
                try:
                    for i in range(number_of_images):
                        images[i].save(os.path.join(current_app.config['SIGHT_IMAGE_FOLDER'], image_names[i]))
                        sight_model.add_sight_image(sight_id, image_names[i])
                except Exception as e:
                    return f'{e=}'
                
            else:
                image_names =""
            
            with Database(dict_cursor=True) as db:
                sight_model = Sight(db)
                result, message = sight_model.update_sight(sight_id, sight_name, age_category_id, address, google_maps_url, active, open_time, close_time, description, image_names, sight_type_id, old_sight_type_id)
                flash(message)
                return redirect(url_for("admin.edit_sight" , sight_id=sight_id))
        else:
            return render_template("edit_sight.html" ,sight=sight, sight_id=sight_id, edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form)

#Add sight function 
@admin.route("/add-sight", methods=["GET", "POST"])
@login_required
def add_sight():
    achievement_sight_form = Achievements_In_Sight()
    edit_sight_form = Edit_sight_detail()
    if request.method == "GET":
        achievement_list = populate_form(None)
        achievement_sight_form.achievements.choices = achievement_list

        edit_sight_form.sight_type.choices = get_categories()
        edit_sight_form.age_category_id.choices = get_age_categories()
        return render_template("add_sight.html", edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form)
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
                            images[i].save(os.path.join(current_app.config['SIGHT_IMAGE_FOLDER'], image_names[i]))
                            sight_model.add_sight_image(sight_id, image_names[i])
                    except Exception as e:
                        return str(e)
                else:
                    image_name = str(sight_id)+'/1.png'
                    upload_folder_path = f"{current_app.config['SIGHT_IMAGE_FOLDER']}"
                    exists = os.path.isdir(upload_folder_path+str(sight_id))
                    if not exists:
                        os.mkdir(upload_folder_path+str(sight_id))
                    shutil.copy("static/images/TravelTracer.png", upload_folder_path + image_name)
                    sight_model.add_sight_image(sight_id, image_name)
                
                a_id_list= []
                for ids in achievement_sight_form.achievements.data:
                    a_id_list.append(int(ids))
                    try:
                        print(a_id_list)
                        for achievement_ids in a_id_list:
                            db.query("INSERT INTO `sight_has_achievement` (`achievement_id`, `sight_id`) VALUES (%s, %s)",(achievement_ids,sight_id,))
                    except Exception as e:
                        return f'{e=}'

                if result:
                    flash(message)
                    return redirect(url_for("admin.edit_sight" , sight_id=sight_id))
                    return render_template("add_sight.html", edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form)
                else:
                    flash(message)
                    return render_template("add_sight.html", edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form)
        else:
            achievement_list = populate_form(None)
            achievement_sight_form.achievements.choices = achievement_list
            return render_template("add_sight.html", edit_sight_form=edit_sight_form, achievement_sight_form=achievement_sight_form)   


@admin.route("/achievements", methods=["GET", "POST"])
@login_required
def achievements_page():
    
    path = f"{current_app.config['ACHIEVEMENTS_FOLDER']}" 
    
    with Database() as db:
        obj = Achievement(db)
        success, message, achievements = obj.getAchievements(1)
        
    if request.method == "GET":
        
        return render_template("achievements.html", achievements = achievements, path=path)

#Edit achievement page with form
@admin.route("/achievements/edit/<int:achievement_id>", methods=["GET", "POST"])
@login_required
def achievement_edit(achievement_id):
    delete_form = Delete_achievement()
    edit_achievement_form = Edit_acheivements()
    path = f"{current_app.config['ACHIEVEMENTS_FOLDER']}"
    message=False
    with Database(dict_cursor=True) as db:
        achievement = Achievement(db)
        result = achievement.get_achievement_data(achievement_id)
        #print(f'{result=}') # (1, '1.png', 1, 'Traveler', 'Travel to some outstanding place')
        current_image = path + result["icon"]
        
    if request.method == "GET":
        edit_achievement_form.name.data = result["name"]
        edit_achievement_form.desc.data = result["description"]
        
        return render_template("edit_achievement.html",edit_achievement_form=edit_achievement_form, path=path, message=message, achievement_id=achievement_id, current_image=current_image, delete_form=delete_form)
    if edit_achievement_form.validate_on_submit():
        
        name = edit_achievement_form.name.data
        desc = edit_achievement_form.desc.data
        print(f'{name=} {desc=}')
        if edit_achievement_form.image.data:
            old_image = current_image
            
            if os.path.exists(old_image[3:]):
                os.remove(old_image[3:])
            else:
                message = f'{old_image[3:]=} Cannot remove'
            image = edit_achievement_form.image.data
            image_name = secure_filename(image.filename)
            image_extention = os.path.splitext(image_name)[1]
            image_name = f'{achievement_id}{image_extention}'
            image.save(f'{path[3:]}{image_name}')
        else:
            image_name = False
        with Database(dict_cursor=True) as db:
            achievement = Achievement(db)
            achievement.update(achievement_id,name,desc,image_name)
        message = "Succsessfully updated achievement!"
        flash(message)
        return render_template("edit_achievement.html",edit_achievement_form=edit_achievement_form, path=path, message=message, achievement_id=achievement_id, current_image=current_image, delete_form=delete_form)
    if delete_form.submit_delete.data:
        print("DELETE PRESSED!")
        delete_id = delete_form.id.data
        with Database(dict_cursor=True) as db:
            try:
                db.queryOne("DELETE FROM `achievement` WHERE `achievement`.`id` = %s",(delete_id,))
                if os.path.exists(current_image[3:]) and result["icon"] !=   "default.png":
                    os.remove(current_image[3:])
                else:
                    message = f'{current_image[3:]=} Cannot remove'
            except Exception as e:
                print(f'Error {e}')
        return redirect(url_for("admin.achievements_page")) 
        
    else:
        return "invalid form"
        
@admin.route("/achievements/add", methods=["GET","POST"])
@login_required
def achievement_add():
    path = path = f"{current_app.config['ACHIEVEMENTS_FOLDER']}"
    achievement_add_form = Edit_acheivements()
    default_image = path + "default.png"
    
    if request.method == "GET":
        return render_template("add_achievement.html", achievement_add_form=achievement_add_form, default_image=default_image)
    if achievement_add_form.validate_on_submit():
        with Database(dict_cursor=True) as db:
            db.query("INSERT INTO `achievement` (`id`, `icon`) VALUES (NULL, 'default.png')")
            result = db.queryOne("SELECT id FROM `achievement` WHERE icon = 'default.png' ORDER BY id DESC LIMIT 1;")
            print(f'after added default! {result=}')
            achievement_id = result["id"]
            name = achievement_add_form.name.data
            desc = achievement_add_form.desc.data
            db.queryOne("INSERT INTO `achievement_meta` (`achievement_id`, `language_id`, `name`, `description`) VALUES (%s, '1', %s, %s)",(achievement_id,name,desc,))
            
        if achievement_add_form.image.data:
            image = achievement_add_form.image.data
            image_name = secure_filename(image.filename)
            image_extention = os.path.splitext(image_name)[1]
            image_name = f"{achievement_id}{image_extention}"
            with Database() as db:
                try:
                    db.queryOne("UPDATE `achievement` SET `icon` = %s WHERE `achievement`.`id` = %s",(image_name,achievement_id,))
                except:
                    return "Failed to insert into DB"
                image.save(path[3:]+image_name)
        else:
            image_name = "default.png"
        return redirect(url_for("admin.achievements_page")) 

    


@admin.route("/sight-types", methods=["GET", "POST"])
@login_required 
def sight_types():

    
    with Database() as db:
        obj = SightType(db)
        success, message, sight_types = obj.get_sight_types(1)
        
    if request.method == "GET":
        
        return render_template("sight_types.html", sight_types=sight_types)
    


@admin.route("/add-sight-type", methods=["GET", "POST"])
@login_required 
def add_sight_type():
    add_sight_type_form = EditOrAddSightType()
    
    if request.method == "GET":
        return render_template("add_sight_type.html", add_sight_type_form=add_sight_type_form)
    
    if add_sight_type_form.validate_on_submit():
        name = add_sight_type_form.name.data
        description = add_sight_type_form.desc.data
        points = add_sight_type_form.points.data

        with Database(dict_cursor=True) as db:
            sight_type = SightType(db)
            sight_type.add_sight_type(name, description, points)

        
        flash("Successfully added sight type")
        return render_template("add_sight_type.html", add_sight_type_form=add_sight_type_form)

    else:
        return flash("Invalid form")



@admin.route("/sight-types/edit/<int:sight_type_id>", methods=["GET", "POST"])
@login_required 
def edit_sight_type(sight_type_id):
    edit_sight_type_form = EditOrAddSightType()
    with Database(dict_cursor=True) as db:
        sight_type = SightType(db)
        sight_data = sight_type.get_sight_type_data(sight_type_id)
        

    if request.method == "GET":
        edit_sight_type_form.name.data = sight_data["name"]
        edit_sight_type_form.desc.data = sight_data["description"]
        edit_sight_type_form.points.data = sight_data["points"]
        
        return render_template("edit_sight_type.html", edit_sight_type_form=edit_sight_type_form, sight_type_id=sight_type_id)
    
    if edit_sight_type_form.validate_on_submit():
        name = edit_sight_type_form.name.data
        description = edit_sight_type_form.desc.data
        points = edit_sight_type_form.points.data

        with Database(dict_cursor=True) as db:
            sight_type = SightType(db)
            sight_type.update(sight_type_id, name, description, points)

        
        flash("Successfully edited sight type")
        return render_template("edit_sight_type.html", edit_sight_type_form=edit_sight_type_form, sight_type_id=sight_type_id)

    else:
        return flash("Invalid form")



@admin.route("/sight-types/delete/<int:sight_type_id>", methods=["POST"])
@login_required 
def delete_sight_type(sight_type_id):
    if request.method == "GET":
        return redirect(url_for('admin.sight_types'))
    
    else:
        with Database(dict_cursor=True) as db:
            sight_type = SightType(db)
            sight_type.delete_sight_type(sight_type_id)

        return redirect(url_for('admin.sight_types'))      

def fix_image_filename(images,sight_id):
    image_names = []
    path = f"{current_app.config['SIGHT_IMAGE_FOLDER']}/{sight_id}"
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

def sort_dropdown_by_id_cat(id,options):
    new = []
    options.pop(0)
    selected = options.pop(id-1)
    new.append(selected)
    for option in options:
        new.append(option)
    return new

@admin.route("/update_image_order/<int:sight_id>", methods=["POST"])
@login_required 
def update_image_order(sight_id):
    image_names = request.form['image_order'].strip()
    image_names = image_names.split(',')
    print(f'{image_names=}')

    with Database(dict_cursor=True) as db:
        sight = Sight(db)
        lst = sight.get_image_ids(sight_id)

    Update_needed = False
    number_of_images = len(image_names)
    number_of_rows = len(lst)

    if number_of_rows != number_of_images:
        return redirect(url_for("admin.edit_sight" , sight_id=sight_id))

    for i in range(len(lst)):
        if lst[i]['photo'] != image_names[i]:
            Update_needed = True
            break

    if Update_needed:
        ids = []
        for i in range(len(lst)):
            ids.append(lst[i]["id"])
        
        with Database(dict_cursor=True) as db:
            sight = Sight(db)
            sight.update_image_order(ids, sight_id, image_names)
        flash('Updated image order')

    return redirect(url_for("admin.edit_sight" , sight_id=sight_id))

#Delete images 
@admin.route("/<int:sight_id>/delete_image/<path:image_path>", methods=["POST"])
@login_required
def delete_image(sight_id, image_path):
    with Database(dict_cursor=True) as db:
        sight = Sight(db)
        result, message = sight.delete_sight_image(image_path)

    flash(message)
    print(f'{message=}')

    image_path = os.path.join(current_app.config['SIGHT_IMAGE_FOLDER'], image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
        print("Deleted", image_path)
    else:
        print(f'{image_path=} does not exist!')

    return redirect(url_for("admin.edit_sight" , sight_id=sight_id))

#Make admin not accessible to normal users and guest
@admin.before_request
def check_admin():
    if current_user.is_authenticated:
        if current_user.check_if_user_is_admin() == False:
            return redirect(url_for("index"))




def get_achievement_in_sight(sight_id):
    if sight_id == None:
        return []
    with Database(dict_cursor=True) as db:
        try:
            result = db.query("SELECT `achievement_id` FROM `sight_has_achievement` WHERE `sight_id`= %s",(sight_id,))
        except:
            return []
    a_ids = []
    if result == None:
        return a_ids
    for item in result:
        a_ids.append(item["achievement_id"])
    return a_ids

def populate_form(sight_id):
    in_sight = get_achievement_in_sight(sight_id)
    
    with Database(dict_cursor=True) as db:
        all_achievements = Achievement(db).getAchievements()
        
        all_achievements = list(all_achievements)
        all_achievements.pop(0)
        all_achievements.pop(0)
        all_achievements = all_achievements[0]
        
        for item in all_achievements:
            if item["id"] in in_sight:
                item["selected"] = True
            else:
                item["selected"] = False
        simple_info = []
        for item in all_achievements:
            simple_info.append((item["selected"],[item["id"],item["name"]]))
            
        return simple_info
