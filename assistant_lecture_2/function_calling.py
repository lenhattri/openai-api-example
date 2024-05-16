# Nhập các thư viện cần thiết
from openai import OpenAI
import requests
import time
import json

from dotenv import load_dotenv
import os
load_dotenv()
# Khai báo khóa API của OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")

# Hàm hiển thị đối tượng JSON
def show_json(obj):
   print(json.dumps(json.loads(obj.model_dump_json()),indent=4))

# Tạo một client OpenAI với khóa API đã khai báo
client = OpenAI(api_key=openai_api_key)

# Khai báo ID của Assistant
assistant_id = assistan_id = os.getenv("ASSISTANT_ID")

# Lấy thông tin của Assistant tương ứng
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

# Tạo một thread mới
thread = client.beta.threads.create()

# Tạo một tin nhắn trong thread
message = client.beta.threads.messages.create(
    thread_id= thread.id,
    role='user',
    content="Thành phố New York hiện tại có phải ban đêm không?"
)

# Khai báo API Key của TimezoneDB. Link: https://timezonedb.com/

timezonedb_api_key = os.getenv("TIMEZONEDB_API_KEY")



def get_timezone(location):
   """
   Hàm để lấy thời gian dựa trên zone code
   Tham số:
      - location(string): Địa điểm. Ví dụ: Asia/Ho_Chi_Minh
   """
   try:
      response = requests.get(f"http://api.timezonedb.com/v2.1/get-time-zone?key={timezonedb_api_key}&format=json&by=zone&zone={location}")
      return response.json()
   except Exception as e:
      print(f"There was an error: {e}")
      return None

# Tạo một run mới để chạy Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id= assistant.id
)

# Hàm chạy và liên tục lắng nghe kết quả của run
def run_and_wait(run):
   # Liên tục cập nhật trạng thái mới nhất của Run hiện tại
   while(run.status == 'in_progress' or run.status == 'queued' or run.status  == 'requires_action'):
      run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id= thread.id)
      #Delay
      time.sleep(0.5)
      #Nếu nhận thấy cần gọi function
      if(run.status == 'requires_action'):
         #Lấy thông tin tổng quát về function 
         toolcall = run.required_action.submit_tool_outputs.tool_calls[0]
         # Lấy tên của function
         name = toolcall.function.name
         arguments = json.loads(toolcall.function.arguments)
         print(f"Function Calling: {name}")
         # Chạy hàm và lưu kết quả vào biến timezone
         timezone = get_timezone(**arguments)
         print(f"Fromatted time: {str(timezone['formatted'])}")
         # Submit kết quả để run tiếp tục chạy
         run = client.beta.threads.runs.submit_tool_outputs(
            run_id= run.id,
            thread_id= thread.id,
            tool_outputs= [
               {
                  "tool_call_id": toolcall.id,
                  "output": str(timezone['formatted'])
               }
            ]
            )
   return client.beta.threads.messages.list(thread_id=thread.id)

# Chạy hàm run_and_wait và lấy kết quả
message = run_and_wait(run)

# Lấy nội dung phản hồi từ Assistant
respond = message.data[0].content[0].text.value
print(respond)
