import s3fs
import deta
from environment import deta_key, s3_endpoint, s3_key, s3_secret


class Storage:
    def __init__(self):
        self.deta = deta.Deta(deta_key).Drive("files")
        self.s3 = s3fs.S3FileSystem(
            key=s3_key,
            secret=s3_secret,
            endpoint_url=s3_endpoint,
        )

    def upload_to_deta(self, file_name, file_data, content_type="video/mp4"):
        self.deta.put(file_name, file_data, content_type=content_type)

    def upload_to_s3(self, file_name, file_data, content_type="video/mp4"):
        if content_type == "video/mp4":
            s3_path = f"bosuutap/video/{file_name}.mp4"

        elif content_type == "image/jpeg":
            s3_path = f"bosuutap/image/{file_name}.jpg"

        elif content_type == "audio/mpeg":
            s3_path = f"bosuutap/audio/{file_name}.mp3"
        else:
            s3_path = f"bosuutap/files/{file_name}"
        with self.s3.open(s3_path, "wb") as s3_file:
            s3_file.write(file_data)
        self.s3.setxattr(s3_path, copy_kwargs={"ContentType": content_type})

    def upload(self, file_name, file_data, content_type="video/mp4"):
        self.upload_to_deta(file_name, file_data, content_type)
        self.upload_to_s3(file_name, file_data, content_type)

    def delete_from_deta(self, file_name):
        self.deta.delete(file_name)

    def delete_from_s3(self, file_name):
        if file_name.endswith(".mp4"):
            s3_path = f"bosuutap/video/{file_name}.mp4"

        elif file_name.endswith(".jpg"):
            s3_path = f"bosuutap/image/{file_name}.jpg"

        elif file_name.endswith(".mp3"):
            s3_path = f"bosuutap/audio/{file_name}.mp3"
        else:
            s3_path = f"bosuutap/files/{file_name}"
        self.s3.rm(s3_path)

    def delete(self, file_name):
        self.delete_from_deta(file_name)
        self.delete_from_s3(file_name)
