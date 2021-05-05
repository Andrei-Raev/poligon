import sqlalchemy
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm

SqlAlchemyBase = dec.declarative_base()


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    avator = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)


conn_str = f'sqlite:///db/users.db?check_same_thread=False'
engine = sqlalchemy.create_engine(conn_str, echo=False)
SqlAlchemyBase.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)
session = Session()

# sss = User()
# sss.email = 'a@a.a'
# sss.name = 'Андрей'
# sss.surname = 'Раев'
# sss.nickname = 'Nerrow'
# sss.avator = 'ava'
# sss.hashed_password = "Moe123moe123"
#
# session.add(sss)
# session.commit()

# for element in session.query(Jobs).filter((Jobs.work_size < 20) & (Jobs.is_finished == 0)):
#     print(element)
