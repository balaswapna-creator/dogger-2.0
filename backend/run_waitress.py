from waitress import serve
from dogger.wsgi import application

if __name__ == '__main__':
    from waitress import serve
    from dogger.wsgi import application
    print("Starting Waitress server on http://0.0.0.0:8001")
    serve(application, host='0.0.0.0', port=8001, threads=4)