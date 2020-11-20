"""SafeWalk."""

from os import environ
import sys
import numpy as np
import pandas as pd
import random
import re 
from jinja2 import StrictUndefined
from flask import Flask, flash, render_template, jsonify, send_from_directory, request, request_finished, make_response,  flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import json
from model import db, Crime, Category, Resolution, Neighborhood, Subcategory, User, Route, connect_to_db
from sqlalchemy import func, update
from threading import Timer
import requests
import urllib.parse
import urllib.request
from twilio.rest import Client
from shapely.geometry import Point, Polygon
from pyshorteners import Shortener 

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined

def checkuser():
    """check if the user if logged in already"""
    
    user_id = session.get("user_id") 

    if(user_id!=None):
        logged_user=User.query.filter_by(user_id=user_id).first()
    else:
        logged_user="None"

    return logged_user


def checkPolygon(poly, p):
    """check polygone"""
    
    point=Point(p)
    polygone = Polygon(poly)

    return point.within(polygone) 


def getScore_neighborhood(avg_crimes):
    """Calculate score for each neighborhood"""
    
    pred_category=0

    if(avg_crimes<0.0001):
        pred_category=0

    if(avg_crimes>=0.0001 and avg_crimes<0.0005):
        pred_category=1

    if(avg_crimes>=0.0005 and avg_crimes<0.001):
        pred_category=2

    if(avg_crimes>=0.001 and avg_crimes<0.005):
        pred_category=3

    if(avg_crimes>=0.005 and avg_crimes<0.01):
        pred_category=4

    if(avg_crimes>=0.01 and avg_crimes<0.02):
        pred_category=5

    if(avg_crimes>=0.02 and avg_crimes<0.03):
        pred_category=6

    if(avg_crimes>=0.03 and avg_crimes<0.05):
        pred_category=7

    if(avg_crimes>=0.05):
        pred_category=8
   
    return pred_category


def password_verif(passwd):
    """verify the password"""
    
    Specialchar ={'$', '@', '#', '%'}
    value = True
      
    if len(passwd) < 6: 
        flash('length of the password should be at least 6') 
        value = False
          
    if len(passwd) > 20: 
        flash('length of the password should be not greater than 20') 
        value = False
          
    if not any(char.isdigit() for char in passwd): 
        flash('Password should have at least one numeral') 
        value = False
          
    if not any(char.isupper() for char in passwd): 
        flash('Password should have at least one uppercase letter') 
        value = False
          
    if not any(char.islower() for char in passwd): 
        flash('Password should have at least one lowercase letter') 
        value = False
          
    if not any(char in Specialchar for char in passwd): 
        flash('Password should have at least one of the symbols $@#') 
        value = False
    if value: 
        return value 


def phone_verif(phone_num):
    """Check if the phone number is valid"""

    value = True
    if phone_num[0:1] == '+':
        for char in phone_num[1:]:
            if not char.isdigit(): 
                flash('Please enter + then a set of digits') 
                value = False
    else:
        flash('Please enter + then a set of digits') 
        value = False
    
    return value


@app.route("/")
def index():
    """Show homepage."""
    
    return render_template("index.html", user=checkuser())


@app.route("/dropmarkers")
def view_crimes_per_neighborhood():
    """Show the map for different categories of crime in the neighborhoods page
    """
    
    api_key=environ.get('API_KEY')

    return render_template("dropmarkers.html", user=checkuser(), api_key=api_key)


@app.route("/mapNeigh")
def view_mapNeigh():
    """Show the map for different neighborhoods in the neighborhoods page
    """
    
    api_key = environ.get('API_KEY')

    return render_template("mapNeigh.html", api_key=api_key)


@app.route("/selectNeigh", methods = ["POST"])
def getNeigh():
    """get the list of neigh in SF"""
    
    neigh_id = request.form.get("neigh_id")
    neigh = Neighborhood.query.filter(Neighborhood.neigh_id == neigh_id).first()
    dic_crimes = neigh.get_coordinates_by_category()

    return jsonify(dic_crimes)


@app.route("/selectcat", methods = ["POST"])
def getcat():
    """get the list of crimes per date and for a given category and neighborhood"""

    neigh_id = request.form.get("neigh_id")
    cat_name = request.form.get("cat_name")
    session["neigh_id"]=neigh_id
    session["cat_name"]=cat_name

    cat = Category.query.filter(Category.category_name == cat_name).first()
    crimes = Crime.query.filter((Crime.neighborhood_id == neigh_id) & (Crime.category_id==cat.category_id)).all()

    xy_dic = {}
    for crime in crimes:
        # 2019/09/30 , 2019/10/02
        date=crime.crime_date
        year=date[:4]
        month=int(date[5:7])

        if year == '2019':
            month = month + 12
        if month in xy_dic:
            xy_dic[month] += 1
        else:
            xy_dic[month] = 1

    return jsonify(xy_dic)


@app.route("/neighClass")
def view_frame_Neigh():
    """show the neighborhoods page and return the list of neighborhoods
    """
    
    logged_user = checkuser()

    list_neigh = []
    neigh = db.session.query(Neighborhood.neigh_id,Neighborhood.neigh_name).all()
    for eachneigh in neigh:
        list_neigh.append({eachneigh[0]:eachneigh[1]})

    return render_template("neighborhood-class.html", user=logged_user, list_neigh=list_neigh)


@app.route("/getNeigh", methods=['POST'])
def get_neigh():
    """show the different neighborhoods on the map, by calculating the score of each one.
    """
    
    data = pd.read_csv("data/SFFind_Neighborhoods.csv") 
    df = pd.DataFrame(data)
    total_rows = len(df.axes[0])
    total_cols = len(df.axes[1])

    json_neigh_coordinates = []
    control = 0

    # count the number of crimes: exp 190644
    total_crimes = db.session.query(Crime).count()
    
    for num_row in range(total_rows):
        dicN = {}
        dic_neigh = {}
        list_coordinates = []
        list_lat = []
        list_lng = []
        poly = []
        geom = data.iloc[num_row]["the_geom"].split(',')
        for index in range(len(geom)):
            # cleaning the data
            if index == 0:
                num_crimes = 0
                coordinates = ((str(geom[index]).strip()).replace('MULTIPOLYGON (((','')).split(" ")
            else:
                coordinates = (str(geom[index]).strip()).split(" ")
            lng = float((coordinates[0]).replace("'",""))
            lat = float(((coordinates[1]).replace("'","")).replace(')',""))
            # { lng: -73.077796936035,  lat: 7.18019914627087 }
            list_coordinates.append({"lng": lng, "lat": lat})
            poly.append((lat,lng))
            
        # calculate the max and the min of the coordinates:
        for c in list_coordinates: 
            list_lat.append(c['lat'])
            list_lng.append(c['lng'])

        dic_neigh["coordinates"] = list_coordinates
        # 'coordinates': [{'lng': -122.45890466499992, 'lat': 37.74053522100007},..]
        dicN[data.iloc[num_row][2]] = dic_neigh
        # [{'Seacliff': {'category':'2','coordinates': [{'lng': -122.49345526799993, 'lat': 37.78351817100008}, {'lng': -122.49372649999992, 'lat': 37.78724665100009}..]}}]
        json_neigh_coordinates.append(dicN)

    return jsonify(json_neigh_coordinates)


@app.route("/direction")
def view_direction():
    """show the direction of the routes.

    - add the directions
    - calculate the safest route
    - Geolocation with HTML5 navigator.geolocate API and direction API
    """

    api_key = environ.get('API_KEY')
    user_id = session.get("user_id")

    if(user_id):
        logged_user = User.query.filter_by(user_id=user_id).first()
        return render_template("direction.html", user=logged_user, api_key=api_key)
    else:
        return render_template("direction.html", user="None", api_key=api_key)

    
@app.route("/coordinates.json")
def showCoordinates():
    """Show the coordinates of the crime on the map"""

    cat_name = session["cat_name"]
    neigh_id = session["neigh_id"]

    list_lat = []
    list_long = []
    infocoordinates = []
    names = []
    cat = Category.query.filter(Category.category_name==cat_name).first()
    crimes = Crime.query.filter((Crime.neighborhood_id==neigh_id) & (Crime.category_id==cat.category_id)).all()
    for eachcrime in crimes:
        infocoordinates.append({"name":eachcrime.subcategory.subcategory_name, "coords":{"lat":eachcrime.latitude, "lng": eachcrime.longitude}, "date": eachcrime.crime_date, "time":eachcrime.crime_time, "intersection":eachcrime.intersection, "day": eachcrime.crime_day})

    del session["cat_name"]
    del session["neigh_id"] 
        
    return jsonify(infocoordinates)


@app.route("/login", methods=['GET'])
def log_in_user():
    """show login page """

    return render_template("adduser.html", user=checkuser())


@app.route('/login', methods=['POST'])
def login_process():
    """Login process"""

    session.clear()
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session.clear()
    session["user_id"] = user.user_id

    return redirect(f"/profile/{user.user_id}")


@app.route("/signin", methods=['GET'])
def add_user():
    """add user"""

    return render_template("signin.html", user="None")

@app.route('/signin', methods=['POST'])
def register_process():
    """Registration process."""

    name = request.form["name"]
    email = "".join((request.form["email"]).split()) 
    password = request.form["password"]
    phone_num = "".join((request.form["pnum"]).split())
    user = User.query.filter_by(email=email).first()

    if not user:
        if name != "":
            if '@' in email:
                password_value = password_verif(password)
                if password_value is True:
                    phone_value = phone_verif(phone_num)
                    if phone_value is True:
                        new_user = User(name=name, email=email, password=password, phone_num=phone_num)
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect("/login")
            else:
                flash("Please enter a valid email")
        else:
            flash("Please enter a valid name")           
    else:
        flash("The user does exist already") 

    return redirect("/signin")    


@app.route('/logout')
def logout():
    """Log out"""

    del session["user_id"]
    session.clear()

    return redirect("/")


@app.route("/profile/<int:user_id>")
def user_detail(user_id):
    """Show info about user.

    the input is the user id 
    the output is the a dictionary that contains, for each traversed neigh in the route
    the different categories of crimes and their sum.
    """

    dic_for_each_route = {}

    user = User.query.options(db.joinedload('routes')).get(user_id)
    query_sum = db.session.query(Crime.category_id, Crime.neighborhood_id, (db.func.count(Crime.crime_id)).label('crime_count')).group_by(Crime.category_id, Crime.neighborhood_id)

    dic_cat_sum = {}
    for eachroute in user.routes:
        list_id = []
        list_neigh = eachroute.neighborhoods
        for eachneigh in list_neigh:
            list_id.append(eachneigh.neigh_id)
        
        query_neigh_cat = query_sum.filter(Crime.neighborhood_id.in_(list_id)).all()

        # group by category the sum of the crimes: now we get the result for each route the crime sum for each categ
        set_cat = set()
        dic_cat = {}
        index = 0
        for line in query_neigh_cat:
            set_cat.add(line.category_id)
        for cat in set_cat:
            sum_cat = 0
            for line in query_neigh_cat:
                if cat == line.category_id:
                    sum_cat += line.crime_count
            name_cat = db.session.query(Category.category_name).filter(Category.category_id == cat).all()
            dic_cat[index] = (name_cat[0][0],sum_cat)
            index += 1

        dic_cat_sum[eachroute] = dic_cat

    return render_template("profile.html", user=user, dic=dic_cat_sum)


@app.route("/chart.json/<int:user_id>")
def route_detail(user_id):
    """Show info about user."""

    dic_for_each_route={}

    user = User.query.options(\
        db.joinedload('routes')\
          .joinedload('neighborhoods')\
          .joinedload('crimes')\
          .joinedload('category')
    ).get(user_id)

    user_routes = []
    for route in user.routes:
        route_json = route.to_dict()
        number_cat = 0

        crimes_sum = {}
        for neighborhood in route.neighborhoods:
            crimes_neighborhood = neighborhood.get_crimes_by_category()
            for crime_cat in crimes_neighborhood:
                if crime_cat in crimes_sum:
                    crimes_sum[crime_cat] += crimes_neighborhood[crime_cat]
                else:
                    crimes_sum[crime_cat] = crimes_neighborhood[crime_cat]
        crimes_sum_sorted = {}
        for key, value in sorted(crimes_sum.items(), reverse=True,  key=lambda x: x[1]):
            crimes_sum_sorted[key]=value
            number_cat += 1
            if number_cat == 8:
                break
        route_json['crimes_by_category'] = crimes_sum_sorted 
        user_routes.append(route_json)

    return jsonify(user_routes)


@app.route('/addRoute', methods = ["POST"])
def post_neighborhood():
    """add a route to the database and return to the profile
    Input: name of the route the start and the end addresses, the score of the best route and the list of
    neighborhoods of that best route.

    Done: store this information in the database route. The list of neigh is stored as a string (text).
        check that that route does not exist.
        if it does not exist then add it to the database 
        add also the neigh_route foe that route. The neigh_route is the link between the route db and the neigh db

    Output: msg
    """

    route_name = request.form.get("name")
    route_start = request.form.get("start_address")
    route_end = request.form.get("end_address")
    score = request.form.get("score")
    list_neigh = request.form.get("list_neigh")
    list_neigh = json.loads(list_neigh)
 
    list_neigh = list(set(list_neigh['neigh']))

    exist_route = Route.query.filter_by( user_id=session.get("user_id"), route_start=route_start, route_end=route_end).first()

    if(exist_route is None):
        new_route = Route(user_id=session.get("user_id"), route_name=route_name, route_start=route_start, route_end=route_end, score=score)
        db.session.add(new_route)
        db.session.commit()
        for n in list_neigh:
            neigh = Neighborhood.query.filter(Neighborhood.neigh_name == n).first()
            if(neigh is not None):
                
                # add the neigh route 
                new_route.neighborhoods.append(neigh)

        db.session.commit()

        return 'The route has been added', 200
    
    return 'The route already exists'


# twilio api 
@app.route("/sendm", methods = ["POST"])
def send_m():
    """Send a message"""

    route_start = request.form.get("start_address")
    route_end = request.form.get("end_address")
    score = request.form.get("score")

    # get the msg
    msg = request.form.get("msg")
    user_id = session.get("user_id")
  
    # find the phone number of the user
    user = User.query.filter_by(user_id=user_id).first()
    message_body = "Sorry {}, This is a warning alert—check it out!\n The holder of the phone {} is going from {} to {}.".format(user.name,user.phone_num, route_start, route_end)

    account_sid = environ.get("ACCOUNT_SID")
    auth_token = environ.get("AUTH_TOKEN")
    my_phone = environ.get("MY_PHONE")

    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=message_body,
                        from_=my_phone,
                        to= user.phone_num
                     )

    return message_body


@app.route("/shareLink", methods = ["POST"])
def share_link():
    """Send a shared link"""

    origin = request.form.get("start_address")
    destination = request.form.get("end_address")
    travel_mode = request.form.get("travelMode")
    waypoints = request.form.get("waypoints")
    link = request.form.get("link")

    # Create a google maps url that enables sharing the directions 
    origin = origin.replace(" ","+")
    destination = destination.replace(" ","+")
    travel_mode = travel_mode.lower()

    # exp: https://www.google.com/maps/dir/?api=1&origin=Pier+33+San+Francisco+ CA+USA&destination=Cable+Car+Museum+Mason+Street+San+Francisco+CA+USA&travelmode=walking&waypoints=37.8063378,-122.4054917|37.8066323,-122.4060625|37.8058092,-122.4119264|37.8011366,-122.4110618|37.8009343,-122.4127215 
    shared_url = link+"&origin="+origin+"&destination="+destination+"&travelmode="+travel_mode+"&waypoints="+waypoints
    
    # find the phone number of the user
    user_id = session.get("user_id") 
    user = User.query.filter_by(user_id=user_id).first()
    message_body = "See directions \n"+shared_url+"\n in Goggle Maps"

    account_sid = environ.get("ACCOUNT_SID")
    auth_token = environ.get("AUTH_TOKEN")
    my_phone = environ.get("MY_PHONE")

    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=message_body,
                        from_=my_phone,
                        to= user.phone_num
                     )

    return message_body


@app.route("/neighgeocode")
def geocode_test_neigh():
    """view neigh page"""
    
    return render_template("geocodeNeigh.html")

# reverse geocoding of the neighborhoods to get the all the neigh in the database.
@app.route("/neighcoordinates.json")
def showNeighborhood():
    """Show the coordinates of the crime for each selected neighborhood on the map"""

    result=Neighborhood.query.all()

    neigh_list = []
    neigh_id_list = []
    lat_list = []
    lng_list = []
    count_crime_list = []

    for eachneigh in result:
        querylatlng = Crime.query.filter(Crime.neighborhood_id==eachneigh.neigh_id).first()
        neigh_list.append(eachneigh.neigh_name)
        neigh_id_list.append(eachneigh.neigh_id)
        lat_list.append(querylatlng.latitude)
        lng_list.append(querylatlng.longitude)
        count_crime_list.append(eachneigh.count_crime)
             
    neigh_dic = {
        "name":neigh_list,
        "id":neigh_id_list,
        "latitude": lat_list,
        "longitude": lng_list,
        "count_crime":count_crime_list,
        "api_key":environ.get("API_KEY")
    }   
        
    return jsonify(neigh_dic)

    
# those variables are used to save the different google maps neighborhoods from ajax requests,
# in order to update the data base
# this route is called only one time and then I defined a function in the queryData file to update the neighborhoods names
# based on the results given by this route (/neighc)
list_neigh = []
listlatitude = []
listlongitude = []
number_names = []
name = []
idlist = []

@app.route("/neighc", methods=['POST'])
def update_neigh():
    """update the table neighborhood with the google maps api names of neighborhoods"""
    
    name.append(request.form.get('name'))
    listlatitude.append(float(request.form.get('latitude')))
    listlongitude.append(float(request.form.get('longitude')))
    number_names.append(int(request.form.get('number')))
    idlist.append(int(request.form.get('id')))

    # name= "Visitacion Valley"  latitude= 37.7181267149201  longitude= -122.414176324324
    if len(number_names) == 39:
        for index in range(len(number_names)):
            #get the neigh id
            neigh = Neighborhood.query.filter(Neighborhood.neigh_id==idlist[index]).first()
            neigh.neigh_name = name[index]
        db.session.commit()
       
    return 'OK', 200


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.app_context().push()
    # app.run()
    app.run(host="0.0.0.0")
