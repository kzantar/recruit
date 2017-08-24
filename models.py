# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('mysql://root:root@0.0.0.0:3000/recruit')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(255))
    password = Column(String(255))

    data_sets = relationship('DataSet', backref='user')

    def __repr__(self):
        return f'<User(login={self.login})>'


class DataSet(Base):
    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    expression = Column(String(500))

    def __repr__(self):
        return f'<DataSet(expression={self.expression})>'


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()
    session.add_all([
        User(login='user_1', password='pass', data_sets=[
            DataSet(expression='(a+b+c)*benefitType'),
        ]),
        User(login='user_2', password='pass', data_sets=[
            DataSet(expression='(a+b)*benefitType'),
            DataSet(expression='(b+c)*benefitType'),
        ]),
        User(login='user_3', password='pass', data_sets=[
            DataSet(expression='a*benefitType'),
            DataSet(expression='(b+c)'),
            DataSet(expression='c*benefitType'),
        ]),
        User(login='user_4', password='pass', data_sets=[
            DataSet(expression='a*+-benefitType'),
            DataSet(expression='(b+d)'),
            DataSet(expression='*benefType'),
        ]),
    ])
    session.commit()
