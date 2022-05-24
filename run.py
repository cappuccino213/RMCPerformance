"""
@File : run.py
@Date : 2022/5/18 9:45
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import subprocess

from config import LOCUST_CONF


def start():
	cli = f"locust -f test_script.py -H {LOCUST_CONF['TEST_HOST']} --web-host {LOCUST_CONF['SHOW_URL']} -P {LOCUST_CONF['SHOW_PORT']}"
	try:
		cl = subprocess.Popen(cli, stdout=subprocess.PIPE, shell=True)
		print(cl.stdout.readlines())  # 打印控制台信息
	except Exception as e:
		raise str(e)


if __name__ == "__main__":
	start()
