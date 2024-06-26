from deta import Deta


class DetaFs:
    def __init__(self, access_key: str, folder: str = "files") -> None:
        self.deta = Deta(access_key)
        self.fs = self.deta.Drive(folder)

    def open(self, file: str):
        return self.fs.get(file)

    def put(self, file: str, data: bytes):
        return self.fs.put(file, data)

    def remove(self, file: str):
        return self.fs.delete(file)

    def ls(self):
        return self.listdir()

    def listdir(self):
        files = self.fs.list()
        return files["names"]
