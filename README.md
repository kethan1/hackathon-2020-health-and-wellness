# Hackathon 2020 Health and Wellness Website

Create a json file called `api_keys.json`. Then, add the below info to the file, and replace `Recall Api Key Here` with an api key from https://open.fda.gov/apis/ and `Air Quality Api Key Here` with an api key from https://docs.airnowapi.org/:
```
{
    "app_secret_key": "<Some random text, used by Flask to encrypt tokens>"
    "RecallApi": "<Recall Api Key Here>",
    "AirQualityApi": "<Air Quality Api Key Here>"
}
```

Install packages:

```
pip install -r requirements.txt
```

Run:

```
python app.py
```

Website Accessable At: https://health-and-wellness2020.herokuapp.com/

Youtube Link: https://www.youtube.com/watch?v=UrM8VZ2CS1Q
