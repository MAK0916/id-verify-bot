from flask import Flask, request, jsonify
import requests, random

app = Flask(__name__)

T = "s=d6b251b37d9642aeff0fb8798f269411&t=1749210471&lm=&lf=4&sk=b4ae90129143285c712db864ae48c59d&mt=1749210471&rc=&v=2.0&a=1"
Q = "u=360H3537885490&n=&le=&m=&qid=3537885490&im=1_t01923d359dad425928&src=pcw_iaa&t=1"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json or {}
    name = data.get("name", "")
    idcard = data.get("idcard", "")
    if not name or not idcard:
        return jsonify(success=False, message="缺少姓名或身份证号"), 400

    boundary = "----WebKitFormBoundary" + ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 16))
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="realName"\r\n\r\n'
        f"{name}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="idCardNumber"\r\n\r\n'
        f"{idcard}\r\n"
        f"--{boundary}--\r\n"
    )

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "T": T,
        "Q": Q,
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://fun.360.cn/user/setting/account"
    }

    try:
        r = requests.post("https://fun.360.cn/iaa/api/user/identityVerify", headers=headers, data=body.encode(), timeout=10)
        res = r.json()
        code = res.get("code")
        msg = res.get("msg", "")
        if code == 0 and msg == "操作成功":
            return jsonify(success=True, message="验证通过")
        else:
            return jsonify(success=False, message=f"验证失败：{msg}")
    except Exception as e:
        return jsonify(success=False, message=f"请求异常：{str(e)}"), 500

@app.route("/", methods=["GET"])
def home():
    return "验证 API 正常运行中", 200
