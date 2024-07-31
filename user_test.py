import requests
import concurrent.futures
import json
import time

# URL của API
generate_url = "http://127.0.0.1:8000/generate"
result_url = "http://127.0.0.1:5000/result/"

input_texts = [
    "Hãy viết một bài luận ngắn về tác động của mạng xã hội đến giới trẻ.",
    "Giải thích khái niệm 'trí tuệ nhân tạo' một cách dễ hiểu.",
    "Nếu bạn có thể thay đổi một điều về thế giới, bạn sẽ chọn điều gì?",
    "Hãy so sánh và phân tích hai tác phẩm văn học nổi tiếng mà bạn biết.",
    "Viết một đoạn code Python để tạo ra một danh sách chứa các số nguyên từ 1 đến 10.",
    "Hãy tưởng tượng bạn là một nhà khoa học. Bạn sẽ nghiên cứu về vấn đề gì?",
    "Tại sao chúng ta cần bảo vệ đa dạng sinh học?",
    "Hãy viết một câu chuyện cười về một con robot.",
    "Nếu bạn có thể du hành thời gian, bạn sẽ muốn đến thời kỳ nào?",
    "Hãy phân tích một bài báo mà bạn vừa đọc về biến đổi khí hậu.",
    "Hãy viết một bài luận ngắn về tác động của mạng xã hội đến giới trẻ.",
    "Giải thích khái niệm 'trí tuệ nhân tạo' một cách dễ hiểu.",
    "Nếu bạn có thể thay đổi một điều về thế giới, bạn sẽ chọn điều gì?",
    "Hãy so sánh và phân tích hai tác phẩm văn học nổi tiếng mà bạn biết.",
    "Viết một đoạn code Python để tạo ra một danh sách chứa các số nguyên từ 1 đến 10.",
    "Hãy tưởng tượng bạn là một nhà khoa học. Bạn sẽ nghiên cứu về vấn đề gì?",
    "Tại sao chúng ta cần bảo vệ đa dạng sinh học?",
    "Hãy viết một câu chuyện cười về một con robot.",
    "Nếu bạn có thể du hành thời gian, bạn sẽ muốn đến thời kỳ nào?",
    "Hãy phân tích một bài báo mà bạn vừa đọc về biến đổi khí hậu."
]


# Hàm gửi yêu cầu generate và nhận request_id
def send_request(input_text):
    response = requests.post(generate_url, json={"inputs": input_text,
                                                 "parameters": {"max_length": 1000, "temperature": 0.7, "top_p": 0.9}})
    if response.status_code == 200:
        return response.json().get("generated_text")
    else:
        print(f"Lỗi khi gửi yêu cầu: {response.json()}")
        return None


# Hàm kiểm tra kết quả từ request_id
def get_result(request_id, timeout=60):
    if request_id is None:
        return None

    start_time = time.time()
    while True:
        response = requests.get(result_url + request_id)
        if response.status_code == 200:
            result = response.json()
            if "output_text" in result:
                return request_id, result["output_text"]
            elif "error" in result:
                return request_id, result["error"]
        else:
            print(f"Lỗi khi kiểm tra kết quả: {response.json()}")
            return request_id, None

        # Kiểm tra timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return request_id, "Yêu cầu đã hết thời gian chờ."

        # Chờ một khoảng thời gian ngắn trước khi kiểm tra lại
        time.sleep(3)


# Thực hiện 10 yêu cầu song song
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Gửi yêu cầu generate
    future_to_request_id = {executor.submit(send_request, text): text for text in input_texts}

    # Nhận request_id
    request_ids = []
    for future in concurrent.futures.as_completed(future_to_request_id):
        request_id = future.result()
        request_ids.append(request_id)
        print(f"Request ID nhận được: {request_id}")

    # # Kiểm tra kết quả từ request_id
    # future_to_result = {executor.submit(get_result, request_id): request_id for request_id in request_ids}
    #
    # # In kết quả nhận được
    # for future in concurrent.futures.as_completed(future_to_result):
    #     request_id, result = future.result()
    #     print(f"Kết quả của ID {request_id}: {result}")
