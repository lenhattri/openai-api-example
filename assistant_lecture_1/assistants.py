from openai import OpenAI
from dotenv import load_dotenv

import time
import os

load_dotenv()
import json

def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

openai_api_key =  os.getenv("OPENAI_API_KEY")

assistan_id = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key= openai_api_key)

assistant = client.beta.assistants.retrieve(assistant_id=assistan_id)


thread = client.beta.threads.create()

messages = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

run = wait_on_run(run,thread)

messages = client.beta.threads.messages.list(thread_id=thread.id)
response = messages.data[0].content[0].text.value
# show_json(messages)
print(response)
