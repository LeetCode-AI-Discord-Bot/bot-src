from run_code_request_body import RunCodeRequestBody

import os
import subprocess
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

TEMP_CODE_FOLDER = "temp_code"
PROCESS_TIME_OUT = 15
TEMP_CODE_NAME_SUFFIX = "temp_code.py"
os.makedirs(os.path.join(os.getcwd(), TEMP_CODE_FOLDER), exist_ok=True)


def save_code(code: str, thread_id: str) -> (bool, str):
    try:
        file_name = f"{thread_id}-{TEMP_CODE_NAME_SUFFIX}"
        file_path = os.path.join(os.getcwd(), TEMP_CODE_FOLDER, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return (True, file_path)
    except Exception as e:
        return (False, None)


def run_python_code(file_path: str) -> str:
    proc = subprocess.Popen("python " + file_path, stdout=subprocess.PIPE, shell=True)
    print(proc)
    try:
        out, _ = proc.communicate(timeout=PROCESS_TIME_OUT)
        os.unlink(file_path)
        return out.decode("utf-8")
    except subprocess.TimeoutExpired:
        proc.kill()
        os.unlink(file_path)
        return f"Python process Time out after {PROCESS_TIME_OUT} seconds"


@app.route("/run-python", methods=["POST"])
def handle_run_python():
    try:
        body = RunCodeRequestBody(request.json, request.json["code"], request.json["thread_id"])
        success, file_path = save_code(body.code, body.thread_id)
        if not success:
            return {"error": "Failed to save code"}, 400

        return {"result": run_python_code(file_path)}
    except Exception as e:
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=False)
