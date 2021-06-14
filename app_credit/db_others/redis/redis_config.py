import pickle
import redis


class Redis_Cache:

    def __init__(self, host, port, db, password):
        self.cache = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    def set(self, key, value, serialization=False):
        if serialization:
            self.cache.set(key, pickle.dumps(value))
        else:
            self.cache.set(key, value)

    def get(self, key, serialization=False):
        result = self.cache.get(key)
        if serialization and result is not None:
            result = pickle.loads(result)
        return result

    def delete(self, key):
        return self.cache.delete(key)

    def flush(self):
        self.cache.flushall()

    def keys(self):
        return self.cache.keys()


redis = Redis_Cache(
    host='192.168.99.100',
    port=6379,
    db=0,
    password='redispass'
)