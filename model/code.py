import string
import random

from sqlalchemy import Column
from sqlalchemy.types import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from model import Base


class Code(Base):
    __tablename__ = 'codes'
    id = Column(String(37), primary_key=True)
    type = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    stamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed = Column(DateTime(timezone=True))

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = self.gen_code()
        super(Code, self).__init__(**kwargs)

    def __repr__(self):
        return 'Code(id={}, type={}, email={})'.format(self.id, self.type, self.email)

    def gen_code(self):
        abc123 = string.ascii_uppercase + string.ascii_lowercase + '0123456789'
        return ''.join(random.choice(abc123) for i in range(37))

    def process(self):
        self.processed = func.now()

    user_from_type = relationship('User',
                                  primaryjoin="Code.type.like('invite-' + type_coerce(remote(foreign(User.id)), types.String))",
                                  viewonly=True, uselist=False)
