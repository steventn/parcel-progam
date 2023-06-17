class HashMap:
    def __init__(self, size):
        self.size = size
        self.map = [[] for _ in range(size)]

    def _hash_function(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        index = self._hash_function(key)
        bucket = self.map[index]
        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)  # Update existing key-value pair
                return
        bucket.append((key, value))  # Add new key-value pair

    def get(self, key):
        index = self._hash_function(key)
        bucket = self.map[index]
        for existing_key, existing_value in bucket:
            if existing_key == key:
                return existing_value
        return None  # Key not found

    def remove(self, key):
        index = self._hash_function(key)
        bucket = self.map[index]
        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                return

    def keys(self):
        keys_list = []
        for bucket in self.map:
            for key, _ in bucket:
                keys_list.append(key)
        return keys_list
