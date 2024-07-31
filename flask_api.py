from flask import Flask, request, jsonify
import torch
from queue import Queue
import logging
from uuid import uuid4
from threading import Thread
from model.hg_inference import HuggingfaceInference

app = Flask(__name__)

# Cài đặt logging
logging.basicConfig(level=logging.INFO)

# Hàng đợi yêu cầu
request_queue = Queue()
results = {}

model = HuggingfaceInference(
    model_path=r"E:\Model\llama3.1")
stt, msg = model.load_model()


# Hàm xử lý yêu cầu
# Hàm xử lý yêu cầu
def process_request(request_id, request_data):
    try:
        input_text = request_data.get("inputs")

        if not input_text:
            results[request_id] = {"error": "Dữ liệu đầu vào rỗng"}
            return
        if stt:
            output_text = model.infer(input_text)
            results[request_id] = {"output_text": output_text}
            logging.info(output_text)
        else:
            results[request_id] = {"error": "Lỗi khi load model"}
            return
    except Exception as e:
        logging.error(e)
        results[request_id] = {"error": "Lỗi xảy ra trong quá trình xử lý yêu cầu"}


# Hàm xử lý đa luồng
def worker():
    with app.app_context():
        while True:
            request_id, request_data = request_queue.get()
            process_request(request_id, request_data)
            request_queue.task_done()


# Thêm yêu cầu vào hàng đợi và trả về ID yêu cầu
@app.route("/generate", methods=["POST"])
def generate_text():
    user_request = request.get_json()
    logging.info(user_request)

    # Lấy địa chỉ IP của client
    client_ip = request.remote_addr
    logging.info(f"Client IP: {client_ip}")

    request_id = str(uuid4())
    results[request_id] = {"status": "processing", "client_ip": client_ip}
    logging.info(f"{request_id} | {user_request}")
    request_queue.put((request_id, user_request))

    return jsonify({"request_id": request_id, "client_ip": client_ip})


# API để kiểm tra trạng thái yêu cầu
@app.route("/result/<request_id>", methods=["GET"])
def get_result(request_id):
    result = results.get(request_id)

    if not result:
        return jsonify({"error": "Request ID không hợp lệ"}), 404

    return jsonify(result)


if __name__ == "__main__":
    # Khởi động worker
    thread = Thread(target=worker)
    thread.daemon = True
    thread.start()

    # Khởi động ứng dụng
    app.run(host='0.0.0.0', debug=True)
