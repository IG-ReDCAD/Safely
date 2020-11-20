"""Fill the tables with data from the CSV file
"""

from model import db, User, Route, Crime, Category, Resolution, Neighborhood, Subcategory, connect_to_db
import pandas as pd 
from sqlalchemy import func, update
from server import app


data = pd.read_csv("data/Police_Department_Incident_Reports__2018_to_Present.csv") 
df = pd.DataFrame(data)
total_rows=len(df.axes[0])
total_cols=len(df.axes[1])


def loadCategory():
    """look for the category names in the csv file and load the table categories"""

    category_names_set = set()
    list_categories = ['Human Trafficking (A), Commercial Sex Acts', 'Civil Sidewalks', 
                            'Gambling','Motor Vehicle Theft', 'Drug Offense', 'Rape',  'Prostitution', 
                            'Homicide', 'Robbery', 'Drug Violation', 'Burglary','Sex Offense', 
                            'Offences Against The Family And Children','Weapons Offense', 
                            'Stolen Property', 'Larceny Theft', 'Assault', 'Human Trafficking, Commercial Sex Acts', 
                            'Warrant', 'Weapons Carrying Etc', 'Family Offense','Weapons Offence', 'Malicious Mischief',
                            'Vehicle Impounded']  

    for index in range(total_rows):
        category_name_row = data.iloc[index][14]
        
        if str(category_name_row).strip() in list_categories :
            category_names_set.add(category_name_row)        

    list_categories = list(category_names_set)

    for i in range(len(list_categories)):
        category_instance = Category( category_name=list_categories[i], count_crime=0)
        db.session.add(category_instance)
        
    db.session.commit()
    print("Category table is loaded")


def loadResolution():
    """look for the resolutions of the crimes and load them in a table"""

    resolution_names_set = set()

    for index in range(total_rows):
        resolution_name_row = data.iloc[index][17]
        if resolution_name_row != "nan":
            resolution_names_set.add(resolution_name_row)     

    list_resolution = list(resolution_names_set)

    for i in range(len(list_resolution)):
        resolution_instance = Resolution(resolution_id=i, resolution_name=list_resolution[i], count_crime=0)
        db.session.add(resolution_instance)
        
    db.session.commit()
    print("Resolution table is loaded")
    

def get_category_id(name_category):
    """function returns the id of a category of a given subcategory"""

    result=Category.query.filter(Category.category_name == name_category).first()
    
    if result != None:
        return result.category_id
    
    return None


def get_subcategory_id(name_subcategory):
    """function returns the id of a category of a given subcategory"""

    result=Subcategory.query.filter(Subcategory.subcategory_name == name_subcategory).first()
    
    if result != None:
        return result.subcategory_id 
    
    return None


def get_resolution_id(name_resolution):
    """function returns the id of a category of a given subcategory"""

    result=Resolution.query.filter(Resolution.resolution_name == name_resolution).first()
    
    return result.resolution_id


def get_neigh_id(name_neigh):
    """function returns the id of a given neighborhood name"""

    result=Neighborhood.query.filter(Neighborhood.neigh_name == name_neigh).first()
    
    return result.neigh_id


def loadSubcategory():
    """look for the subcategories of the crimes and load them in a table"""

    subcat_name_set = set()

    for index in range(total_rows):
        subcat_name_row = data.iloc[index][15]
        if str(subcat_name_row).strip() != "nan" and str(subcat_name_row).strip() != "NaN":
            if (data.iloc[index][14]!="nan" and data.iloc[index][14]!="NaN" and data.iloc[index][14]!=None):
                cat_id = get_category_id(data.iloc[index][14])
                if cat_id:
                    subcat_name_set.add((subcat_name_row, int(cat_id)))     

    list_subcat = list(subcat_name_set)

    for i in range(len(list_subcat)):
        subcat_instance = Subcategory(subcategory_id=i, category_id=list_subcat[i][1], subcategory_name=list_subcat[i][0], count_crime=0)
        db.session.add(subcat_instance)
        
    db.session.commit()
    print("subcategory table is loaded")


def loadNeighborhood():
    """look for the neighborhoods and load them to the table"""

    neighborhood_name_set = set()

    for index in range(total_rows):
        neighborhood_name_row = data.iloc[index][21]
        if neighborhood_name_row != "null":
            neighborhood_name_set.add(neighborhood_name_row)

    list_neighborhood = list(neighborhood_name_set)

    for i in range(len(list_neighborhood)):
        neigh_instance = Neighborhood(neigh_id=i, neigh_name=list_neighborhood[i], count_crime=0)
        db.session.add(neigh_instance)
        
    db.session.commit()
    print("neighborhood table is loaded")


def loadCrime():
    """look for the crimes from the csv file and load the table"""

    id_value=0

    for index in range(total_rows):
        if (str(data.iloc[index][23]).strip()!="nan" and str(data.iloc[index][23]).strip()!="NaN"):
            crime_name_row = data.iloc[index][16]
            if crime_name_row != "null" and str(data.iloc[index][21]).strip()!="null" and str(data.iloc[index][21]).strip()!="nan" and str(data.iloc[index][21]).strip()!="NaN" and str(data.iloc[index][14]).strip()!="nan" and str(data.iloc[index][14]).strip()!="NaN" and str(data.iloc[index][15]).strip()!="nan" and str(data.iloc[index][15]).strip()!="NaN" and str(data.iloc[index][17]).strip()!="nan" and str(data.iloc[index][17]).strip()!="NaN":
                if (str(data.iloc[index][14]).strip()!="nan" and str(data.iloc[index][14]).strip()!="NaN"):
                    cat_id = get_category_id(str(data.iloc[index][14]))
                    if cat_id!=None:
                        cat_id=int(cat_id)
                        if (str(data.iloc[index][15]).strip()!="nan" and str(data.iloc[index][15]).strip()!="NaN"):
                            subcat_id = get_subcategory_id(data.iloc[index][15])
                            if subcat_id!=None:
                                subcat_id=int(subcat_id)
                                if (str(data.iloc[index][17]).strip()!="nan" and str(data.iloc[index][17]).strip()!="NaN"):
                                    res_id = int(get_resolution_id(data.iloc[index][17]))
                                    if (str(data.iloc[index][21]).strip()!="null" and str(data.iloc[index][21]).strip()!="nan" and str(data.iloc[index][21]).strip()!="NaN"):
                                        neigh_id=int(get_neigh_id(data.iloc[index][21]))
                                        crime_date=data.iloc[index][1]
                                        crime_time=data.iloc[index][2]
                                        crime_day=data.iloc[index][4]
                                        intersection=data.iloc[index][18]
                                        police_district=data.iloc[index][20]
                                        latitude=float(data.iloc[index][23])
                                        longitude=float(data.iloc[index][24])

                                        #add a crime instance 
                                        crime_instance = Crime(
                                                            category_id=cat_id,
                                                            subcategory_id=subcat_id,
                                                            resolution_id=res_id,
                                                            neighborhood_id=neigh_id,crime_date=crime_date,
                                                            crime_time=crime_time,
                                                            crime_day=crime_day,
                                                            intersection=intersection,
                                                            police_district=police_district,
                                                            latitude=latitude,
                                                            longitude=longitude)

                                        db.session.add(crime_instance)
                                        
    db.session.commit()
    print("crime table is loaded")


def countcrimeCategory():
    """count the crimes for each category"""

    result=db.session.query(Crime.category_id, func.count(Crime.category_id)).group_by(Crime.category_id).all()

    for item in result:
        cat_instance=Category.query.filter(Category.category_id==item[0]).first()
        cat_instance.count_crime=item[1]
        
    db.session.commit()
    print("Success count of the crimes in the category table")
    

def countcrimeSubcategory():
    """count the crimes for each category"""

    result=db.session.query(Crime.subcategory_id, func.count(Crime.subcategory_id)).group_by(Crime.subcategory_id).all()

    for item in result:
        subcat_instance=Subcategory.query.filter(Subcategory.subcategory_id==item[0]).first()
        subcat_instance.count_crime=item[1]
        
    db.session.commit()
    print("Success count of the crimes in the subcategory table")


def countneigh():
    """count the crimes for each category"""

    result=db.session.query(Crime.neighborhood_id, func.count(Crime.neighborhood_id)).group_by(Crime.neighborhood_id).all()

    for item in result:
        neigh_instance=Neighborhood.query.filter(Neighborhood.neigh_id==item[0]).first()
        neigh_instance.count_crime=item[1]
        
    db.session.commit()
    print("Success count of the crimes in the neighborhood table")


def countresolution():
    """count the crimes for each category"""

    result=db.session.query(Crime.resolution_id, func.count(Crime.resolution_id)).group_by(Crime.resolution_id).all()

    for item in result:
        res_instance=Resolution.query.filter(Resolution.resolution_id==item[0]).first()
        res_instance.count_crime=item[1]
        
    db.session.commit()
    print("Success count of the crimes in the resolution table")
    

def updateNeigh():
    """update neighborhood names"""

    list_names=['Richmond District', 'Ingleside Heights', 'Mission Bay', 'Western Addition', 'Inner Richmond', 'Financial District', 'North Beach', 'Richmond District', 'Outer Mission', 'Inner Richmond', 'Inner Richmond', 'Excelsior', 'Bernal Heights', 'Russian Hill', 'Western Addition', 'Chinatown', 'Western Addition', 'Mission District', 'Visitacion Valley', 'Eureka Valley', 'Lower Haight', 'Nob Hill', 'Presidio of San Francisco', 'Outer Sunset', 'SoMa', 'Crocker-Amazon', 'Cow Hollow', 'Tenderloin', 'Inner Richmond', 'Mission District', 'Lakeshore', 'Noe Valley', 'Bayview', 'Western Addition', 'Inner Sunset', 'Treasure Island', 'Portola', 'Potrero Hill', 'Excelsior']
    list_lat=['37.7875617006166', '37.7116545464983', '37.7734669206075', '37.7876505608381', '37.7829892031684', '37.7886939911118', '37.8053613764333', '37.7813271952934', '37.7323680630673', '37.7813145853411', '37.7746869050224', '37.7218093092921', '37.7447701714148', '37.8031353981594', '37.7869246657501', '37.7976275611592', '37.7804962596111', '37.7507710862427', '37.7124652739157', '37.7590248731517', '37.7708609110404', '37.7938920832601', '37.8046420690203', '37.763514757218', '37.777092184217', '37.7102705625953', '37.7996339290201', '37.784500842896', '37.7731144218041', '37.7687704978535', '37.7269499129252', '37.7520921065393', '37.7270441457937', '37.7780718661844', '37.7657826688311', '37.8241191327352', '37.7324386568328', '37.7546287151564', '37.7265882010247']
    list_lng=['-122.486358958424', '-122.46616467655', '-122.391434336521', '-122.428525012334', '-122.46335052669', '-122.405221173456', '-122.411858463637', '-122.499870571861', '-122.439747761245', '-122.457733044998', '-122.455252545373', '-122.416484418862', '-122.417851081279', '-122.418151093184', '-122.426666808154', '-122.408618846805', '-122.43214039079', '-122.416107621549', '-122.411571716261', '-122.440797806792', '-122.432717263695', '-122.416291703749', '-122.471124297135', '-122.478190826914', '-122.410505754041', '-122.433033238211', '-122.437694706538', '-122.419454543896', '-122.472297342032', '-122.427462058806', '-122.476039473494', '-122.434162782384', '-122.388672813182', '-122.424903921014', '-122.469653850017', '-122.372658041869', '-122.4056075492', '-122.40062568351', '-122.433357451163']

    for index in range(len(list_names)):
        crime_instance=Crime.query.all()
        for item in crime_instance:
            if item.latitude == float(list_lat[index]) and item.longitude== float(list_lng[index]):
                neigh_instance=Neighborhood.query.all()
                for item_neigh in neigh_instance:
                    if item_neigh.neigh_id == item.neighborhood_id:
                        item_neigh.neigh_name=list_names[index]

    db.session.commit()
    print("table updated with the new names from the google map neighborhoods")


def addRoute():
    """add a route"""

    new_user= User(name="Imy", email="aa.gmail.com", password="123")
    new_route = Route(user_id=1, route_name="home", route_start="Hackbright Academy, Sutter Street, San Francisco, CA, USA", route_end="Dolores Park, 19th Street, San Francisco, CA, USA", score=5246.363636363636)
    db.session.add(new_user)
    db.session.add(new_route)
    db.session.commit()
    

def cleanTables():
    """clean the tables"""

    result=Neighborhood.query.filter(Neighborhood.neigh_name == "NaN").all()
    for neigh in result:
        db.session.delete(neigh)
        db.session.commit()

    result=Category.query.filter(Category.category_name == "NaN").all()
    for cat in result:        
        db.session.delete(cat)
        db.session.commit()
        
    print("table category and neighborhood is ready after cleaning them")


if __name__ == '__main__':
    connect_to_db(app)
    app.app_context().push()

    loadCategory()
    loadResolution()
    loadSubcategory()
    loadNeighborhood()
    cleanTables()
    loadCrime()
    countcrimeCategory()
    countcrimeSubcategory()
    countneigh()
    countresolution()
    updateNeigh()
