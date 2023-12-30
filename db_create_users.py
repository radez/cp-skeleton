from model.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import parse_config

cfg = parse_config('PROJECTNAME.conf')

engine = create_engine(cfg['db']['url'], echo=True)
session = sessionmaker(bind=engine)()


users = [
    # Admin
    {'id': 1, 'email': 'admin@example.com', 'firstname': 'Admin', 'lastname': 'User', 'admin': True},
    # Non-admin
    {'id': 2, 'email': 'user@example.com', 'firstname': 'User', 'lastname': 'Name'},
]
session.add_all(map(lambda x: User(**x), users))
for user in users:
    user = session.query(User).filter(User.id == user['id']).one()
    user.set_password('insecurepassword')
session.commit()
