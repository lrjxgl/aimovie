import json
import base64
def arr2str(data):
    # 将列表转换成JSON字符串
    json_str = json.dumps(data)

    # 将JSON字符串转换成字节串
    json_bytes = json_str.encode('utf-8')

    # 对字节串进行Base64编码
    base64_bytes = base64.b64encode(json_bytes)

    base64_str = base64_bytes.decode('utf-8')
    return base64_str