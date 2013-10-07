from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    local_a = 1
    local_b = 2
    import pdb
    pdb.set_trace()
    return 'hello world!'

if __name__ == '__main__':
    app.run()
