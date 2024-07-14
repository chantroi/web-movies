---
app_name: File Stream
tagline: "Deta Drive's files explorer, support streaming large file."
media: []
ported_from: ""
works_with: []
---

https://<url>/<drive: optional>

# API

List files:
GET https://<url>/<drive>/<folder|root>

Streaming file:
GET https://<url>/<drive>/<folder>/<file>

Delete file:
DELETE https://<url>/<drive>/<folder>/<file>
