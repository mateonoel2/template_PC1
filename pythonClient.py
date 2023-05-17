import http.client
import json

# Create an HTTP connection
conn = http.client.HTTPConnection("127.0.0.1", 5000)


# Create the data to send in the request body
data = {
    "username": "Profe",
    "password": "123"
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the headers for the request
headers = {
    "Content-type": "application/json"
}

# Send a PUT request with the body
conn.request("POST", "/players/add", body=json_data, headers=headers)

# Get the response
response = conn.getresponse()

# Print the response status code
print("Status:", response.status)

# Print the response body
print("Response:", response.read().decode())

conn.request("GET", "/players")

# Get the response
response = conn.getresponse()

print("GET")

# Print the response status code
print("Status:", response.status)

# Print the response body
print("Response:", response.read().decode())

# Close the connection
conn.close()

#kfuhsdiufghdi