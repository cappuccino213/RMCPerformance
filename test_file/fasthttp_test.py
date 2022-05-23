"""
@File : fasthttp_test.py
@Date : 2022/5/20 10:32
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from locust import task, between, constant
from requests_toolbelt import MultipartEncoder

from http_request import *


# 申请诊断用户
class RequestDiagnosisUser(FastHttpRequestUser):
	# wait_time = between(3, 5)
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
		res_data = self.fast_http_request(api, header, '获取token', json_body=body)
		self.user_token = res_data.json()['data']['token']
		# 设置token
		self.request_header = {'userToken': self.user_token}

	# 上传诊断文件
	@task
	def upload_file(self):
		api = '/openapi/File/dicom/Upload'
		headers = self.request_header  # 拿到获取的token放进headers
		m_body = MultipartEncoder(
			fields={'key': 'cc788d84f04ab7712d5eed60b41d8668',
					'FileDate': '2022-05-19 01:59:59',
					'SliceSize': '202000',
					'TotalSize': '202000',
					'Startindex': '0',
					'Extension': 'zip',
					'file': (
						'DY012029.zip',
						open(r'D:\Python\Project\testProject\RMCPerformance\test_file\DY012029.zip', 'rb'),
						'application/octet-stream')}
		)
		headers['content-type'] = m_body.content_type
		result = self.fast_http_request(api, headers, '上传文件', data_body=m_body)
		logging.info(result)
	# 申请远程诊断

	# 获取诊断结果
	@task(0)
	def get_diagnosis_result(self):
		api = '/openapi/Diagnosis/GetResultByUniqueID'
		# headers = {'UserToken': self.user_token}
		headers = self.request_header
		params = {'uniqueID': '92b32e70-7D34-5e9f-A15C-31CEaCf26bAd'}
		self.fast_http_request(api, headers, '获取诊断结果', params=params)


if __name__ == "__main__":
	pass
