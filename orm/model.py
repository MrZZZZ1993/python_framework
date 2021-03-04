from orm.fields import Field
from orm.sql_conn import BaseDB


class ModelMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name

        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields

        if '__database__' not in attrs:
            attrs['__database__'] = 'default'

        attrs['db'] = BaseDB('root', 'chuxuan19930327', database=attrs['__database__'])

        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'%s' instance has no attribute '%s'" % (self.__class__.__name__, key))

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                setattr(self, key, value)
        return value

    @classmethod
    def filter(cls, where='', *args):
        sql = 'select * from %s %s' % (cls.__table__, 'where %s' % where if where else '')
        print(sql)
        res = cls.db.execute(sql)
        return res

    def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))

        names = ','.join(map(str, self.__fields__)) + ',' + self.__primary_key__
        sql = f'insert into {self.__table__} ({names}) values (7, 123, 123)'
        sql = 'insert into users (password,name,id) values (7, 123, 123)'
        print(sql)

        values = ','.join(map(str, args))

        self.db.execute(sql)

