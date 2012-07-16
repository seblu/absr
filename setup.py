from setuptools import setup
import os

ldesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='abs',
    version=0,
    description='Archlinux Build System',
    long_description=ldesc,
    author='Sébastien Luttringer',
    license='GPL2',
    packages=['abs'],
    scripts=['bin/abs', 'bin/ats', 'bin/auc', 'bin/aurdown'],
    data_files=(
	  ('/usr/share/abs/', ('README.rst', 'LICENSE', 'CHANGELOG', 'COPYRIGHT')),
      ('/usr/share/abs/samples/', ('samples/auc.conf',))
    ),
    classifiers=[
        'Operating System :: Unix',
        'Programming Language :: Python',
        ],
    )
