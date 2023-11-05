import openai
import base64

api_path = "api_key.txt"
with open(api_path, mode="r", encoding="utf-8") as f:
    api_key = f.read()


def read_prompt(fname):
    f = open(fname)
    content = f.read()
    f.close()
    return content


def access_openai(prompt_value, image_size, num):
    openai.api_key = api_key
    prompt = read_prompt("prompt.txt")

    response = openai.Image.create(
        prompt = prompt + prompt_value,
        n = num,
        size = image_size,
        response_format = "b64_json"
    )
    tstamp = response["created"]
    # image_url = response["data"][0]["url"] #URL出力にしたとき(単一出力)
    # for ob in response["data"]: #URL出力にしたとき(複数出力)
    #     print("¥n" + ob.url)
    # image_b64 = response["data"][0]["b64_json"] #json出力にしたとき(単一出力)
    # binarry_data = base64.b64decode(image_b64)
    # with open(f"result/{tstamp}_created_image.png", "wb") as f:
    #     f.write(binarry_data)
    for number, data in zip(range(num), response["data"]): #json出力にしたとき(複数出力)
        binarry_data = base64.b64decode(data["b64_json"])
    with open(f"result/{tstamp}_created_image_{number}.png", "wb") as f:
        f.write(binarry_data)
    print("ファイルに保存しました。:")


if __name__ == "__main__":
    input_text = input("テキストを入力してください。")
    image_size_small = "256x256"
    image_size_midium = "512x512"
    image_size_large = "1024x1024"
    gen_num = 1
    access_openai(input_text, image_size_small, gen_num)