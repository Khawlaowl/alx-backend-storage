#!/usr/bin/env python3
'''Task 14's module.
'''

from pymongo import MongoClient

def top_students(mongo_collection):
    '''Returns all students in a collection sorted by average score.
    '''
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    'name': 1,
                    'averageScore': {
                        '$avg': '$topics.score',
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return students

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.students

    for student in top_students(collection):
        print(f"Name: {student['name']}, Average Score: {student['averageScore']}")

if __name__ == '__main__':
    main()
