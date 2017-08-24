# coding: utf-8

import json
import base64

import tornado.ioloop
from models import Session, User
from tornado.web import Application, RequestHandler


class BasicAuthMixin(object):
    class AuthError(Exception):
        pass

    def get_authenticated_user(self, auth_func, realm):
        try:
            return self.authenticate_user(auth_func, realm)
        except self.AuthError:
            self.send_auth_challenge(realm)

    def send_auth_challenge(self, realm):
        header = 'Basic realm="{}"'.format(realm.replace('\\', '\\\\').replace('"', '\\"'))
        self.set_status(401)
        self.set_header('www-authenticate', header)
        self.finish()

        return False

    def authenticate_user(self, auth_func, realm):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            raise self.AuthError()

        auth_data = auth_header.split(None, 1)[-1]
        auth_data = base64.b64decode(auth_data).decode('ascii')
        username, password = auth_data.split(':', 1)

        user = auth_func(username, password)
        if not user:
            raise self.AuthError()

        return user


class MainHandler(BasicAuthMixin, RequestHandler):
    def initialize(self, db):
        self.db = db

    def prepare(self):
        self.current_user = self.get_authenticated_user(
            auth_func=self._auth_by_creds,
            realm='Protected'
        )

    def post(self):
        try:
            benefit_type = float(self.get_argument('benefitType'))
        except (ValueError, TypeError):
            self.send_error(400, reason='benefitType is not a number')
            return

        params = json.loads(self.get_argument('params'))

        results = []
        for ds in self.current_user.data_sets:
            try:
                res = eval(ds.expression, {}, {'benefitType': benefit_type, **params})
            except Exception as err:
                res = str(err)

            results.append((ds.expression, res))

        self.write(dict(results))

    def _auth_by_creds(self, login, password):
        return self.db.query(User).filter_by(login=login, password=password).one_or_none()


def make_app():
    session = Session()
    return Application([
        (r'/', MainHandler, {'db': session}),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
