import torch

class KVCache:
    def __init__(self, max_length):
        self.max_length = max_length
        self.cache = {}

    def update_cache(self, key, value):
        if key not in self.cache:
            self.cache["key"] = key
            self.cache["value"] = value
        else:
            self.cache["key"] = torch.cat([self.cache["key"], key], dim=1)
            self.cache["value"] = torch.cat([self.cache["value"], value], dim=1)