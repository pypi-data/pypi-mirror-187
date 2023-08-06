import sys
from pymongo import MongoClient
import os

TEST_MONGODB_URI_ENV = "TEST_MONGODB_URI"


def init_request(request):
    arguments_count = len(sys.argv)

    if arguments_count != 2:
        print("error: test requires a token")
        exit(1)

    request["header"]["token"] = sys.argv[1]


def restore_initial_state(database, collection) -> bool:
    try:
        client = MongoClient(os.environ.get(TEST_MONGODB_URI_ENV))

        database = client[database]
        collection = database[collection]

        collection.drop()

        return True
    except:
        return False
