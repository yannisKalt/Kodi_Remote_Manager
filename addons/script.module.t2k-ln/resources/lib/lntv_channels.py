import requests
import string
import random
import time
import uuid
from base64 import b64encode, b64decode
from hashlib import md5


class lntvChannels(object):
    def __init__(self, config, user=""):
        self.config = config
        self.user = user
        self.host = "195.154.26.54:8080/data/i/"
        self.package_name = "com.streams.androidnettv"
        self.sha1 = "EA:32:78:87:BF:88:8F:AD:C9:88:81:09:9A:31:69:F7:BE:E9:91:CE"
        self.user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1; AFTM Build/LMY47O)"
        self.s = requests.Session()

    @staticmethod
    def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    def config_var(self, var):
        return b64decode(self.config[var][1:]).decode("utf-8")

    def get_channel_list(self):
        login_url = self.config_var("YXBpS2V5TGluazQ2")
        time_stamp = str(int(time.time() * 1000))
        allow = b64encode(
            "{time_md5}${package_name}${apk_cert_sha1}${time_stamp}${user_id}${provider}".format(
                time_md5=md5(time_stamp.encode()).hexdigest(),
                package_name=self.package_name,
                apk_cert_sha1=self.sha1,
                time_stamp=time_stamp,
                user_id=self.user,
                provider="2",
            ).encode()
        )
        data = {"ALLOW": allow}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.user_agent,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        req = requests.Request("POST", login_url, headers=headers, data=data)
        prq = req.prepare()
        r = self.s.send(prq)
        _key = r.json().get("funguo")
        _meta = r.headers["etag"].split(":")[0]
        _enc = r.headers["etag"].split(":")[1]
        _hash, _host = b64decode(_enc + "=" * (-len(_enc) % 4)).decode("utf-8").split("|")
        if _host.startswith("http"):
            self.host = _host
        else:
            self.host = "http://" + _host
        check = "1"
        if not self.user:
            self.register_user(_key)
            check = "11"
        list_url = self.host + "data.nettv/"
        headers = {
            "Referer": self.config_var("SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"),
            "Meta": _meta,
            "Authorization": self.config_var("amFnX3Ryb3JfYXR0X2Vu"),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.user_agent,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = {"provider": "2", "time": time_stamp, "user_id": self.user, "check": check, "key": _key, "version": "30"}
        req = requests.Request("POST", list_url, headers=headers, data=data)
        prq = req.prepare()
        r = self.s.send(prq)
        try:
            return r.json()
        except:
            return ""

    def register_user(self, funguo):
        user_url = self.host + "adduserinfo.nettv/"
        time_stamp = str(int(time.time() * 1000))
        _string2 = b"|".join(
            [b"19", b64encode("30".encode()), b64encode(time_stamp.encode()), b64encode("000000000000000".encode()), b64encode(str(uuid.uuid4()).encode())]
        )
        _id = b"|".join(
            [
                md5(time_stamp.encode()).hexdigest().encode(),
                b64encode(self.package_name.encode()),
                b64encode(self.sha1.encode()),
                b64encode("AFTM".encode()),
                b64encode(_string2),
            ]
        )
        data = {
            "id": b64encode(_id),
            "api_level": "21",
            "android_id": self.id_generator(16),
            "time": time_stamp,
            "device_name": "AFTM",
            "provider": "2",
            "device_id": "unknown",
            "key": funguo,
            "version": "4.6 (30)",
        }
        headers = {
            "Referer": self.config_var("SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"),
            "Authorization": self.config_var("amFnX3Ryb3JfYXR0X2Vu"),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.user_agent,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        req = requests.Request("POST", user_url, headers=headers, data=data)
        prq = req.prepare()
        r = self.s.send(prq)
        self.user = str(r.json().get("user_id"))
