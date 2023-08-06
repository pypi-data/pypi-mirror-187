from distutils.core import setup

setup(name='argp',
      version='1.0.0',
      description='Desciption for argp here',
      author='Ville M. Vainio',
      author_email='ville.vainio@basware.com',
      url='',
      packages=['argp'],
      install_requires=[],
      entry_points = {
        'console_scripts': [
            'argp = argp.argp:main'
        ]
      }
     )
