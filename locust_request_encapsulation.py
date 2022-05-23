"""
@File : http_request.py
@Date : 2022/5/19 10:03
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import logging

from locust import FastHttpUser, HttpUser

from config import LOCUST_CONF


# 定义fast http user的类
class FastHttpRequestUser(FastHttpUser):
	abstract = True

	# post/get方法封装,使得调阅更简单
	def fast_http_request(self, api, headers, api_name, json_body=None, data_body=None, params=None):
		"""
		:param api:
		:param headers:
		:param api_name:
		:param json_body:
		:param data_body:
		:param params:
		:return:
		"""
		try:
			if json_body:
				logging.info('入参为json')
				res = self.client.post(path=LOCUST_CONF['TEST_HOST'] + api, headers=headers, json=json_body,
									   name=api_name)
			elif data_body:
				logging.info('入参为data')
				res = self.client.post(path=LOCUST_CONF['TEST_HOST'] + api, headers=headers, data=data_body,
									   name=api_name)
			else:
				logging.info('入参为params')
				res = self.client.get(path=LOCUST_CONF['TEST_HOST'] + api, headers=headers, params=params,
									  name=api_name)
			logging.info(f"申请-api:{api}|返回结果-:{res.json()}")
			return res
		except Exception as e:
			logging.info(str(e))
			return str(e)


# 定义http user的类
class HttpRequestUser(HttpUser):
	abstract = True

	# post/get方法封装,使得调阅更简单
	def http_request(self, api, headers, api_name, json_body=None, data_body=None, params=None):
		"""
		:param api:
		:param headers:
		:param api_name:
		:param json_body:json格式的body
		:param data_body:对象的入参
		:param params:
		:return:
		"""
		try:
			if json_body:
				# logging.info('入参为json')
				res = self.client.post(url=LOCUST_CONF['TEST_HOST'] + api, headers=headers, json=json_body,name=api_name)
			elif data_body:
				# logging.info('入参为data')
				res = self.client.post(url=LOCUST_CONF['TEST_HOST'] + api, headers=headers, data=data_body,
									   name=api_name)
			else:
				# logging.info('入参为params')
				res = self.client.get(url=LOCUST_CONF['TEST_HOST'] + api, headers=headers, params=params,
									  name=api_name)
			logging.info(f"-->申请-api:{api}")
			logging.info(f"<--返回结果-:{res.json()}")
			return res
		except Exception as e:
			logging.info(str(e))


if __name__ == "__main__":
	pass
