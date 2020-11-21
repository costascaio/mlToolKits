from flask import jsonify, request, Flask
import os
from database import Dataset
from utils import Database, Csv
from concurrent.futures import ThreadPoolExecutor

HTTP_STATUS_CODE_SUCCESS = 200
HTTP_STATUS_CODE_SUCCESS_CREATED = 201
HTTP_STATUS_CODE_NOT_ACCEPTABLE = 406
HTTP_STATUS_CODE_CONFLICT = 409

DATABASE_API_HOST = "DATABASE_API_HOST"
DATABASE_API_PORT = "DATABASE_API_PORT"

MESSAGE_RESULT = "result"

DATABASE_URL = "DATABASE_URL"
DATABASE_PORT = "DATABASE_PORT"
DATABASE_NAME = "DATABASE_NAME"
DATABASE_REPLICA_SET = "DATABASE_REPLICA_SET"

FILENAME = "datasetName"
URL_FIELD_NAME = "datasetURI"

FIRST_ARGUMENT = 0

MESSAGE_INVALID_URL = "invalid url"
MESSAGE_DUPLICATE_FILE = "duplicate file"
MESSAGE_DELETED_FILE = "deleted file"

PAGINATE_FILE_LIMIT = 20

MICROSERVICE_URI_GET = "/api/learningOrchestra/v1/dataset/"
MICROSERVICE_URI_GET_PARAMS = "?query={}&limit=10&skip=0"

app = Flask(__name__)


@app.route("/files", methods=["POST"])
def create_file():
    print("teste3", flush=True)

    database_connector = Database(
        os.environ[DATABASE_URL],
        os.environ[DATABASE_REPLICA_SET],
        os.environ[DATABASE_PORT],
        os.environ[DATABASE_NAME])

    file_downloader = Csv(database_connector)

    database = Dataset(database_connector, file_downloader)

    #try:
    database.add_file(request.json[URL_FIELD_NAME], request.json[FILENAME])

    '''except Exception as error_message:

        if error_message.args[FIRST_ARGUMENT] == MESSAGE_INVALID_URL:
            return (
                jsonify({MESSAGE_RESULT: error_message.args[FIRST_ARGUMENT]}),
                HTTP_STATUS_CODE_NOT_ACCEPTABLE,
            )

        elif error_message.args[FIRST_ARGUMENT] == MESSAGE_DUPLICATE_FILE:
            return (
                jsonify({MESSAGE_RESULT: error_message.args[FIRST_ARGUMENT]}),
                HTTP_STATUS_CODE_CONFLICT,
            )'''

    return (
        jsonify({
            MESSAGE_RESULT:
                MICROSERVICE_URI_GET +
                request.json[FILENAME] +
                MICROSERVICE_URI_GET_PARAMS}),
        HTTP_STATUS_CODE_SUCCESS_CREATED,
    )


@app.route("/files/<filename>", methods=["GET"])
def read_files(filename):
    database_connector = Database(
        os.environ[DATABASE_URL],
        os.environ[DATABASE_REPLICA_SET],
        os.environ[DATABASE_PORT],
        os.environ[DATABASE_NAME])

    file_downloader = Csv(database_connector)
    database = Dataset(database_connector, file_downloader)

    limit = int(request.args.get("limit"))
    if limit > PAGINATE_FILE_LIMIT:
        limit = PAGINATE_FILE_LIMIT

    file_result = database.read_file(
        filename, request.args.get("skip"), limit, request.args.get("query")
    )

    return jsonify({MESSAGE_RESULT: file_result}), HTTP_STATUS_CODE_SUCCESS


@app.route("/files", methods=["GET"])
def read_files_descriptor():
    database_connector = Database(
        os.environ[DATABASE_URL],
        os.environ[DATABASE_REPLICA_SET],
        os.environ[DATABASE_PORT],
        os.environ[DATABASE_NAME])

    file_downloader = Csv(database_connector)
    database = Dataset(database_connector, file_downloader)

    return jsonify(
        {MESSAGE_RESULT: database.get_files(
            request.args.get("type"))}), HTTP_STATUS_CODE_SUCCESS


@app.route("/files/<filename>", methods=["DELETE"])
def delete_file(filename):
    database_connector = Database(
        os.environ[DATABASE_URL],
        os.environ[DATABASE_REPLICA_SET],
        os.environ[DATABASE_PORT],
        os.environ[DATABASE_NAME])

    file_downloader = Csv(database_connector)
    database = Dataset(database_connector, file_downloader)

    thread_pool = ThreadPoolExecutor()
    thread_pool.submit(database.delete_file, filename)

    return jsonify(
        {MESSAGE_RESULT: MESSAGE_DELETED_FILE}), HTTP_STATUS_CODE_SUCCESS


if __name__ == "__main__":
    app.run(host=os.environ[DATABASE_API_HOST],
            port=int(os.environ[DATABASE_API_PORT]), debug=True)
