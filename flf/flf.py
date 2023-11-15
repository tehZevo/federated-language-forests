import base64

from protopost import ProtoPost

class FLF:
    def __init__(self):
        pass

    def _begin(self, data):
        return self.begin()

    def begin(self):
        pass

    def _update(self, sequences):
        #TODO: support other parameters from protopost data
        #coerce to list and decode each sequence to bytes

        if type(sequences) != list:
            sequences = [sequences]

        sequences = [base64.b64decode(seq) for seq in sequences]

        return self.update(sequences)

    def update(self):
        pass

    def _generate(self, data):
        #TODO: allow self.generate to return dict or something with `generations` field
        generations = self.generate(**data)
        if type(generations) != list:
            generations = [generations]

        #coerce each to bytes and base64 encode
        generations = [bytes(gen, "utf8") if type(gen) == str else gen for gen in generations]
        generations = [base64.b64encode(gen).decode("utf8") for gen in generations]

        return generations

    def generate(self):
        pass

    def _rollback(self, data):
        return self.rollback()

    def rollback(self):
        pass

    def _end(self, data):
        return self.end(**data)

    def end(self):
        pass

    def listen(self, port=80):
        #TODO: allow extra routes to be passed in
        routes = {
            "begin": lambda x: self._begin(x),
            "update":  lambda x: self._update(x),
            "generate":  lambda x: self._generate(x),
            "rollback":  lambda x: self._rollback(x),
            "end": lambda x: self._end(x),
        }

        ProtoPost(routes).start(port)
