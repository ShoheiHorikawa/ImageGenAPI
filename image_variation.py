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


def access_openai(image_size, num):
    openai.api_key = api_key

    response = openai.Image.create_variation(
        image = open("image.png", "rb"),
        n = num,
        size = image_size,
        response_format = "b64_json"
    )
    tstamp = response["created"]
    for number, data in zip(range(num), response["data"]):
        binarry_data = base64.b64decode(data["b64_json"])
        with open(f"result/{tstamp}_variation_image_{tstamp}.png", "wb") as f:
            f.write(binarry_data)

    print("ファイルに保存しました。:")


if __name__ == "__main__":
    image_size_small = "256x256"
    image_size_midium = "512x512"
    image_size_large = "1024x1024"
    gen_num = 3
    access_openai(image_size_small, gen_num)