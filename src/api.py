from flask import Flask
from main import execute

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
  return execute()


if __name__ == '__main__':
  app.run()
