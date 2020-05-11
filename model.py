"""Data model classes for a crime database
"""
"""drobdb crimesData
createdb crimeData
go to python file $python3 -i <filename>
db.create_all()

in a new tab:
psql <filename>
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    """Data model for a category."""

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)
    count_crime = db.Column(db.Integer, nullable=False)
    label = db.Column(db.Integer)
    
    crimes = db.relationship('Crime', backref='category')

    def __repr__(self):
        """printing the category table as a string."""

        return f'<Category category_id={self.category_id} category_name={self.category_name}\
                    count_crime ={self.count_crime} label = {self.label}>'

class Neighborhood(db.Model):
    """Data model for a neighborhood."""

    __tablename__ = 'neighborhoods'

    neigh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    neigh_name = db.Column(db.String(50))
    neigh_latitude = db.Column(db.Float)
    neigh_longitude = db.Column(db.Float)
    zipcode = db.Column(db.Integer)
    score = db.Column(db.Integer)
    count_crime = db.Column(db.Integer, nullable = False)

    crimes = db.relationship('Crime', backref='neighborhood')


    def get_crimes_by_category(self):
        """Return a dictionary of crime categories and sum of crimes.

        Example:

            {'Larceny Theft': 1000}
        """

        result = {}
        for crime in self.crimes:
            cat_name = crime.category.category_name
            if cat_name in result:
                result[cat_name] += 1
            else:
                result[cat_name] = 1
        return result

    def get_coordinates_by_category(self):
        """Return a dictionary of crime categories and list of coordinates.

        Example:

            {'Larceny Theft': [(33.3333,-122,9000),()]}
        """

        result = {}
        for crime in self.crimes:
            cat_name = crime.category.category_name.strip()
            if cat_name in result:
                result[cat_name].append((crime.latitude, crime.longitude))
            else:
                result[cat_name] = [(crime.latitude, crime.longitude)]
        return result


    def __repr__(self):
        """for printing."""

        return f'<Neighborhood neigh_id={self.neigh_id} neigh_name={self.neigh_name}\
                    neigh_latitude={self.neigh_latitude} neigh_longitude={self.neigh_longitude} score={self.score}\
                    zipcode={self.zipcode} \
                    count_crime={self.count_crime}>'


class Resolution(db.Model):
    """Data model for a resolution."""

    __tablename__ = 'resolutions'

    resolution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resolution_name = db.Column(db.String(100))
    count_crime = db.Column(db.Integer, nullable = False)

    crimes = db.relationship('Crime', backref='resolution')


    def __repr__(self):
        """for printing."""

        return f'<Resolution resolution_id={self.resolution_id} resolution_name={self.resolution_name}\
                    neigh_latitude={self.neigh_latitude} neigh_longitude={self.neigh_longitude}\
                     description={self.discription} count_crime={self.count_crime}>'


class Subcategory(db.Model):
    """Data model for a resolution."""

    __tablename__ = 'subcategories'

    subcategory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    subcategory_name = db.Column(db.String(100))
    count_crime = db.Column(db.Integer, nullable = False)

    crimes = db.relationship('Crime', backref='subcategory')


    def __repr__(self):
        """for printing."""

        return f'<Resolution resolution_id={self.resolution_id} resolution_name={self.resolution_name}\
                    neigh_latitude={self.neigh_latitude} neigh_longitude={self.neigh_longitude}\
                     description={self.discription} count_crime={self.count_crime}>'


class Crime(db.Model):
    """Data model for a crime."""

    __tablename__ = 'crimes'

    crime_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # crime_name = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.subcategory_id'))
    resolution_id = db.Column(db.Integer, db.ForeignKey('resolutions.resolution_id'))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neigh_id'))
    crime_date = db.Column(db.String(50))
    crime_time = db.Column(db.String(50))
    crime_day = db.Column(db.String(50))
    intersection = db.Column(db.String(100))
    police_district = db.Column(db.String(100))
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    label = db.Column(db.Integer)


    def __repr__(self):
        """for printing."""

        return f'<Crime crime_id={self.crime_id} crime_date={self.crime_date}\
                    crime_time={self.crime_time} crime_day={self.crime_day}\
                    police_district={self.police_district} intersection={self.intersection}\
                    latitude={self.latitude} longitude={self.longitude} label={self.label}>'


class User(db.Model):
    """Data model for a user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    phone_num=db.Column(db.String(100))
    # phone_number=bd.Column(db.Integer)


    

    def __repr__(self):
        """printing the user table as a string."""

        return f'<User user_id={self.user_id} name={self.name}\
                email ={self.email} user_password={self.password} phone_num={self.phone_num}>'


class Route(db.Model):
    """Data model for a route"""

    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    route_name = db.Column(db.String(50))
    route_start = db.Column(db.String(100))
    route_end = db.Column(db.String(100))
    score = db.Column(db.Float)
    
    user = db.relationship('User', backref='routes')
    neighborhoods = db.relationship('Neighborhood',
                                    secondary='routeneighs',
                                    backref='routes')

    def to_dict(self):
        return {"route_id":self.route_id,
                "user_id": self.user_id,
                "route_name": self.route_name,
                "route_start": self.route_start,
                "route_end": self.route_end,
                "score": self.score}

    def makeDic(self):
        """make a dictionary of a route"""

        return {"route_id":self.route_id,
                "user_id": self.user_id,
                "route_name": self.route_name,
                "route_start": self.route_start,
                "route_end": self.route_end,
                "score": self.score}

    def get_route_id(self):
        """return the route id"""

        return self.route_id


    def __repr__(self):
        """for printing."""

        return f'<route_id={self.route_id} route_name={self.route_name}\
                    route_start={self.route_start}\
                    route_end={self.route_end} \
                    score={self.score}>'



class RouteNeigh(db.Model):
    """Data model for a route"""

    __tablename__ = 'routeneighs'

    route_neigh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'))
    neigh_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neigh_id'))


    def __repr__(self):
        """for printing."""

        return f'<route_id={self.route_id} neigh_id={self.neigh_id}>'



def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///crimeData'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    



if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print('Connected to db!')
    db.create_all()
