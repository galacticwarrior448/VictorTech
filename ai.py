from fastapi import FastAPI

import requests
import google.generativeai as genai
import time

app = FastAPI()
genai.configure(api_key="AIzaSyBFLy_vJnEB1aJhStRbtaCYXu45YmzrB6s")
model = genai.GenerativeModel("gemini-1.5-flash")

from fastapi import FastAPI, Request
from realTime import *

app = FastAPI()

@app.get("/stock/{company}")
def return_stocks(company: str):
    output = get_line_graph(company)
    print({"symbol": output[0], "data": output[1]})
    return {"symbol": output[0], "data": output[1]}

@app.get("/find/{company}")
def return_location(company: str):
    stores = find_stores(company, "India")
    return {"data": stores}

@app.get("/age_gender/{company}")
def return_gender_age(company: str):
    return age_gender_traffic_distribution(company)

@app.get("/connect")
def read_root():
    return {"message": "hello"}

@app.get("/everything/{company}")
def master(company: str):
    output = {}
    output["name"] = company
    locations = find_stores(company, "India")
    output["mapLocations"] = locations
    stocks = get_line_graph(company)
    output["performance"] = {"years": stocks[0], "data": stocks[1]}
    demo = age_gender_traffic_distribution(company)
    output["traffic"] = {"stores": demo["trafficSources"][0], "data": demo["trafficSources"][1]}
    output["demographics"] = {"gender": demo["gender"][1], "age": demo["age"][1]}
    output["marketingStrategies"] =  ["Social Media", "Email Marketing", "Influencer Partnerships"]
    output["customerFeedback"] = ["Great service at Store 1!", "Store 2 has a good selection of products.", "The staff at Store 3 were very helpful."]
    return output

@app.get("/once/")
def once():
    return master("croma electronics")

@app.get("/marketingo/{company}")
def return_stocks(company: str):
    response = model.generate_content(f"Write 3 marketing strategy single line points of {company}, give only the points and no intro line")
    marketing=response.text
    return {"message": marketing}
