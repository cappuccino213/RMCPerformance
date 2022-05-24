"""
@File : test_script.py
@Date : 2022/5/18 9:45
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import datetime
import logging
import os

from locust import task, between, constant
from requests_toolbelt import MultipartEncoder

from locust_request_encapsulation import *

from mock_data import *


class RequestDiagnosisUser(HttpRequestUser):
	# wait_time = between(3, 5)
	wait_time = constant(2)
	user_token = ''
	request_header = {}

	# 执行请求前先获取token
	def on_start(self):
		logging.info("新增用户，先获取token.....")
		api = '/openapi/auth/gettoken'
		header = {'content-type': 'application/json'}
		body = {"LoginName": "AdminOrg1_6",
				"password": "e10adc3949ba59abbe56e057f20f883e"}
		res_data = self.http_request(api, header, '获取token', json_body=body)
		self.user_token = res_data.json()['data']['token']
		# 设置token
		self.request_header = {'userToken': self.user_token}

	# 上传诊断文件\提交诊断申请
	@task
	def request_diagnosis(self):
		# 上传影像
		upload_api = '/openapi/File/dicom/Upload'
		upload_headers = self.request_header  # 拿到获取的token放进headers
		# 生成一个zip文件
		test_file = FileData().generate_zip(r'./test_file/temp')
		test_file_info = FileData().get_file_info(Path(test_file))
		m_body = MultipartEncoder(
			fields={'key': FileData().compute_file_hash(test_file),
					'FileDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					'SliceSize': test_file_info['file_size'],
					'TotalSize': test_file_info['file_size'],
					'Startindex': '0',
					'Extension': test_file_info['file_extension'],
					'file': (
						test_file_info['file_name'],
						open(test_file, 'rb'),
						'application/octet-stream')}
		)
		upload_headers['content-type'] = m_body.content_type
		# self.http_request(upload_api, headers, '上传文件', data_body=m_body)
		result = self.http_request(upload_api, upload_headers, '上传文件', data_body=m_body).json()

		# 上传成功后，调用诊断申请接口
		if result['code'] == 200 and result['data']['isFinish']:
			request_headers = self.request_header
			request_api = '/openapi/Diagnosis/Add'
			request_headers['content-type'] = 'application/json'

			patient_info = DiagnosisData().mock_patient_info()
			observation_info = DiagnosisData().mock_observation_info()

			j_body = {'name': patient_info['name'],
					  'sex': patient_info['sex'],
					  'age': patient_info['age'],
					  'ageUnit': '岁',
					  'accessionNumber': observation_info['accession_number'],
					  'idCard': patient_info['id_card'],
					  'symptom': observation_info['symptom'],
					  'clinicDiagnosis': observation_info['clinic_diagnosis'],
					  'patientClass': observation_info['patient_class'],
					  'serviceCenterUID': 'c25700bb-e081-4341-9593-acc3010d63d4',
					  'fileURL': result['data']['url'],
					  'FileUID': result['data']['fileUID'],
					  'hasWrite': 0,
					  'serviceSectID': observation_info['service_sect_id'],
					  'technicianDate': observation_info['technician_date'],
					  'exambodypart': observation_info['exam_body_part'],
					  'procedureName': observation_info['procedure_name'],
					  'UniqueID': f'{uuid4()}'}

			logging.info(j_body)
			self.http_request(request_api, request_headers, '申请诊断', json_body=j_body)

	# 获取诊断结果
	@task(0)
	def get_diagnosis_result(self):
		api = '/openapi/Diagnosis/GetResultByUniqueID'
		# headers = {'UserToken': self.user_token}
		headers = self.request_header
		params = {'uniqueID': '92b32e70-7D34-5e9f-A15C-31CEaCf26bAd'}
		self.http_request(api, headers, '获取诊断结果', params=params)

	# 执行完任务后执行，每个user执行一次
	def on_stop(self):
		pass


def start():
	import subprocess
	cli = f"locust -f test_script.py -H {LOCUST_CONF['TEST_HOST']} --web-host {LOCUST_CONF['SHOW_URL']} -P {LOCUST_CONF['SHOW_PORT']}"
	try:
		cl = subprocess.Popen(cli, stdout=subprocess.PIPE, shell=True)
		print(cl.stdout.readlines())  # 打印控制台信息
	except Exception as e:
		raise str(e)


if __name__ == '__main__':
	start()
