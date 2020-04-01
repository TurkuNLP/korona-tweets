from flask import current_app, g


class DummyDB:
    def query(self, q):
        return [
            { 'id': '1234', 'text': 'foo bar' },
            { 'id': '5678', 'text': 'baz quuz' }
        ]

    def close(self):
        pass


def get_db():
    if 'db' not in g:
        g.db = DummyDB()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
