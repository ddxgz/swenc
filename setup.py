from setuptools import setup

import swenc


setup(name='swenc',
      #version=swift3.version,
      description='Swift object encryption Middleware',
      author='pc',
      #author_email='openstack@lists.launchpad.net',
      url='https://github.com/ddxgz/swenc',
      packages=['swenc'],
      requires=['swift(>=1.13)', 'python_dateutil(>=2.1)'],
      entry_points={'paste.filter_factory':
                        ['swenc=swenc.encryption:filter_factory',
                         ]
                  }
      )