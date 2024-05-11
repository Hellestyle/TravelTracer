from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from forms import Filter_by_category, get_categories

from database import  Database
from models.sight import Sight
from models.sight_type import SightType
from models.sight_name import SightName
from models.wishlist import Wishlist
from models.visited_list import VisitedList

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
        context = db.query("SELECT `sight_type_id`,`name` FROM `sight_type_meta` WHERE `language_id`= 1 ORDER BY sight_type_id")
        
    print(f'{context=}')

    Filter_by_category = [x["name"] for x in context]
    print(f'{Filter_by_category=}')

    """
    filter_by_category = Filter_by_category()
    if request.method == "GET":
        filter_by_category.sight_type.choices = get_categories()
        if filter_by_category.validate():
            filter_by_category = filter_by_category """
    with Database(dict_cursor=True) as db:
        
        sight_model = Sight(db)
        sights = sight_model.getAllSights()
        statistics = sight_model.get_all_sight_statistics()

        sight_type_model = SightType(db)
        sight_types = sight_type_model.getAllSightTypes()

        sight_name_model = SightName(db)
        sight_names = sight_name_model.getAllSightNames()
    
    admin = False
    if current_user.is_authenticated:
        user = current_user
        admin = True if user.check_if_user_is_admin() else False

        result, message, user_wishlist, user_visited_list =  user.get_user_wishlist_and_visited_list()
        if result:
            return render_template(
                "sight/sights.html",
                sights=sights,
                filter_by_category = filter_by_category,
                sight_type_names=[sight_type["name"] for sight_type in sight_types],
                sight_names = [sight_name["name"] for sight_name in sight_names],
                admin=admin, user_wishlist=user_wishlist, user_visited_list=user_visited_list,
                statistics=statistics
            )
        else:
            return render_template(
                "sight/sights.html",
                filter_by_category = filter_by_category,
                sights=sights,
                sight_type_names=[sight_type["name"] for sight_type in sight_types],
                sight_names = [sight_name["name"] for sight_name in sight_names],
                admin=admin, message=message, user_wishlist=None, user_visited_list=None,
                statistics=statistics
            )
    else:
        return render_template(
            "sight/sights.html",
            filter_by_category = filter_by_category,
            sights=sights,
            sight_type_names=[sight_type["name"] for sight_type in sight_types],
            sight_names = [sight_name["name"] for sight_name in sight_names],
            admin=admin, statistics=statistics
        )


@sight.route("/sight/id/<int:sight_id>")
def sight_details(sight_id):
    admin = False
    if current_user.is_authenticated:
        user = current_user
        admin = True if user.check_if_user_is_admin() else False
    
    with Database(dict_cursor=True) as db:

        sight_model = Sight(db)
        wishlist_model = Wishlist(db)
        visited_list_model = VisitedList(db)

        sight = sight_model.getSight(sight_id)
        sight_statistic = sight_model.get_a_single_sight_statistic(sight_id)

        in_wishlist = wishlist_model.sightInWishlist(sight_id, current_user.get_id()) if current_user.is_authenticated else None

        in_visited_list = visited_list_model.sightInVisitedList(sight_id, current_user.get_id()) if current_user.is_authenticated else None

    if sight is not None:
        now = dt.now().time()

        is_open = sight["open_time"] is None and sight["close_time"] is None or \
            sight["open_time"] <= now and sight["close_time"] >= now

        images = [url_for('static', filename=f"images/sight/{sight_photo}") for sight_photo in sight["photos"]]

        return render_template(
            "sight/sight.html",
            sight=sight, images=json.dumps(images),
            is_open=is_open,
            in_wishlist=in_wishlist,
            in_visited_list=in_visited_list,
            admin=admin, sight_statistic=sight_statistic
        )
    else:
        message = "No sights found"
        return render_template("sight/sights.html", message=message)
    
# Handling everything search related:
@sight.route("/sight/<string:age>/<string:user_input>", methods=["GET", "POST"])
def sight_by_everything(age, user_input):

    filter_by_category = Filter_by_category()
    
    filter_by_category.sight_type.choices = get_categories()
    if filter_by_category.validate():
        filter_by_category = filter_by_category
        


    
    age_options = {
        "children": 1,
        "family_friendly": 2,
        "teenagers": 3,
        "young_adults": 4,
        "adults": 5,
        "seniors": 6
    }
    age_id = age_options[age]

    admin = False
    if current_user.is_authenticated:
        user = current_user
        admin = True if user.check_if_user_is_admin() else False
    

    with Database(dict_cursor=True) as db:
        sight_model = Sight(db)
        sights = sight_model.getAllSights()
        #sight_category_id = sight_model.getSight()
        sight_category_id = filter_by_category.sight_type.data

        print(f'{sight_category_id=}')
        sight_type_meta = SightType(db)
        sight_types = sight_type_meta.getAllSightTypes()

        sight_name_model = SightName(db)
        sight_names = sight_name_model.getAllSightNames()

        # Check if sight exist
        sight_id = None
        for sight in sights:
            if user_input.lower() == sight['name'].lower():
                sight_id = sight['id']
                break
        
        if sight_id is not None:
            sight_found = True
            return redirect(url_for("sight.sight_details", sight_id=sight_id))
        else:
            sight_found = False
        
        # Check if empty
        if age_id == 2:
            age_selected = False
        else:
            age_selected = True
        if sight_category_id == 0:
            category_selected = False
        else:
            category_selected = True
        
        # Return to all sights if no filter is chosen
        if age_selected == False and category_selected == False and user_input is None:
            return render_template("sight/sights.html", sights=sights,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input, admin=admin
                                )
        
        # Make list of all results of selected filters
        else:
            age_filter_result = [sight for sight in sights if sight["age_id"] == age_id]
            category_filter_result = [sight for sight in sights if sight_category_id["sight_type_id"] == category]
            complete_filter_result = [sight for sight in sights if sight["age_id"] == age_id and sight_category_id["sight_type_id"] == category]

        # Return end results
        if age_selected == True and category_selected == True and user_input is None:
            if not complete_filter_result:
                    message = "No sights found with the filters you have choosen"
                    return render_template("sight/sights.html", message=message,
                                        filter_by_category = filter_by_category,
                                        sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                        sight_names = [sight_name["name"] for sight_name in sight_names],
                                        user_input=user_input, admin=admin
                                    )
            else:
                return render_template("sight/sights.html", sights=complete_filter_result,
                                filter_by_category = filter_by_category,
                                sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                sight_names = [sight_name["name"] for sight_name in sight_names],
                                user_input=user_input, admin=admin
                            )
        if age_selected == True and category_selected == False and user_input is None:
            if not age_filter_result:
                message = "No sights found with the age filter you have choosen"
                return render_template("sight/sights.html", message=message,
                                    filter_by_category = filter_by_category,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input, admin=admin
                                )
            else:   
                render_template("sight/sights.html", sights=age_filter_result,
                                filter_by_category = filter_by_category,
                                sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                sight_names = [sight_name["name"] for sight_name in sight_names],
                                user_input=user_input, admin=admin
                            )
        if category_selected == True and age_selected == False and user_input is None:
            if not category_filter_result:
                message = "No sights found with the category filter you have choosen"
                return render_template("sight/sights.html", message=message,
                                    filter_by_category = filter_by_category,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input, admin=admin
                                )
            else:   
                render_template("sight/sights.html", sights=category_filter_result,
                                filter_by_category = filter_by_category,
                                sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                sight_names = [sight_name["name"] for sight_name in sight_names],
                                user_input=user_input, admin=admin
                            )
        if sight_found == False and category_selected == False and age_selected == False:
            message = "No sights with that name"
            return render_template("sight/sights.html", message=message,
                                    filter_by_category = filter_by_category,
                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
                                    sight_names = [sight_name["name"] for sight_name in sight_names],
                                    user_input=user_input, admin=admin
                                )
    

## Handling cases where the inputbox is not empty and the age is selected
#@sight.route("/sight/<string:category>/<string:age>")
#def sight_by_category(category, age):
#    user_input = category
#
#    age_categories = {
#        "children": 1,
#        "family_friendly": 2,
#        "teenagers": 3,
#        "young_adults": 4,
#        "adults": 5,
#        "seniors": 6
#    }
#    age_category_id = age_categories[age]
#
#    admin = False
#    if current_user.is_authenticated:
#        user = current_user
#        admin = True if user.check_if_user_is_admin() else False
#
#    with Database(dict_cursor=True) as db:
#        sight_model = Sight(db)
#        sights = sight_model.getSightByCategory(category)
#
#        sight_type_meta = SightType(db)
#        sight_types = sight_type_meta.getAllSightTypes()
#
#        sight_name_model = SightName(db)
#        sight_names = sight_name_model.getAllSightNames()
#
#        if sights is not None:
#            # We need to check the value of "age" parameter
#            # If it's "all" by default (it means age == "family_friendly"), just return the sights
#            if age_category_id == 2:
#                return render_template("sight/sights.html", sights=sights,
#                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
#                                    sight_names = [sight_name["name"] for sight_name in sight_names],
#                                    user_input=user_input, admin=admin
#                                )    
#            # If it's not "all", we need to filter the sights by age
#            else:
#                filtered_sights = [sight for sight in sights if sight["age_id"] == age_category_id]
#                
#                if not filtered_sights:
#                    message = "No sights found"
#                    return render_template("sight/sights.html", message=message,
#                                        sight_type_names=[sight_type["name"] for sight_type in sight_types],
#                                        sight_names = [sight_name["name"] for sight_name in sight_names],
#                                        user_input=user_input, admin=admin
#                                    )
#                else:
#                    return render_template("sight/sights.html", sights=filtered_sights,
#                                    sight_type_names=[sight_type["name"] for sight_type in sight_types],
#                                    sight_names = [sight_name["name"] for sight_name in sight_names],
#                                    user_input=user_input, admin=admin
#                                )
#
#        # Check if the "category" parameter matches any sight name
#        # If it does, redirect to the sight details page
#        else:
#            sight_model = Sight(db)
#            sights = sight_model.getAllSights()
#
#            sight_id = None
#            for sight in sights:
#                if category.lower() == sight['name'].lower():
#                    sight_id = sight['id']
#                    break
#            
#            if sight_id is not None:
#                return redirect(url_for("sight.sight_details", sight_id=sight_id))
#            else:
#                message = "No sights found"
#                return render_template("sight/sights.html", message=message,
#                                       sight_type_names=[sight_type["name"] for sight_type in sight_types],
#                                       sight_names = [sight_name["name"] for sight_name in sight_names],
#                                       user_input=user_input, admin=admin
#                                    )
#
#
## Handling cases where the inputbox is empty but the age is selected
#@sight.route("/sight/<string:age>")
#def sight_by_age(age):
#    age_categories = {
#        "children": 1,
#        "family_friendly": 2,
#        "teenagers": 3,
#        "young_adults": 4,
#        "adults": 5,
#        "seniors": 6
#    }
#    
#    admin = False
#    if current_user.is_authenticated:
#        user = current_user
#        admin = True if user.check_if_user_is_admin() else False
#
#    if age == "family_friendly":
#        return redirect(url_for("sight.sights"))
#
#    else:
#        age_category_id = age_categories[age]
#        with Database(dict_cursor=True) as db:
#            sight_model = Sight(db)
#            sights = sight_model.getSightByAge(age_category_id)
#
#            sight_name_model = SightName(db)
#            sight_names = sight_name_model.getAllSightNames()
#
#            sight_type_meta = SightType(db)
#            sight_types = sight_type_meta.getAllSightTypes()
#            
#            return render_template("sight/sights.html",
#                                sights=sights, 
#                                sight_names = [sight_name["name"] for sight_name in sight_names], 
#                                sight_type_names=[sight_type["name"] for sight_type in sight_types],
#                                admin=admin
#                            )


@sight.route("/wishlist/add/<int:sight_id>")
@login_required
def add_to_wishlist(sight_id):

    next_page = request.args.get("next", url_for("sight.sight_details", sight_id=sight_id))

    with Database(dict_cursor=True) as db:

        wishlist_model = Wishlist(db)

        success, message = wishlist_model.addSightToWishlist(sight_id, current_user.get_id())

    if not success:
        flash(message)
    
    return redirect(next_page)


@sight.route("/wishlist/remove/<int:sight_id>")
@login_required
def remove_from_wishlist(sight_id):

    next_page = request.args.get("next", url_for("sight.sight_details", sight_id=sight_id))

    with Database(dict_cursor=True) as db:

        wishlist_model = Wishlist(db)

        success, message = wishlist_model.removeSightFromWishlist(sight_id, current_user.get_id())

    if not success:
        flash(message)
    
    return redirect(next_page)


@sight.route("/visited-list/add/<int:sight_id>")
@login_required
def add_to_visited_list(sight_id):

    liked = request.args.get("liked", None)

    next_page = request.args.get("next", url_for("sight.sight_details", sight_id=sight_id))

    if liked is not None:
        liked = bool(int(liked))

    with Database(dict_cursor=True) as db:

        visited_list_model = VisitedList(db)

        success, message = visited_list_model.addSightToVisitedList(sight_id, current_user.get_id(), liked)

    if not success:
        flash(message)
    
    return redirect(next_page)
