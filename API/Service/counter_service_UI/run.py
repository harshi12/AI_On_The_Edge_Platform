from app import app
foo = ""

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--service_id')
parser.add_argument('--port')
args = parser.parse_args()
foo = args.service_id

if __name__ == "__main__":
    app.run(debug=False, host = '0.0.0.0', port = int(args.port))
