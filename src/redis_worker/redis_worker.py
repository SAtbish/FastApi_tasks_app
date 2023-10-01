from ast import literal_eval

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_NAME, REDISMAXPULL
from redis import asyncio as aioredis
from redis.exceptions import ResponseError, DataError

r = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def getbuiltin_method(method, val):
    if method == 'list':
        return literal_eval(val)
    elif method == 'bool':
        if val == 'True':
            return True
        return False
    else:
        try:
            return getattr(__builtins__, method)(val)
        except Exception as e:
            return __builtins__[method](val)


class RWrapper:
    def __init__(self, uuid=None):
        self.uuid = uuid
        self.r = r

    async def get_redis(self, keys):
        """
        :param keys: list of redis keys
        :return: dict {key:val ...}
        """
        dict_data = {}  # Here will lay default settings
        for key in keys:
            key = key.decode("utf-8")
            try:
                _, param, type_value = key.split(':')
                if type_value == 'NoneType':
                    continue
            except ValueError:
                raise ValueError("Trying to get more than one key."
                                 "Implemented only for uuid:key:type named keys."
                                 "Passed key is {}".format(key))
            try:
                dict_data = await self.put_key(
                    param,
                    getbuiltin_method(type_value, (await self.r.get(key)).decode("utf-8")),
                    dict_data
                )

            except ResponseError as e:
                if 'WRONGTYPE' in repr(e):
                    raise ValueError("Tried to get more than one key, "
                                     "one of which is a {}".format(type_value))

        return dict_data

    async def put_key(self, param, value, dict_little={}):
        params = param.split('.', 1)
        if len(params) == 1:
            dict_little[params[0]] = value
        else:
            dict_little[params[0]] = await self.put_key(params[1], value, dict_little.get(params[0], {}))
        return dict_little

    async def pull(self, id, start=0, end=0):
        if end == 0:
            end = await self.r.llen(id)
        if not start:
            start = 0
        if end > start + REDISMAXPULL:
            end = start + REDISMAXPULL
        li = await self.r.lrange(id, start, end)
        return li, end

    async def get_one_key(self, key):
        key = key.decode("utf-8")
        _, _, type_value = key.split(':')
        try:
            value = getbuiltin_method(type_value, self.r.get(key).decode("utf-8"))

            return value
        except ResponseError:
            redis_type = await self.r.type(key).decode()
            if redis_type == 'list':
                return await self.pull(key)[0]
            else:
                raise AttributeError('{}.val() not implemented'.format(redis_type))

    async def search(self, search_string):
        return await self.r.keys(search_string)

    async def delete(self, keys):
        for key in keys:
            await self.r.delete(key)

    async def ping(self):
        try:
            return await self.r.ping()
        except Exception as _:
            return False

    def __getattr__(self, name):
        setattr(self, name, Getter(self.uuid, name))
        return getattr(self, name)


class Getter(RWrapper):

    def __init__(self, uuid=0, name=''):
        super().__init__(uuid)
        self.uuid = uuid
        self.__name__ = name

    def __comp__(self, d):
        *_, name = self.__name__.split('.')
        for key in d.keys():
            if key == name:
                return d[key]
            elif isinstance(d[key], dict):
                return self.__comp__(d[key])
        return {}

    async def val(self):
        keys = await self.keys_list()
        if len(keys) > 1:

            default_dict = await self.get_redis(self.r.keys(':'.join(('defaults', self.__name__))))
            result = {**default_dict, **(await self.get_redis(keys))}
            return self.__comp__(result)
        else:
            key = await self.r.keys('defaults' + self.__name__ + ':*')
            if key:
                result = await self.get_one_key(key)
                return result
            else:
                return None

    async def keys_list(self):
        search_string = ':'.join((self.uuid, self.__name__)) if self.uuid else self.__name__
        return await self.r.keys(search_string + ':*') or await self.r.keys(search_string + '*')

    async def set(self, val):
        if isinstance(val, dict):
            for key in val.keys():
                self.__getattr__(key).set(val[key])
        else:
            try:
                await self.r.set(':'.join((self.uuid, self.__name__)) + ':' + type(val).__name__, val)
            except DataError:
                await self.r.set(':'.join((self.uuid, self.__name__)) + ':' + type(val).__name__, val.__str__())
        await self.r.save()

    def __getattr__(self, name):
        setattr(self, name, Getter(self.uuid, '.'.join((self.__name__, name))))
        return getattr(self, name)

    def __call__(self):
        return self.val()

    def __str__(self):
        return self.__name__

    async def rem(self):
        keys = await self.keys_list()
        await self.delete(keys)


rw = RWrapper(REDIS_NAME)


async def check_availability():
    return await rw.ping()
