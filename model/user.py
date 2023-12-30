import cherrypy

from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean
from sqlalchemy import or_


from model import Base

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True)
    password = Column(String(128), default=None)
    firstname = Column(String(32))
    lastname = Column(String(32))
    prefix = Column(String(16))
    phone = Column(String(24))
    address = Column(String(128))
    address2 = Column(String(128))
    city = Column(String(32))
    state = Column(String(32))
    zipcode = Column(String(16))
    country = Column(String(32))

    status = Column(String(16))
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(email='{self.email}', firstname='{self.firstname}', lastname='{self.lastname}')"

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        if not self.password:
            raise EmptyPassword()
        if not pwd_context.verify(password, self.password):
            raise InvalidPassword()
        return True

    @property
    def firstlast(self):
        return f'{self.firstname} {self.lastname}'


def userfilter(db, value, limit=5, is_comm=False):
    items = value.split(' ')
    if not value.strip():
        return []
    or_filters = []
    and_filters = []

    cols = (User.firstname, User.lastname, User.email)
    for i in items:
        for c in cols:
            or_filters.append(c.like(f'%{i}%'))

    if is_comm:
        and_filters.append(User.commission_class.is_not(None))
    users = db.query(User).filter(or_(*or_filters), *and_filters).limit(limit).all()
    return users


def get_user(db, user_id=None, email=None):
    if user_id:
        return db.query(User).filter(User.id == user_id).one_or_none()
    elif email:
        return db.query(User).filter(User.email == email).one_or_none()
    else:
        if 'user' not in cherrypy.session:
            raise cherrypy.HTTPRedirect(f'{cherrypy.request.script_name}/auth/login/')
        return db.query(User).filter(User.id == cherrypy.session['user'].id).one_or_none()


class InvalidPassword(Exception):
    pass


class EmptyPassword(Exception):
    pass
