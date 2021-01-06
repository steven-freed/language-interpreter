
class TypeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UndeclaredException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ParamException(Exception):
    def __init__(self, msg):
        super().__init__(msg)