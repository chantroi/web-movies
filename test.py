from detafs import DetaFs

fs = DetaFs("c0a1xmuzlhz_9ukoxqAYL8nr8w9hPai2kPbyf7qnAaGC")

f = fs.open("Áo Cưới.mp4")
with open("video2.mp4", "wb") as w:
    w.write(f.read())
