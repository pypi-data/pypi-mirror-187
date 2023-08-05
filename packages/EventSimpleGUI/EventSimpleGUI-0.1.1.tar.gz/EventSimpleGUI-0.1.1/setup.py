from setuptools import setup

with open('README.MD', 'r') as arq:
    readme = arq.read()
keywords = ['EventSimpleGUI']

setup(name='EventSimpleGUI',
      version='0.1.1',
      license='MIT license',
      author='Daniel Coêlho',
      long_description=readme,
      long_description_content_type='text/markdown',
      author_email='heromon.9010@gmail.com',
      keywords='',
      description='A tool for create events to PySimpleGUI',
      packages=['pysimpleevent'],
      install_requires=['pysimplegui'])