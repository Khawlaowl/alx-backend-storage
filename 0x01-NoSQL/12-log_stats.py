#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB.
Database: logs, Collection: nginx
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provides statistics about Nginx logs stored in MongoDB.
    """
    # Count total number of logs
    num_logs = mongo_collection.count_documents({})
    print(f"{num_logs} logs")

    # Count documents by HTTP methods
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count documents with method=GET and path=/status
    status_check = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx
    log_stats(collection)
