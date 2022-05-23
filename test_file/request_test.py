"""
@File : request_test.py
@Date : 2022/5/19 17:24
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import requests

from requests_toolbelt import MultipartEncoder

from config import LOCUST_CONF


def upload_file():
	api = '/openapi/File/dicom/Upload'
	headers = {'userToken': '5c8ee30b-c0c2-4b7b-9853-ae9a00e0abde'}
	m_body = MultipartEncoder(
		fields={'key': 'cc788d84f04ab7712d5eed60b41d8668',
				'FileDate': '2022-05-19 01:59:59',
				'SliceSize': '2000001',
				'TotalSize': '2000001',
				'Startindex': '0',
				'Extension': 'zip',
				'file': ('DY012029.zip', open('DY012029.zip', 'rb'), 'application/octet-stream')}
	)
	headers['content-type'] = m_body.content_type
	res = requests.request('POST', LOCUST_CONF['TEST_HOST'] + api, data=m_body, headers=headers)
	print(res.json())


# logging.info(f"申请-api:{api}|返回结果data:{res.json()}")


if __name__ == "__main__":
	upload_file()
