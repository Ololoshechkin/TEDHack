from server import *
import unittest
from json import *

class TUI_PIDOR(unittest.TestCase):

    def test_NewUser(self):
        server = Server()
        rets = []
        rets += [
            server.get('new_user', dumps({
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
        ]
        rets += [
            server.get('new_user', dumps({
                "login": 'josdas',
                "password": '1111',
                "user": {
                    "name": "Stas",
                    "sex": "m",
                    "age": 1998,
                    "login": "josdas",
                    "person_info": {}
                }
            }))
        ]
        rets += [
            server.get('new_user', dumps({
                "login": 'wafemand',
                "password": '1111',
                "user": {
                    "name": "Andrey",
                    "sex": "m",
                    "age": 1999,
                    "login": "wafemand",
                    "person_info": {}
                }
            }))
        ]
        rets += [
            server._get_new_token('josdas', '1234')
        ]
        rets += [
            server._get_new_token('josdas', '1234')
        ]
        rets += [
            server.get('update_position', dumps(
                {"token": server._get_new_token('josdas', '1234'), "position":[1, 2]}
            ))
        ]
        rets += [
            server.get('update_targets', dumps(
                {"token": server._get_new_token('josdas', '1234'), "targets":["SOSAT"]}
            ))
        ]
        rets += [
            server.get('find_person_nearby', dumps({
                "token": server._get_new_token("josdas", "1234"), "max_duration":"10", "sex":["m"], "min_age":"0", "max_age":"14"
            }
            )
                       )
        ]
        print(*rets, sep='\n')


if __name__ == '__main__':
    unittest.main()