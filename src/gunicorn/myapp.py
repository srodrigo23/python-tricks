
# gunicorn -w 4 myapp:app
# https://gunicorn.org/

def app(environ, start_response):
    data=b'Hello, World\n'
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])