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
