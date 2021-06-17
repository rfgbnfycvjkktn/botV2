from pymongo import MongoClient
import datetime

import os

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

# Connect to the test db
db = client.tbot


class User:
    def add(self, data):
        user = db.users
        user_details = {
            '_id': data['id'],
            'name': data['name'],
            'username': data['username'],
            'email': "",
            'access': data['access'],
            'reg_date': data['reg_date'],
            'sub_start_date': data['sub_start_date'],
            'sub_end_date': data['sub_end_date']
        }

        Queryresult = user.find_one({'_id': data['id']})

        if Queryresult is None:
            result = user.insert_one(user_details)
            print('Добавлен юзер')
        else:
            print('Юзер уже есть')


    # проверка есть ли подписка и не кончилась ли она
    def paid(self, data):
        user = db.users
        Queryresult = user.find_one({'_id': data, 'access': True, 'sub_end_date': {'$gte': datetime.datetime.today().replace(microsecond=0)}})

        if Queryresult is None:
             return False
        else:
            return True

        return False

    def check_sub(self, data):
        user = db.users
        Queryresult = user.find_one({'_id': data, 'access': True})

        if Queryresult is None:
            return {"status_sub": False, "sub_end": ""}
        else:
            return {"status_sub": True, "sub_end": Queryresult['sub_end_date']}

        return {"status_sub": False, "sub_end": ""}

    def add_sub(self, data):
        user = db.users
        user_details = {
            '_id': data['id'],
            'name': data['name'],
            'username': data['username'],
            'email': "",
            'access': data['access'],
            'reg_date': data['reg_date'],
            'sub_start_date': data['sub_start_date'],
            'sub_end_date': data['sub_end_date']
        }

        Queryresult = user.find_one({'_id': data['id']})

        if Queryresult is None:
            result = user.insert_one(user_details)
            print('Добавлен юзер')
        else:
            result = user.update_one({'_id': user_details['_id']}, {'$set': {'sub_start_date': user_details['sub_start_date'], 'sub_end_date': user_details['sub_end_date'], 'access': user_details['access']}})
            print('Обновление подписки')
