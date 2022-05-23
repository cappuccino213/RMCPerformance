"""
@File : config.py
@Date : 2022/5/18 9:44
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import socket


# 获取本地ip地址
def get_ipaddress():
	try:
		csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		csock.connect(('8.8.8.8', 80))
		(addr, port) = csock.getsockname()
		csock.close()
		return addr
	except socket.error:
		return "127.0.0.1"


"""locust参数"""
LOCUST_CONF = {"TEST_HOST": "http://192.168.1.18:8212",
			   "SHOW_URL": get_ipaddress(),
			   "SHOW_PORT": 8186}

"""script参数"""

if __name__ == "__main__":
	print(get_ipaddress())
