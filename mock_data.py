"""
@File : mock_data.py
@Date : 2022/5/20 16:22
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import hashlib
import os
import zipfile
import random
import datetime

from pathlib import Path
from uuid import uuid4

from faker import Faker

from data_dictionary import *


# 模拟文件的相关数据
class FileData:
	@staticmethod
	def get_file_info(file_path: Path):
		return {"file_name": file_path.name,  # 文件名
				"file_size": str(file_path.stat().st_size),  # 文件大小
				"file_extension": file_path.suffix[1:]}  # 文件扩展名

	# 计算文件哈希值
	@staticmethod
	def compute_file_hash(file_path):
		m = hashlib.md5()
		with open(file_path, 'rb') as fh:
			while True:
				data = fh.read(8192)
				if not data:
					break
				m.update(data)
			hash_value = m.hexdigest()
		return hash_value

	# 随机生成zip压缩包文件
	@staticmethod
	def generate_zip(src_dir):
		# 随机生成压缩的txt文本
		if not os.path.exists(src_dir):
			os.makedirs(src_dir)
		file_name = str(uuid4())
		file_path = os.path.join(src_dir, file_name)
		txt_file = os.path.join(file_path + '.txt')
		with open(txt_file, 'w') as f:
			f.write(file_name)

		# 随机文件压缩成zip包
		zip_name = file_path + '.zip'
		with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
			for dir_path, dir_names, file_names in os.walk(src_dir):
				f_path = dir_path.replace(src_dir, '')
				f_path = f_path and f_path + os.sep or ''
				for fn in file_names:
					if fn == file_name + '.txt':
						z.write(os.path.join(dir_path, fn), f_path + fn)

		# 压缩完，删除原txt文件
		if os.path.exists(txt_file):
			os.remove(txt_file)
		return zip_name


# 模拟诊断申请数据
fake = Faker('zh_CN')


class DiagnosisData:

	# 生成身份证号
	@staticmethod
	def mock_id(birthday):
		region_code = random.choice(CODE_LIST)
		bird_code = birthday.strftime('%Y%m%d')
		sequence_code = str(random.randint(100, 300))
		# 前17位地区码+生日+3位顺序号
		id_card = region_code + bird_code + sequence_code
		# 计算校验码
		weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
		check_code = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5',
					  '9': '3',
					  '10': '2'}  # 校验码映射
		count = 0
		for i in range(0, len(id_card)):
			count = count + int(id_card[i]) * weight[i]
		id_card = id_card + check_code[str(count % 11)]
		return id_card

	# 模拟患者信息
	@staticmethod
	def mock_patient_info():
		# fake = Faker('zh_CN')
		birthday = fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=90)
		age = datetime.date.today().year - birthday.year
		return {'name': fake.name(),
				'sex': random.choice([1, 2]),
				'age': age,
				'birthday': f'{birthday}',
				'id_card': DiagnosisData.mock_id(birthday)}

	# 模拟检查信息
	@staticmethod
	def mock_observation_info():
		service_sect_id = random.choice(['CR', 'MR', 'CT', 'DX', 'MG', 'XA', 'RF'])

		# 根据检查类型挑选出对应的检查信息
		def pick_observation_by_sect_id(ssid, observation_list):
			for observation in observation_list:
				if observation['ServiceSectID'] == ssid:
					return observation

		observation_dict = pick_observation_by_sect_id(service_sect_id, OBSERVATION_SAMPLE)
		# 检查时间，取当前时间5小时以内的任意时间
		technician_date = ((datetime.datetime.now()-datetime.timedelta(minutes=random.randint(0,5))).strftime("%Y-%m-%d %H:%M:%S"))
		return {'accession_number': f"{datetime.datetime.now().strftime('%H%M%S%f')}-{random.randint(1, 100)}",
				'symptom': f'病人主诉{fake.text(max_nb_chars=200)}',
				'patient_class': random.choice([1, 2, 3, 4]),
				'service_sect_id': service_sect_id,
				'exam_body_part': observation_dict['ExamBodyPart'],
				'procedure_name': observation_dict['ProcedureName'],
				'technician_date': technician_date,
				'clinic_diagnosis': f'临床诊断{fake.text(max_nb_chars=200)}'}



if __name__ == "__main__":
	# fd = FileData()
	# file = fd.generate_zip(r'D:\Python\Project\testProject\RMCPerformance\test_file\temp')
	# print(fd.get_file_info(Path(file)))
	# fake = Faker('zh_CN')
	# print(DiagnosisData().mock_id(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=90)))
	# print(DiagnosisData().mock_patient_info())
	print(DiagnosisData().mock_observation_info())
