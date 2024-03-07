from flask import Blueprint, render_template

from database import  Database
from models.sight import Sight


sight = Blueprint("sight", __name__, template_folder="templates", static_folder="static")


@sight.route("/sights")
def sights():



    # sights=[
    #         {'name': 'Eiffel Tower'},
    #         {'name': 'Statue of Liberty'},
    #         {'name': 'Great Wall of China'},
    #         {'name': 'Taj Mahal'},
    #         {'name': 'Pyramids of Giza'},
    #         {'name': 'Colosseum'},
    #         {'name': 'Machu Picchu'},
    #         {'name': 'Stonehenge'},
    #         {'name': 'Petra'},
    #         {'name': 'Chichen Itza'},
    #         {'name': 'Christ the Redeemer'},
    #         {'name': 'Angkor Wat'},
    #         {'name': 'Sydney Opera House'},
    #         {'name': 'Golden Gate Bridge'},
    #         {'name': 'Sagrada Familia'},
    #         {'name': 'Neuschwanstein Castle'},
    #         {'name': 'Acropolis of Athens'},
    #         {'name': 'Burj Khalifa'},
    #         {'name': 'Mount Rushmore'},
    #         {'name': 'St. Basil’s Cathedral'},
    #         {'name': 'Alhambra'},
    #         {'name': 'Borobudur'},
    #         {'name': 'Easter Island'},
    #         {'name': 'Potala Palace'},
    #         {'name': 'Chateau de Chambord'},
    #         {'name': 'Chateau de Versailles'},
    #         {'name': 'Chateau de Chenonceau'},
    #         {'name': 'Chateau de Chantilly'},
    #         {'name': 'Chateau de Fontainebleau'},
    #         {'name': 'Chateau de Vaux-le-Vicomte'},
    #         {'name': 'Chateau de Pierrefonds'},
    #         {'name': 'Chateau de Compiègne'},
    #         {'name': 'Chateau de Rambouillet'},
    #         {'name': 'Chateau de Malmaison'},
    #         {'name': 'Chateau de Maisons-Laffitte'},
    #         {'name': 'Chateau de Saint-Germain-en-Laye'},
    #         {'name': 'Chateau de Sceaux'},
    #         {'name': 'Chateau de Dampierre'},
    #         {'name': 'Chateau de Breteuil'},
    #         {'name': 'Chateau de Courson'},
    #         {'name': 'Chateau de Thoiry'},
    #         {'name': 'Chateau de Champs-sur-Marne'},
    #         {'name': 'Chateau de La Ferté-Vidame'},
    #         {'name': 'Chateau de La Roche-Guyon'},
    #         {'name': 'Chateau de La Motte-Tilly'},
    #         {'name': 'Chateau de La Ferté-Milon'},
    #         {'name': 'Chateau de La Ferté-Alais'},
    #         {'name': 'Chateau de La Chapelle-Godefroy'},
    #         {'name': 'Chateau de La Chapelle-Rablais'},
    #         {'name': 'Chateau de La Chapelle-Moutils'},
    #         {'name': 'Chateau de La Chapelle-Gauthier'},
    #         {'name': 'Chateau de La Chapelle-Anthenaise'},
    #         {'name': 'Chateau de La Chapelle-Aubareil'},
    #         {'name': 'Chateau de La Chapelle-Blanche-Saint-Martin'},
    #         {'name': 'Chateau de La Chapelle-Bâton'},
    #         {'name': 'Chateau de La Chapelle-Baloue'},
    #         {'name': 'Chateau de La Chapelle-Aux-Choux'},
    #         {'name': 'Chateau de La Chapelle-Aubareil'},
    #         {'name': 'Chateau de La Chapelle-Blanche-Saint-Martin'},
    #         {'name': 'Chateau de La Chapelle-Bâton'},
    # ]

    with Database(dict_cursor=True) as db:
        
        sight_model = Sight(db)

        sights = sight_model.getAllSights()

    print(sights)

    return render_template(
        "sight/sights.html",
        sights=sights
    )
