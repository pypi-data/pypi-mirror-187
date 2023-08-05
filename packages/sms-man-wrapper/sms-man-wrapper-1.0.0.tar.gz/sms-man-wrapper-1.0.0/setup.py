from setuptools import setup

setup(
    name='sms-man-wrapper',
    version='1.0.0',
    description='A Python wrapper for the SMS-Man API',
    author='Laurent Baaziz',
    author_email='laurent.baaziz@gmail.com',
    url='https://github.com/BaLaurent/sms-man-wrapper',
    py_modules=['sms-man-wrapper'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
	readme = "README.md"
)
