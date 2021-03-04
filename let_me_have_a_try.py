from orm.model import Model
from orm.fields import StringField, IntField


class User(Model):
    __table__ = 'users'
    __database__ = 'test1'
    id = IntField(primary_key=True)
    password = StringField(ddl='varchar(200)')
    name = StringField(ddl='varchar(50)')


u = User(id=6, password='123456', name='xiaoming')

u.save()

# a = User.filter()
# print(a)







