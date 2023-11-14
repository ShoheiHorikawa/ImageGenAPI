import logging
from openai import OpenAI
import io
import base64
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# OpenAIクライアントの初期化
api_path = "api_key.txt"
with open(api_path, mode="r", encoding="utf-8") as f:
    api_key = f.read()
openai_client = OpenAI(api_key=api_key)

# Slackトークンの読み込み
slack_bot_token_path = "slack_bot_token.txt"
with open(slack_bot_token_path, mode="r", encoding="utf-8") as f:
    bot_token = f.read()

slack_app_token_path = "slack_app_token.txt"
with open(slack_app_token_path, mode="r", encoding="utf-8") as f:
    app_token = f.read()

# Slackアプリの初期化
app = App(token=bot_token)

# ログ設定
logging.basicConfig(filename='api_responses.log', level=logging.INFO, format='%(asctime)s: %(message)s')


def generate_image(prompt):
    if not prompt:
        raise ValueError("プロンプトが空です。")

    response = openai_client.images.generate(
        model="dall-e-3",
        prompt="必ず英語プロンプトで画像作成してください。\n"+prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json"
    )
    logging.info(f"API Response: {response}")
    image_b64 = response.data[0].b64_json
    binary_data = base64.b64decode(image_b64)
    revised_prompt = response.data[0].revised_prompt  # 修正されたプロンプトを取得
    return binary_data, revised_prompt


@app.event("message")
def handle_message_events(body, say, context):
    # ユーザーからのメッセージを取得
    prompt = body.get("event", {}).get("text", "")
    user_id = body.get("event", {}).get("user", "")

    if prompt:
        # 画像生成
        try:
            say("画像生成中です。少々お待ちください。。。")
            image_data, revised_prompt = generate_image(prompt)
            # メモリ内の画像データを使用してSlackに画像を送信
            with io.BytesIO(image_data) as image_io:
                app.client.files_upload(
                    channels=user_id, # ダイレクトメッセージとしてユーザーに送信
                    file=image_io,
                    filename="image.png"
                )
            # 修正されたプロンプトを送信
            say(f"修正されたプロンプト: {revised_prompt}")
        except Exception as e:
            say(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
