from setuptools import setup, find_packages


with open('README.rst') as file:
    long_description = file.read()

setup(name='PyTuning',
      version='0.7.1',
      description='A Python package for the exploration of musical tunings.',
      author='Mark Conway Wirt',
      author_email='markcwirt@gmail.com',
      license='MIT',
      url='https://github.com/MarkCWirt/PyTuning',
      packages=find_packages(where="src"),
      scripts=['src/pytuning/interactive.py'],
      install_requires = ['sympy', 'numpy'],
      package_dir = {'': 'src'},
      package_data={
          '' : ['README.rst', 'License.txt', 'docs/*'],
          },
      include_package_data = True,
      platforms='Platform Independent',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Topic :: Multimedia :: Sound/Audio',
            'Topic :: Multimedia :: Sound/Audio :: Analysis',
            'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      keywords = 'Music Scales Tuning Microtonalities',
      long_description=long_description
     )
