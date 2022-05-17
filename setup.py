from setuptools import setup, find_packages

setup(name='ekphrasis',
      version='0.5.4',
      description='Text processing tool, geared towards text from '
                  'social networks, such as Twitter or Facebook. '
                  'Ekphrasis performs tokenization, word normalization, '
                  'word segmentation (for splitting hashtags) '
                  'and spell correction.',
      url='https://github.com/cbaziotis/ekphrasis',
      author='Christos Baziotis',
      author_email='christos.baziotis@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests*', 'analysis']),
      install_requires=[
          'termcolor',
          'tqdm',
          'colorama',
          'ujson',
          'matplotlib',
          'nltk',
          'ftfy',
          'numpy'
      ],
      include_package_data=True
      )
