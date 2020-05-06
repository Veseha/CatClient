import os
import parser

from flask import jsonify
from flask_restful import Resource

import global_var as gv
import service_func as sf
from data import db_session
from data.settings import Settings
from data.users import User


class Userlist(Resource):
    def get(self, token):
        """
        :return:
            {
              "users": [
                {"Veseha": "dir,dir,dir"},
                {"Lunar": "dir,dir,dir"}
              ]
            }
        """

        session = db_session.create_session()
        userlist = session.query(User).all()
        real = sf.token_to_login(token)
        if real:
            if real == 'admin':
                users = [(i.name, i.dirs) for i in userlist]
            else:
                users = [((i.name, i.dirs) if i.name == real else None) for i in userlist]
            ret = {'users': users}
        else:
            ret = {'error': 'CredentialError'}

        return jsonify(ret)


class Userget(Resource):
    def get(self, user, token):
        """
        :param id_user:
        :return:
        {
            "dirs": "dir,dir,dir"
        }
        """

        real = sf.token_to_login(token)

        if real:
            if not sf.get_user(sf.login_to_id(user)):
                return jsonify({"error": 'NoUserFound'})
            session = db_session.create_session()
            user = session.query(User).get(sf.login_to_id(user))
            dirs_user = user.dirs

            if real == 'admin' or user.name == real:
                return jsonify({'dirs': dirs_user})
            else:
                return jsonify({'error': 'CredentialError'})
        else:
            return jsonify({'error': 'CredentialError'})

    def post(self):
        """
        not working
        :return:
        """
        args = parser.parse_args()
        session = db_session.create_session()
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, news_id):
        """
        not work
        :param news_id:
        :return:
        """
        sf.get_user(news_id)
        session = db_session.create_session()
        session.commit()
        return jsonify({'success': 'OK'})


class Users(Resource):
    None


class Auth(Resource):
    def get(self, login, hash):
        session = db_session.create_session()
        user = session.query(User).filter(User.name == login).first()
        ret = {}
        if user and user.check_password(hash, is_hash=True):
            ret['error'] = 'OK'
            token = sf.get_token(login)
            if token:
                ret['token'] = token
            else:
                ret['error'] = 'NoToken'
            return ret
        else:
            ret['error'] = 'CredentialError'
            return ret

    def post(self):
        pass


class Tokens(Resource):
    def get(self, login, hash):
        pass

    def post(self, login, hash):
        from service_func import generate_token
        session = db_session.create_session()

        user = session.query(User).filter(User.name == login, User.hashed_password == hash).first()

        if not user:
            return jsonify({"error": "CredentialError"})
        user_settings = session.query(Settings).filter(Settings.id == user.id).first()
        if user_settings.token:
            return jsonify({"error": "TokenAlreadyExists"})
        user_settings.token = generate_token()
        session.commit()
        return jsonify({"error": "OK"})


class Q(Resource):

    def get(token, src):
        src = src.replace(gv.url_path_separation, '/')  # конвертируем C:;;dir;;dir2 в нормальный формат с /
        src_split = os.path.split(src)

        real = sf.token_to_login(token)
        if real:
            if sf.available_user_addresses(real, address_dir=src):
                if src_split[-1] and os.path.isfile(src):
                    pass      # file
                else:
                    pass  # folder
                # serve folder or file

            else:
                return jsonify({'error': 'CredentialError'})
        else:
            return jsonify({'error': 'CredentialError'})

    def post(self):
        pass
