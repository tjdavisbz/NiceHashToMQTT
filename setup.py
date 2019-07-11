from setuptools import setup
setup(name='NiceHashToMQTT',
      version='0.01',
      description='Publishes Nicehash data to an MQTT brokder.',
      url='https://github.com/tjdavisbz/NiceHashToMQTT',
      author='TJ Davis',
      author_email='tjdavisbz@gmail.com',
      license='MIT',
      packages=['NiceHashToMQTT'],
      install_requires=['forex-python==1.5',
                        'paho-mqtt==1.4.0'])
