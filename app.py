# 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

# https://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@github.com/emmarodam/uw_exam.git

from bottle import default_app, get, post, request, response, run, static_file, template
import x
from icecream import ic
import re
import requests
import json

from bottle import get, post, run, response, Bottle, request
import git, json

app = Bottle()

@post('/secret_url_for_git_hook')
def git_update():
  repo = git.Repo('./uw_exam')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

##############################

@get("/")
def _():
  return "Jubii"

##############################

correct_token = "241097"

@get("/crimes")
def _():
    token = request.query.get("token", "")
    if token != correct_token:
        response.status = 401
        return "Unauthorized access"
    try:
        # Assuming your JSON file is named data.json
        with open("/home/emmarodam/uw_exam/crime.json", "r") as f:
            data = json.load(f)
        response.content_type = 'application/json'
        return json.dumps(data)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080, debug=True)

##############################
try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=80, debug=True, reloader=True)

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")


##############################
@get("/<file_name>.js")
def _(file_name):
    return static_file(file_name+".js", ".")

##############################
@get("/get-crime")
def _():
  token = "241097"
  crime = f"https://emmarodam.pythonanywhere.com/crime?token={token}"
 
  # Make the HTTP GET request
  response = requests.get(crime)
 
  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Access the JSON data from the response
    crime_data = response.json()
    print(crime_data)  # Output the JSON data
  else:
    print("Failed to fetch data. Status code:", response.status_code)
 
  query = {
    "query": """
      INSERT @crime_data INTO crimes RETURN NEW
    """,
    "bindVars": {
      "crime_data": crime_data
    }
  }
 
  res = x.db(query)
  ic(res)
 
  return res["result"]
 
app = default_app

# @get("/")
# def _():
#     # url from postman but the first part we found in docker 
#     url = "http://host.docker.internal:8529/_api/cursor"
#     # query i want to send 
#     q = {"query":"FOR suspect IN suspects RETURN suspect"}
#     # respond
#     res = requests.post( url, json = q )
#     res = res.json()
#     print("#"*50)
#     print(type(res))
#     # return str(res["result"])
#     return template("index", suspects=res["result"])

# @get("/get-crimes")
# def _():
#   crime = {
#     "id": "1",
#     "lat": 1,
#     "lon":1,
#     "severity":8,
#     "suspects":[
#       {"cpr":"111", "name":"A"}
#     ]
#   }
 
#   # Extract the suspects from the crime
#   # The crime will be the same without suspect
 
#   suspects = crime["suspects"]
#   ic("#"*30)
#   ic(suspects)
 
 
#   # Save the crime to the crimes collection, make sure
#   # that you get back the crime's id: Eg: crimes/4565656
 
#   query = {
#     "query": """
#       INSERT @crime INTO crimes RETURN NEW
#     """,
#     "bindVars": {
#       "crime": crime
#     }
#   }
#   res = x.db(query)
#   ic(res)
 
#   # Get the id of the crime
#   crime_id = res["result"][0]["_id"]
#   ic(crime_id)
#   # res->result->0->_id
#   # return "crimes saved in arangodb"
 
 
#   # Gold Challenge
#   # Insert the crime and the suspect in the edge collection
 
#   doc = {"_from":crime_id, "_to":suspects_id}
#   query = {
#     "query": """
#       INSERT @doc INTO crimes_commited_by_suspects RETURN NEW
#     """,
#     "bindVars": {
#       "doc": doc
#     }
#   }
#   x.db(query)
 
#   return "ok"

