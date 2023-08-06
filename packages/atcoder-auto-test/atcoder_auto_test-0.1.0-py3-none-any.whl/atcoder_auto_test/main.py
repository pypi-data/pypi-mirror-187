import os
import shutil
from fnmatch import filter
from io import BytesIO

import numpy as np
from google.cloud import vision
from PIL import Image, ImageGrab

TMP_DIR = os.path.join(os.path.expanduser("~"), ".atcoder/tmp")
TEST_DATA_DIR = os.path.join(TMP_DIR, "test")
os.makedirs(TEST_DATA_DIR, exist_ok=True)

CONTEST_URL_CAPTURE = os.path.join(TMP_DIR, "contest_url.png")
CAPTURE_POSITION_TEXT = os.path.join(TMP_DIR, "contest_url_position.txt")
PREV_URL_TEXT = os.path.join(TMP_DIR, "prev_url.txt")


class URLNotFoundError(Exception):
    pass


def detect_contest_url(screenshot):
    url = ""
    position = (-1, -1, -1, -1)  # (left, top, right, bottom)

    # テキスト検出（Google Cloud Vision API）
    client = vision.ImageAnnotatorClient()
    bytes_content = BytesIO()
    screenshot.save(bytes_content, format="PNG")
    image = vision.Image(content=bytes_content.getvalue())
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # URLを検出（atcoder.jp/contests/〜で始まるテキストを検出する）
    for text in texts:
        if text.description.startswith("atcoder.jp/contests/"):
            url = "https://" + text.description
            vertices = text.bounding_poly.vertices
            position = (vertices[0].x, vertices[0].y, vertices[2].x, vertices[2].y)
            break
        else:
            continue

    if url == "" and position == (-1, -1, -1, -1):
        raise URLNotFoundError("URLが見つかりませんでした")
    else:
        return url, position


def test():
    # 提出コード（注意：Pythonファイルが1つしかないことを仮定しています）
    answer_code = filter(os.listdir(os.getcwd()), "*.py")[0]

    # スクリーンショットを取得
    screenshot = ImageGrab.grab()

    # 前回のスクリーンショットと変わらなければ、そのままテストを実行して終了する
    if os.path.exists(CONTEST_URL_CAPTURE):
        prev_screenshot = Image.open(CONTEST_URL_CAPTURE)
        prev_position = tuple(map(int, open(CAPTURE_POSITION_TEXT).read().split()))
        if np.all(
            np.array(screenshot.crop(prev_position)) == np.array(prev_screenshot)
        ):
            # テストを実行
            os.system(f"oj t -c 'python {answer_code}' -d {TEST_DATA_DIR}")
            return

    try:
        # コンテストURLと位置を取得
        url, position = detect_contest_url(screenshot)
    except URLNotFoundError:
        # URLが見つからなかった場合は終了
        print("URLが見つかりませんでした")
        return

    # コンテストURLの位置と画像を保存（問題ページの遷移判定に使用）
    with open(PREV_URL_TEXT, "w") as f:
        f.write(url)
    with open(CAPTURE_POSITION_TEXT, "w") as f:
        f.write(" ".join(map(str, position)))
    screenshot.crop(position).save(CONTEST_URL_CAPTURE)

    # テストケースをダウンロード
    shutil.rmtree(TEST_DATA_DIR)
    os.system(f"oj d {url} -d {TEST_DATA_DIR}")

    # テストを実行
    os.system(f"oj t -c 'python {answer_code}' -d {TEST_DATA_DIR}")


def submit():
    # 提出コード（注意：Pythonファイルが1つしかないことを仮定しています）
    answer_code = filter(os.listdir(os.getcwd()), "*.py")[0]
    # 提出
    os.system(f"oj s -y {open(PREV_URL_TEXT).read()} {answer_code}")
