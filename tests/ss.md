     return self._clients[role]

...:
In [3]: manager = ModelManager(_settings)
In [4]: first = manager.get_role(ModelTag.research)
In [5]: second = manager.get_role(ModelTag.research)
In [6]: print(first is second)
True
In [7]:
