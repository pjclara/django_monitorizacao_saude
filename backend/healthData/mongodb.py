from pymongo import MongoClient

# client = MongoClient("mongodb+srv://pjclara:mongoDB@djangodb.tdvpxfr.mongodb.net/?retryWrites=true&w=majority&appName=djangoDB")
# db = client['health-monitor-data']

# client = MongoClient("mongodb+srv://luismarques:o7xWHI2YFUoVyDYc@healthmonitor.tczuvem.mongodb.net/?retryWrites=true&w=majority&appName=HealthMonitor")
# db = client['health-monitor-data']

client = MongoClient("mongodb+srv://pjclara:mongoDB@djangodb.tdvpxfr.mongodb.net/?retryWrites=true&w=majority&appName=djangoDB")
db = client['health-monitor-final-data']