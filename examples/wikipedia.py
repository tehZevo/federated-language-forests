import wikipedia

from flf import FLF

class Wikipedia(FLF):
    def generate(self, article=None):
        return wikipedia.summary("Natural Langauge Processing")

if __name__ == "__main__":
    import threading
    import base64

    from protopost import protopost_client as ppcl

    #start FLF tree in a new thread so we can test
    threading.Thread(target=lambda: Wikipedia().listen(8123), daemon=True).start()

    output = ppcl("http://127.0.0.1:8123/generate")[0]
    print(base64.b64decode(output).decode("utf8"))
