import qubesadmin

class ApiFormatter:

    def __init__(self, properties, rename: dict = None):
        self.properties = properties
        self.rename = {} if not rename else rename

    def to_dict(self, qube_object):
        result = {}
        for key in self.properties:
            value = getattr(qube_object, key)
            if isinstance(value, qubesadmin.label.Label):
                value = str(value)
            result[self.rename.get(key, key)] = value() if callable(value) else value
        return result
