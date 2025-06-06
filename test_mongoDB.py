
# from pymongo.mongo_client import MongoClient

# uri ="mongodb+srv://hardikkhobragade78:hardik@cluster0.7tj79jr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('username')
password = urllib.parse.quote_plus('password')

client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster.7tj79jr.mongodb.net/dbname?retryWrites=true&w=majority",
    ssl=True,
    tlsAllowInvalidCertificates=False  # Set to True only for testing
)