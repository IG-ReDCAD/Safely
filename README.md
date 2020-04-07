# Safely
# <img src="https://github.com/IG-ReDCAD/Project-03-10/blob/master/static/img/logo.jpg" width="80%" alt="Safely">
From now on you can travel safely in San Francisco. Safely helps you walk or drive in safe routes. The user can get an idea about the level of safety of each route given by google maps. Then, these routes can be saved and shared on the phone. Safely also can give the user information and statistics about the level of safety of each neighborhood in San Francisco.
## Deployment
## About Me
Before studying at Hackbright Academy, Imen was as a mom taking care of her little one and wrapping up her PhD in computer science, graduating in 2018. Towards the end of her PhD studies, Imen wanted to work more practical applications. She just wanted to solve more concrete problems and see the results of her work much more quickly. So, she decided to become a software engineer. 
## Table of contents
* [Tech Stack](#tech-stack)
* [APIs](#api)
* [Features](#features)
* [Roadmap](#future)
* [Installation](#installation)
## <a name="tech-stack"></a>Technologies
* Python
* Javascript
* Flask
* Jinja2
* Pandas
* SQLAlchemy
* HTML
* CSS
* Bootstrap
* jQuery
## <a name="api"></a>APIs
* Google maps APIs
** Geocoding api
** Directions api
** Places api
* Twilio API

## <a name="features"></a>Features

#### login and registration
Once signed in, the user’s profile is created. 
![alt text](https://github.com/IG-ReDCAD/Project-03-10/blob/master/static/img/login.gif "Sign in")

#### Directions
Using Safely, users can access the direction page and give the origin and the destination of their trip. Using SQLAlchemy, the application can interface with the crime database. The application’s backend is written in Python with Flask as a Python web application framework. Using Javascript and google maps APIs, the different route options are generated. Then, by sending an Ajax request to the server, the different crime data for each direction are given. Based on this data, safety score for each route is calculated.

![alt text](https://github.com/IG-ReDCAD/Project-03-10/blob/master/static/img/direction.gif "Directions")

Safely also enables the users to save and share the different trips on their iOS/ Android phone or tablet using the Twilio API. If you are concerned about your children safety, you can just create a profile for them, and if your child is going through a high crime route, Safely will automatically notify you by sending a text message.

#### Neighborhoods
The Safely app enables the user to get an idea about the safety level of each neighborhood in the city. Here the user can select the neighborhood and the crime category to get the information about the crime history in that area, and to get the statistics according to the time which is generated using jQuery and Chart.js.

![alt text](https://github.com/IG-ReDCAD/Project-03-10/blob/master/static/img/neighborhood.gif "Neighborhood")

#### Profile
The user of Safely has a profile in which the different trips are saved and a safety related statistics are given. 

![alt text](https://github.com/IG-ReDCAD/Project-03-10/blob/master/static/img/profile.gif "Profile")

## <a name="future"></a>Roadmap
The project roadmap for Safely has several features planned out for the next sprint:
* Extending support to other cities besides San Francisco.

## <a name="installation"></a>Installation
💡To run Safely on your own machine:
* Clone this repository: 
```
https://github.com/IG-ReDCAD/Safely.git
```
* Create and activate a virtual environment inside your Safely directory:
```
virtualenv env
source env/bin/activate
```

* Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Google maps API](https://cloud.google.com/maps-platform/)
Sign up to use the [Twilio API](https://www.twilio.com/try-twilio)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export API_KEY="YOUR_KEY_HERE"
export ACCOUNT_SID="YOUR_SID_HERE"
export AUTH_TOKEN="YOUR_TOKEN_HERE"
export MY_PHONE="YOUR_PHONE_NUMBER_HERE"

```
* Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```
* Create an empty database called crimeData and use crimeData.sql to populate it:
```
createdb crimeData
psql crimeData < crimeData.sql
```
<!-- 
* Download the SF crimes CSV file:
```
https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/data
```
* Save the crimes CSV file into a `data` folder and name the file: 
```
Police_Department_Incident_Reports__2018_to_Present.csv
```
* Download the SF neighborhoods CSV file:
```
https://data.sfgov.org/Geographic-Locations-and-Boundaries/SF-Find-Neighborhoods/pty2-tcw4
```
* Save the neighborhoods CSV file into a `data` folder and name the file: 
```
SFFind_Neighborhoods.csv
```

* Set up the database:

```
createdb crimeData
python3 model.py
python3 queryData.py
```
-->
* Run the app:

```
python3 server.py
```

⭐ You can now navigate to 'localhost:5000/' to access Safely.




