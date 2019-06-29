import hashlib

SPECIAL_STR = "cxk"                     # MD5加密特殊字符串
MD5_LEN = 10                            # 加密组合长度

def encode(password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf-8'))
    final_password = hl.hexdigest()
    hl.update(SPECIAL_STR.encode(encoding='utf-8'))
    special = hl.hexdigest()
    final_password = final_password[: -MD5_LEN] + special[-MD5_LEN:]
    return final_password