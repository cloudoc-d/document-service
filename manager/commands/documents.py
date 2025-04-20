from argparse import Namespace
from motor import MotorClient
import os

def generate_documents(args: Namespace):
    if args.mongodb_url is None:
        print('url to mongodb not provided. finishing')
        return -1

    mongo_client = MotorClient(args.mongodb_url)
    database = mongo_client.get_database(args.database)
    collection = mongo_client.get_collection(args.collection)

    # TODO
