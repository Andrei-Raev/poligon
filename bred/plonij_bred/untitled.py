
# import sqlalchemy
# import sqlalchemy.ext.declarative as dec
# import sqlalchemy.orm as orm
#
# SqlAlchemyBase = dec.declarative_base()
#
#
# class User(SqlAlchemyBase):
#     __tablename__ = 'users'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     surname = sqlalchemy.Column(sqlalchemy.String)
#     name = sqlalchemy.Column(sqlalchemy.String)
#     age = sqlalchemy.Column(sqlalchemy.Integer)
#     position = sqlalchemy.Column(sqlalchemy.String)
#     speciality = sqlalchemy.Column(sqlalchemy.String)
#     address = sqlalchemy.Column(sqlalchemy.String)
#     email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
#     hashed_password = sqlalchemy.Column(sqlalchemy.String)
#
#     def __repr__(self):
#         return f'{self.name} {self.surname}'
#
#
# class Jobs(SqlAlchemyBase):
#     __tablename__ = 'jobs'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
#     job = sqlalchemy.Column(sqlalchemy.String)
#     work_size = sqlalchemy.Column(sqlalchemy.Integer)
#     collaborators = sqlalchemy.Column(sqlalchemy.String)
#     start_date = sqlalchemy.Column(sqlalchemy.DateTime)
#     end_date = sqlalchemy.Column(sqlalchemy.DateTime)
#     is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
#
#     def __repr__(self):
#         return f'<Job> {self.job}'
#
#
# conn_str = f'sqlite:///{input()}?check_same_thread=False'
# engine = sqlalchemy.create_engine(conn_str, echo=False)
# SqlAlchemyBase.metadata.create_all(engine)
# Session = orm.sessionmaker(bind=engine)
# session = Session()
#
# longest = set()
# for element in session.query(Jobs).all():
#     longest.add(len(element.collaborators.split(', ')))
# max_val = max(longest)
# iii = set()
#
# for element in session.query(Jobs).all():
#     if len(element.collaborators.split(', ')) == max_val:
#         iii.add(
#             session.query(User).filter((User.id == element.team_leader) & (User.name.notin_(['Venkat'])).first()).id)
#
# for element in session.query(User).filter(User.id.in_(list(iii))):
#     pass
