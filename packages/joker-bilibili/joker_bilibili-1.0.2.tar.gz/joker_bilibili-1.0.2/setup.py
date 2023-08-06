import os
import setuptools

setuptools.setup(
      name='joker_bilibili',
      version='1.0.2',  # 版本号
      keywords='joker',
      description='Hello,welcome to my field',
      long_description=open(
          os.path.join(
              os.path.dirname(__file__),
              'README.rst')
      ).read(),
      author='jokerLang',
      author_email='524276169@qq.com',
      packages=setuptools.find_packages(),
      license='MIT'
      )
