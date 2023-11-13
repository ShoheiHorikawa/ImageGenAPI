from openai import OpenAI
import io
import base64
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

api_path = "api_key.txt"
with open(api_path, mode="r", encoding="utf-8") as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)

app = App(token="")

SLACK_APP_TOKEN = ""

def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json"
    )
    image_b64 = response["data"][0]["b64_json"]
    binarry_data = base64.b64decode(image_b64)
    return binarry_data

@app.event("message")
def handle_message_events(body, say, client):
    # ユーザーからのメッセージを取得
    prompt = body.get("event", {}).get("text", "")
    user_id = body.get("event", {}).get("user", "")

    # 画像生成
    image_data = generate_image(prompt)

    # メモリ内の画像データを使用してSlackに画像を送信
    with io.BytesIO(image_data) as image_io:
        client.files_upload(
            channels=user_id, # ダイレクトメッセージとしてユーザーに送信
            file=image_io,
            filename="image.png"
        )

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN).start