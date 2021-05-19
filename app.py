import time
import json
import datetime
import os

from flask import *
from flask_cors import CORS
from recall_api import RecallsAPI
from air_quality_api import AirAPI
import earthquakes
import tzlocal

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if 'DYNO' not in os.environ:
    with open("api_keys.json", "r") as api_keys:
        api_keys_json = json.loads(api_keys.read())
else:
    api_keys_json = {
        "secret_key": os.environ["secret_key"],
        "RecallApi": os.environ["RecallApi"],
        "AirQualityApi": os.environ["AirQualityApi"]
    }
app.secret_key = api_keys_json["secret_key"]
recall_object = RecallsAPI(api_key=api_keys_json["RecallApi"])
air_object = AirAPI(api_key=api_keys_json["AirQualityApi"])

@app.route("/", methods=["GET", "POST"])
def home(): 
    if request.method == "GET":   
        try:
            session["start_date_food"]
            session["end_date_food"]
            session["start_date_slash_food"]
            session["end_date_slash_food"]  
        except:
            session["start_date_food"] = datetime.datetime.today().strftime("%Y0101")
            session["end_date_food"] = datetime.datetime.today().strftime("%Y%m%d")
            session["start_date_slash_food"] = datetime.datetime.today().strftime("1/1/%Y")
            session["end_date_slash_food"] = datetime.datetime.today().strftime("%m/%d/%Y")
        x = recall_object.search('&search=report_date:[%s+TO+%s]&limit=100' %(session["start_date_food"], session["end_date_food"]))
        return render_template("home.html", food_recalls=x, start_date_food=session["start_date_slash_food"], end_date_food=session["end_date_slash_food"], earthquakes_reported=earthquakes.get_report('week', 'all'), epoch_to_time=lambda x: epoch_to_time(x))
    elif request.method == "POST":
        print(request.form)
        if request.form["type"] == "date_change":
            tmp_lst = request.form["start_date"].split(" ")
            x = str(time.strptime(tmp_lst[0],'%b').tm_mon)
            if len(x) == 1:
                x = "0"+x
            session["start_date_food"] = "".join([tmp_lst[2], x, tmp_lst[1][0:2]])
            session["start_date_slash_food"] = "".join([x, "/", tmp_lst[1][0:2], "/", tmp_lst[2]])
            tmp_lst = request.form["end_date"].split(" ")
            x = str(time.strptime(tmp_lst[0],'%b').tm_mon)
            if len(x) == 1:
                x = "0"+x
            session["end_date_food"] = "".join([tmp_lst[2], x, tmp_lst[1][0:2]])
            session["end_date_slash_food"] = "".join([x, "/", tmp_lst[1][0:2], "/", tmp_lst[2]])
            return redirect("/")

@app.route("/api/air_quality", methods=["POST"])
def air_quality():
    try: # Detects if zip code does not exist
        return {"air_quality": air_object.search(request.json["zipCode"])[0]["Category"], "full_air_quality": air_object.search(request.json["zipCode"])[0], "worked": True}
    except:
        return {"worked": False}

def epoch_to_time(epoch_time):

    utc_time = datetime.datetime.fromtimestamp(epoch_time/1000, datetime.timezone.utc)
    local_time = utc_time.astimezone()
    return local_time.strftime("%I:%M:%S %h/%d/%Y")


if __name__ == "__main__":
    app.run(debug=True)
