from flask import Flask, request
from flask import make_response

app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route('/')
def home():
    # returning string
    # return "Hello, World!, this is a Flask app running in a virtual environment!"

    # returning json
    return {"message": "Hello, World!, this is a Flask app"}

@app.route('/no_content')
def no_content():
    # returning no content
    return "No content found", 204

@app.route('/exp')
def index_explicit():
    # returning json with make_response() method
    resp = make_response({"message": "Hello, World!, this is a Flask app"})
    resp.status_code = 200
    
    return resp

@app.route('/data')
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
             # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"meassage": "Data not found"}, 404
    
@app.route("/name_search")
def name_search():
    """Find a person in the database.

    Returns:
        json: Person if found, with status of 200
        404: If not found
        422: If argument 'q' is missing
    """
    # Get the argument 'q' from the query parameters of the request
    query = request.args.get('q')

    # Check if the query parameter 'q' is missing
    if not query:
        # Return a JSON response with a message indicating 'q' is missing and a 422 Unprocessable Entity status code
        return {"message": "Query parameter 'q' is missing"}, 422

    if not isinstance(query, str):
        return {"message": "Invalid parameter type"}, 400
    
    # Iterate through the 'data' list to look for the person whose first name matches the query
    for person in data:
        if query.lower() in person["first_name"].lower():
            # If a match is found, return the person as a JSON response with a 200 OK status code
            return person

    # If no match is found, return a JSON response with a message indicating the person was not found and a 404 Not Found status code
    return {"message": "Person not found"}, 404


@app.route("/count")
def get_count():
    try:
        # Attempt to return a JSON response with the count of items in 'data'
        return {"message": f"Data count is {len(data)}"}, 200
    except NameError:
        # If 'data' is not defined and raises a NameError
        return {"message": "Data is Not Found"}, 500
    

@app.route("/person/<var_name>", methods=['GET'])
def find_by_uuid(var_name):
    # Iterate through the 'data' list to search for a person with a matching ID
    person = find_person_by_id(var_name)
    if person:
        # Return the person as a JSON response if a match is found
        return person

    # Return a JSON response with a message and a 404 Not Found status code if no matching person is found
    return {"message": "Person not found"}, 404


@app.route("/person/<var_name>", methods=['DELETE'])
def delete_person(var_name):
    for person in data:
        if person["id"] == str(var_name):
            # Remove the person from the data list
            data.remove(person)
            # Return a JSON response with a message and HTTP status code 200 (OK)
            return {"message": f"Person with ID: {var_name} deleted"}, 200
    # If no person with the given ID is found, return a JSON response with a message and HTTP status code 404 (Not Found)
    return {"message": "Person not found"}, 404


@app.route("/person", methods=['POST'])
def add_by_uuid():
    try:    
        # Get the JSON data from the request
        new_person =  request.get_json()
        if not new_person:
            # If no JSON data is provided, return a 422 Unprocessable Entity response
            return {"message": "No JSON data provided"}, 422
        
        # Check if the required fields are present in the JSON data
        if not all(key in new_person for key in ("id", "first_name", "last_name", "graduation_year", "address", "city", "zip", "country", "avatar")):
            # If any required field is missing, return a 422 Unprocessable Entity response
            return {"message": "Missing required fields"}, 422

        if (person_exists:= find_person_by_id(new_person['id'])):
            # If a person with the same ID already exists, return a 422 Unprocessable Entity response
            return {"message": f"Person: {person_exists} with ID already exists"}, 422
        
        # Add the new person to the data list
        data.append(new_person)

        # Return a JSON response with a message and HTTP status code 201 (Created)
        return {"message": f"Person with ID: {new_person['id']} added"}, 201
    except NameError:
        # If 'data' is not defined and raises a NameError
        return {"message": "Data is Not Found"}, 500
    

@app.errorhandler(404)
def api_not_found(error):
    # Return a JSON response with a message and HTTP status code 404 (Not Found)
    return {"message": "API not found"}, error.code


def find_person_by_id(person_id):
    """Find a person in the database by ID.

    Args:
        person_id (str): The ID of the person to find.

    Returns:
        dict: The person if found, None otherwise.
    """
    try:
        for person in data:
            if person["id"] == person_id:
                return person
    except NameError:
        # Handle the case where 'data' is not defined
        # Return None or raise an exception as needed
        raise NameError("Data not found")
    return None