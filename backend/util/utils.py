
import os
from PIL import Image
import base64
from io import BytesIO


punctuation = '。！？.'
def is_ending_with_punctuation(sentence):

    # 检查句子是否为空
    if not sentence:
        return False
    # 判断最后一个字符是否是标点符号
    return sentence[-1] in punctuation


def deleteFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def video_frame_to_base64(video_frame)-> str:
    # 将 AVFrame 转换为 PIL 图像
    img = video_frame.to_image()
    # 保存图像到文件
    output_path = "./output_image.jpg"  # 设置文件名和路径
    img.save(output_path)  # 保存为 JPEG 格式
    # 创建一个 BytesIO 对象来保存图像
    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # 或者其他格式，如 PNG
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 现在 img_str 是 Base64 编码的图像字符串
    print("Base64 Image:", img_str)

    return img_str


def merge_frame(data) -> bytes:
    merged_bytes = b''
    print("merge_frame start")
    try:
        for frame in data:
            # 将每个 AudioFrame 转换为字节格式并添加到合并的字节数据中
            merged_bytes += bytes(frame.planes[0])

    except Exception as e:
        print("Error while merging", e)
    return merged_bytes