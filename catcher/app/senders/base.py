from abc import abstractmethod


class Sender:
    required_fields = []

    def __init__(self, **kwargs):
        for key in self.required_fields:
            if key not in kwargs:
                raise ValueError(f'no required key {key}')
        self.config = kwargs

    @abstractmethod
    def send(self, message):
        raise NotImplementedError
