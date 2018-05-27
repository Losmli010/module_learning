import os

#查询目录和文件信息
print(os.path.abspath(__file__))                       #返回当前文件所在的完整路径
curdir = os.path.dirname(os.path.abspath(__file__))    #返回当前文件所在的目录
print(curdir)
file_path = os.path.join(curdir, "osModule.py")        # 使用目录名和文件名构成一个路径字符串
print(file_path)
print(os.path.dirname(file_path))                      # 查询路径中包含的目录
print(os.path.split(file_path))                        # 将路径分割成目录和文件名两个部分，放在一个元组中返回
print(os.path.basename(file_path))                     # 查询路径中包含的文件名
print(os.path.exists(curdir))                          # 查询文件或目录是否存在,存在返回True

print(os.path.getsize(file_path))                      # 查询文件大小
print(os.path.getatime(file_path))                     # 查询文件上一次读取的时间
print(os.path.getmtime(file_path))                     # 查询文件上一次修改的时间

print(os.path.isfile(file_path))                       # 路径是否指向常规文件
print(os.path.isdir(curdir))                           # 路径是否指向目录文件

# 文件管理
print(os.listdir(curdir))                              #返回目录中的所有文件
newDir = os.path.join(curdir, "test")
# os.mkdir(newDir)                                       #创建新目录
# os.rmdir(newDir)                                       #删除空目录,目录内不能有文件存在,否则报错
filename = os.path.join(curdir, "test.txt")
file = open(filename, "w")                             #创建新文件
file.close()
# os.remove(filename)                                    #删除文件
# os.rename(src, dst)                                    #重命名文件，src和dst为两个路径，分别表示重命名之前和之后的路径
print(os.stat(filename))                               #查看path所指向文件的附加信息
print(os.getcwd())                                     #返回当前工作路径

#文件遍历
for root, dirs, files in os.walk(curdir):
    print(root, dirs, files)

import glob

print(glob.glob(os.path.join(curdir, "*")))            #返回当前目录下所有文件的完整目录
print(glob.glob("*.py"))                               #返回当前目录下所有Python文件名

import shutil

# shutil.copy(filename, "test_copy.txt")                 #复制文件

import sys

print(sys.argv)
print(sys.platform)                                     #获取当前系统平台
print(sys.version)
print(sys.path)
