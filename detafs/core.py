from deta import Deta


class DetaFs:
    def __init__(self, access_key: str, folder: str = "files") -> None:
        self.deta = Deta(access_key)
        self.fs = self.deta.Drive(folder)
        self.db = self.deta.Base("detafs")
        if not self.db.get(folder):
            self.db.put({"key": folder, "list": []})
        self.folder = self.db.get(folder)

    def open(self, file: str):
        return self.fs.get(file)

    def put(self, file: str, data: bytes):
        self.folder["list"].append(file)
        self.db.put(self.folder)
        return self.fs.put(file, data)

    def remove(self, file: str):
        self.folder["list"].remove(file)
        self.db.put(self.folder)
        return self.fs.delete(file)

    def ls(self):
        return self.folder["list"]

    def listdir(self):
        files = self.fs.list()
        self.folder["list"] = files["names"]
        self.db.put(self.folder)
        return files["names"]

    def mkdir(self, folder: str):
        if self.db.get(folder):
            return False
        self.db.put({"key": folder, "list": []})
        return True

    def chdir(self, folder: str):
        self.fs = self.deta.Drive(folder)
        self.folder = self.db.get(folder)
