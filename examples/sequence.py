from uuid import uuid4

from flf import FLF

#short example using a session
class Sequence(FLF):
    def __init__(self):
        self.sessions = {}

    def begin(self):
        id = str(uuid4())
        self.sessions[id] = 0

        return {
            "session_id": id
        }

    def generate(self, session_id):
        #TODO: how to return error (session id not provided) instead of 500?
        num = self.sessions[session_id]
        self.sessions[session_id] += 1
        return str(num)

    def end(self, session_id):
        del self.sessions[session_id]


if __name__ == "__main__":
    import threading
    import base64

    from protopost import protopost_client as ppcl

    #start FLF tree in a new thread so we can test
    threading.Thread(target=lambda: Sequence().listen(8123), daemon=True).start()

    URL = "http://127.0.0.1:8123"

    def get_and_decode(session_id):
        output = ppcl(URL + "/generate", {"session_id": session_id})[0]
        return base64.b64decode(output).decode("utf8")

    #start a new session
    session_id = ppcl(URL + "/begin")["session_id"]

    #generate using that session identifier
    for _ in range(10):
        print(get_and_decode(session_id))

    ppcl(URL + "/end", {"session_id": session_id})
