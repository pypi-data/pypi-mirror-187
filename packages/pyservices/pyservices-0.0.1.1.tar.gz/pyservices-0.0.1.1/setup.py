from setuptools import setup


with open('./README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='pyservices',
    version='0.0.1.1',
    author='Aidar Turkenov',
    author_email='a.k.turken0v@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aturkenov/pyservices',
    project_urls={
        'Bug Tracker': 'https://github.com/aturkenov/pyservices/issues',
        'Discussions': 'https://github.com/aturkenov/pyservices/discussions',
    },
    classifiers=[
        'Typing :: Typed',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['pyservices'],
    install_requires=[
        'orjson',
        'pydantic',
    ],
    python_requires='>=3.6',
)

