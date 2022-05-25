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
LOCUST_CONF = {"IF_WEBUI": False,
			   "TEST_HOST": "http://192.168.1.18:8212",
			   "SHOW_URL": get_ipaddress(),
			   "SHOW_PORT": 8186}

"""script参数"""
# no web 模式参数
# user_amount:用户并发量/spawn_rate:生成率/run_time:运行时长/stop_time:停止时长
CMD_CONF = {"USER_AMOUNT": 20,
			"SPAWN_RATE": 5,
			"RUN_TIME": "30s",  # 1h30m  5m30s
			"STOP_TIME": 30}  # 单位秒

# STEP_TIME 步长时间，即每一步需要的时间
# STEP_LOAD 每步负载，即每一步需要增加的用户数量
# SPAWN_RATE 生成率，在这一步期间每秒钟启动的用户数量
# TIME_LIMIT 测试时长,单位秒
LOAD_SHAPE = {"STEP_TIME": 30,
			  "STEP_LOAD": 10,
			  "SPAWN_RATE": 10,
			  "TIME_LIMIT": 600}

if __name__ == "__main__":
	print(get_ipaddress())
