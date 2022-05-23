"""
@File : file_info_test.py
@Date : 2022/5/20 10:46
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import datetime
import hashlib
import zipfile
import os

from uuid import uuid4

from pathlib import Path

file_path = Path(r'D:\Python\Project\testProject\RMCPerformance\test_file\1223.zip')

file_path2 = Path(r'\\192.168.1.59\Images\DY012029-1-1.zip')


# print(os.path.getsize(file_path))
# print(file_path.stat().st_size)
# print(file_path.name)
# print(file_path.suffix[1:])
#
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 计算hash

def compute_file_hash(path):
	m = hashlib.md5()
	with open(path, 'rb') as fh:
		while True:
			data = fh.read(8192)
			if not data:
				break
			m.update(data)
		hash_value = m.hexdigest()
	return hash_value


# print(compute_file_hash(file_path))

# 文件压缩
src_dir = r'D:\Python\Project\testProject\RMCPerformance\test_file\dicomfile'


def zip_file(source_directory, zip_name):
	# zip_name = src_dir +'.zip'
	with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
		for dir_path, dir_names, file_names in os.walk(source_directory):
			f_path = dir_path.replace(source_directory, '')
			f_path = f_path and f_path + os.sep or ''
			for file_name in file_names:
				z.write(os.path.join(dir_path, file_name), f_path + file_name)


temp_dir = r'D:\Python\Project\testProject\RMCPerformance\test_file'
file_name = str(uuid4())


#  随机写文本文件
def make_txt(source_director, file_name):
	txt_path = os.path.join(source_director, file_name)
	if not os.path.exists(txt_path):
		os.makedirs(txt_path)
	with open(os.path.join(txt_path, file_name + '.txt'), 'w') as f:
		f.write(file_name)
	return os.path.join(txt_path, file_name + '.txt')

# 删除指定后缀文件
# def remove_files()

if __name__ == "__main__":
	# zip_file(src_dir, '2.zip')

	make_txt(temp_dir, file_name)
