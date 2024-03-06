from flask import Blueprint, render_template


sight = Blueprint("sight", __name__, template_folder="templates", static_folder="static")


@sight.route("/sights")
def sights():

    return render_template(
        "sight/sights.html",
        sights=[
            {'name': 'Eiffel Tower'},
            {'name': 'Statue of Liberty'},
            {'name': 'Great Wall of China'},
            {'name': 'Taj Mahal'},
            {'name': 'Pyramids of Giza'},
            {'name': 'Colosseum'},
            {'name': 'Machu Picchu'},
            {'name': 'Stonehenge'},
            {'name': 'Petra'},
            {'name': 'Chichen Itza'}
        ]
    )
