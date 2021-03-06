# coding=utf-8
import os
from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps, loads
from werkzeug.utils import secure_filename
import json
import server_actions
import user
import random
import string
import copy


class Server(Resource):
    """
    Singleton!
    Special class for flask
    """

    def __init__(self):
        if not hasattr(Server, '_actions'):
            Server._actions = server_actions.Actions()
            Server._tokens = {}
            Server._logins = {}
        self._actions = Server._actions
        self._tokens = Server._tokens
        self._logins = Server._logins

    def _get_new_token(self, login, password):
        TOKEN_LEN = 32
        if self._actions.storage.is_user(login, password):
            token = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(TOKEN_LEN)
            )
            if login in self._logins:
                self._tokens.pop(self._logins[login])
                self._logins.pop(login)
            self._logins[login] = token
            self._tokens[token] = login
            return token
        else:
            return None

    def _is_correct_token(self, token):
        return token in self._tokens

    @staticmethod
    def _get_user_from_json(data):
        return user.User(**data)

    def get(self, function_name, args):
        SPECIAL_ANSWER = 'bad'
        SUCCESS_ANSWER = 'ok'
        try:
            parsed = loads(str(args))
        except TypeError:
            return SPECIAL_ANSWER
        try:
            if function_name == 'new_user':
                login = parsed['login']
                self._actions.new_user(
                    login,
                    parsed['password'],
                    Server._get_user_from_json(parsed['user'])
                )
                return SUCCESS_ANSWER
            elif function_name == 'get_new_token':
                login = parsed['login']
                return self._get_new_token(
                    login,
                    parsed['password']
                )
            elif self._is_correct_token(parsed['token']):
                login = self._tokens[parsed['token']]
                if function_name == 'find_person_nearby':
                    temp_users = self._actions.find_person_nearby(
                        login,
                        int(parsed['max_duration']),
                        parsed['sex'],
                        int(parsed['min_age']),
                        int(parsed['max_age'])
                    )
                    for i in range(len(temp_users)):
                        temp_users[i] = copy.deepcopy(temp_users[i].to_dick())
                        info = temp_users[i]['person_info']
                        if 'position' in info:
                            info['position'] = list(info['position'])
                        if 'targets' in info:
                            info['targets'] = list(info['targets'])
                    return dumps(temp_users)
                elif function_name == 'update_position':
                    self._actions.update_position(
                        login,
                        tuple(parsed['position'])
                    )
                    return SUCCESS_ANSWER
                elif function_name == 'update_user_info':
                    self._actions.update_user_info(
                        login,
                        Server._get_user_from_json(parsed['user'])
                    )
                    return SUCCESS_ANSWER
                elif function_name == 'update_targets':
                    self._actions.update_targets(
                        login,
                        set(parsed['targets'])
                    )
                    return SUCCESS_ANSWER
        except IndexError:
            return SPECIAL_ANSWER
        return SPECIAL_ANSWER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def start_server():
    app = Flask(__name__, static_url_path='/image', static_folder='tmp')
    api = Api(app)
    api.add_resource(Server, '/<string:function_name>/<args>')
    app.run()


if __name__ == '__main__':
    print(dumps({
        "login": 'josdas',
        "password": '1234',
        "user": {
            "name": "Stas",
            "sex": "m",
            "age": 1998,
            "login": "josdas",
            "person_info": {}
        }
    }))
    start_server()
