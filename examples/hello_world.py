from flf import FLF

#doesn't require a session, simply generates `Hello world!` endlessly
class HelloWorld(FLF):
    def generate(self, **kwargs):
        return bytes("Hello world!", "utf8")

if __name__ == "__main__":
    import time
    import threading
    import base64

    from protopost import protopost_client as ppcl

    #start FLF tree in a new thread so we can test
    threading.Thread(target=lambda: HelloWorld().listen(8123), daemon=True).start()

    while True:
        #generate returns a list of outputs
        output = ppcl("http://127.0.0.1:8123/generate")[0]
        print(base64.b64decode(output).decode("utf8"))
        time.sleep(1)
