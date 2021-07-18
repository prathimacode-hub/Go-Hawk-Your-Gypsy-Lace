from flask_sqlalchemy import SQLAlchemy

# Instantiate a SQLAlchemy object
db = SQLAlchemy()

class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    staff_user = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a user"""

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>"

class Map(db.Model):
    """Data model for a map."""

    __tablename__ = "maps"

    map_id = db.Column(db.Integer, 
                        primary_key=True,   
                        autoincrement=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    map_name = db.Column(db.String(50), nullable=False)
    map_description = db.Column(db.String(100), nullable=True)
    map_url_hash = db.Column(db.String(32), nullable=False)

    #***********
    user = db.relationship("User", backref="maps")
    place = db.relationship("Place", backref="maps")
    #***********

    def __repr__(self):
        """Return a human-readable representation of a map"""

        return f"<Map map_id={self.map_id} user_id={self.user_id} map_name={self.map_name}>"


class Place(db.Model):
    """Data model for a place."""

    __tablename__ = "places"

    place_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    map_id = db.Column(db.Integer, 
                        db.ForeignKey('maps.map_id'))
    google_place_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    place_types = db.Column(db.String(100), nullable=False)
    google_places_id = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    user_notes = db.Column(db.String(300), nullable=False)
    place_active = db.Column(db.Boolean, default=True, nullable=False)
    

    def __repr__(self):
        """Return a human-readable representation of a place"""

        return f"<Place place_id={self.place_id} map_id={self.map_id} google_place_name={self.google_place_name} address={self.address} website={self.website} place_types={self.place_types} google_places_id={self.google_places_id} latitude={self.latitude} longitude={self.longitude} user_notes={self.user_notes} place_active={self.place_active}>"


def example_data():
    """Create some example data"""
    
    #Example users
    Prathima = User(fname="prathima", lname="k", email="prathimak569@gmail.com", password="Kprathima@88", staff_user=True)
    Chandu = User(fname="Moon", lname="Light", email="Moonlight994844@gmail.com", password="Nightowl44")

    #Example maps
    map1 = Map(user=gwen, map_name="Hyderabad", map_description="Hyderabad activities", map_url_hash="0c38abd239da4782b1510e57d0eb49d")
    map2 = Map(user=jesse, map_name="Hyderabad", map_description="Hyderabad activities", map_url_hash="e514f0af375b4343930437cbba9793c3")
    
    #Example places
    place1 = Place(maps=map1, 
                    google_place_name="Golconda Fort", 
                    address="Khair Complex, Ibrahim Bagh, Hyderabad, Telangana 500008", 
                    website="https://www.telanganatourism.gov.in/partials/destinations/heritage-spots/hyderabad/golconda-fort.html", 
                    place_types="bar,point_of_interest,establishment", 
                    google_places_id="ChIJC5_zVw-HhYARet1rQr-DRl0", 
                    latitude="17.3850", 
                    longitude="78.4867", 
                    user_notes="Very ancient fort in city of hyderabad, which recollects the history of Nizams rule.", 
                    place_active=True)
    place2 = Place(maps=map1, 
                    google_place_name="Hussain Sagar Lake", 
                    address=" Tank Bund Rd, Hyderabad, Telangana, 500004, India", 
                    website="https://www.hyderabadtourism.travel/hussain-sagar-lake-hyderabad", 
                    place_types="tourist_attraction,point_of_interest,establishment", 
                    google_places_id="ChIJszBPbLWHhYARfrlLxEb3GuA", 
                    latitude="17.3850", 
                    longitude="78.4867", 
                    user_notes="An amazing lake in form of necklace and best place to hang out in evenings", 
                    place_active=True)
    db.session.add_all([Prathima, Chandu, map1, map2, place1, place2])
    db.session.commit()
    

def connect_to_db(app, db_uri="postgresql:///Go Hawk Your Gypsy Lace"):
    """Connect the database to the Flask app"""

    # Configure to use the database.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
