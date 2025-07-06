from utils import webRequests
from rich import print


# Make the request
url = 'http://ip-api.com/json/'
requests = webRequests()
response = requests.get(url)
# Print the response
print(response.json())

# SECOND TIME USE
response = requests.get(url)
# Print the response
print(response.json())