"""
@File : test_script.py
@Date : 2022/5/18 9:45
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from locust import task, constant, HttpUser
from requests_toolbelt import MultipartEncoder

from locust_request_encapsulation import *


# 申请诊断用户
class RequestDiagnosisUser(HttpUser):
	wait_time = constant(2)
	user_token = ''
	request_header = {}

	# 执行请求前先获取token
	def on_start(self):
		logging.info("新增用户，先获取token.....")
		api = '/openapi/auth/gettoken'
		header = {'content-type': 'application/json'}
		# data = {"LoginName": "orgAdmin1",
		body = {"LoginName": "AdminOrg1_6",
				"password": "e10adc3949ba59abbe56e057f20f883e"}
		res_data = self.client.post(url='http://192.168.1.18:8212' + api, headers=header, name='获取token', json=body)
		self.user_token = res_data.json()['data']['token']
		logging.info(f"{self.user_token}")
		# 设置token
		self.request_header = {'userToken': self.user_token}

	# 上传诊断文件
	@task
	def upload_file(self):
		api = '/openapi/File/dicom/Upload'
		headers = self.request_header
		m_body = MultipartEncoder(
			fields={'key': 'cc788d84f04ab7712d5eed60b41d8668',
					'FileDate': '2022-05-19 01:59:59',
					'SliceSize': '2000011',
					'TotalSize': '2000011',
					'Startindex': '0',
					'Extension': 'zip',
					'file': (
					'DY012029.zip', open(r'/test_file/DY012029.zip', 'rb'),
					'application/octet-stream')}
		)

		headers['content-type'] = m_body.content_type
		res = self.client.request('POST', LOCUST_CONF['TEST_HOST'] + api, name='上传文件', data=m_body, headers=headers)
		# logging.info(f"申请-api:{api}|返回结果-status:{res.status},data:{res.json()}")
		logging.info(f"申请-api:{api}|返回结果:{res.json()}")

# 申请远程诊断


def start():
	import subprocess
	cli = f"locust -f test_script_httpuser.py -H {LOCUST_CONF['TEST_HOST']} --web-host {LOCUST_CONF['SHOW_URL']} -P {LOCUST_CONF['SHOW_PORT']}"
	try:
		cl = subprocess.Popen(cli, stdout=subprocess.PIPE, shell=True)
		print(cl.stdout.readlines())  # 打印控制台信息
	except Exception as e:
		raise str(e)


if __name__ == '__main__':
	start()
