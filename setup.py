from setuptools import setup, find_packages


setup(name='moviequizz',
      version='1',
      description='A slack bot to test your film knowledge.',
      url='https://github.com/BryanMums/MovieQuizz',
      author='Infinit8',
      author_email='contact@infinit8.io',
      license='MIT',
      packages=find_packages(),
      install_requires=('aiohttp'),
      extra_requires={
          'doc': ('Sphinx', 'sphinx_rtd_theme'),
      },
      zip_safe=False)