from setuptools import setup

setup(name='qs-qrcode',
      version='1.2',
      author='Q',
      author_email='tomhaoye@gmail.com',
      description='generate qrcode',
      long_description=open("README.rst", encoding='UTF-8').read(),
      url='http://github.com/tomhaoye/qrcode',
      license='MIT',
      packages=['qsqrcode'],
      install_requires=[
          'reedsolo',
          'Pillow'
      ],
      classifiers=[
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: MIT License",
          "Topic :: Multimedia :: Graphics",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6"
      ],
      entry_points={
          "console_scripts": [
              "qsqrcode = qsqrcode.commandline:main"
          ]
      },
      zip_safe=False)
