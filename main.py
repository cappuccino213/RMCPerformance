"""
@File : run.py
@Date : 2022/5/18 9:45
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import logging
import subprocess

from config import LOCUST_CONF,CMD_CONF


# 执行命令返回信息
def run_shell(command):
	"""
	:param command: 命令行
	:return: 返回执行结果
	"""
	try:
		stdout, stderr = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()
		return stdout
	except Exception as err:
		raise str(err)


# 运行locust的脚本
def start():
	# 先查历史locust进程
	exists_locust_process = run_shell("tasklist |findstr locust")
	if exists_locust_process:
		run_shell("TASKKILL /IM locust.exe /F")
	# 判断是什么模式运行
	if LOCUST_CONF['IF_WEBUI']:
		run_cmd = f"locust -f test_script.py -H {LOCUST_CONF['TEST_HOST']} --web-host {LOCUST_CONF['SHOW_URL']} -P {LOCUST_CONF['SHOW_PORT']}"
	else:
		run_cmd = f"locust -f test_script.py -H {LOCUST_CONF['TEST_HOST']} -u {CMD_CONF['USER_AMOUNT']} -r {CMD_CONF['SPAWN_RATE']} --run-time {CMD_CONF['RUN_TIME']} --stop-timeout {CMD_CONF['STOP_TIME']} --headless"
	message = run_shell(run_cmd)
	logging.info(message)


if __name__ == "__main__":
	start()
