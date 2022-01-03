from setuptools import setup, find_packages

setup(
    name='netpwn',
    version='1.4',
    license='GPL-2.0',
    description='A netcat listener alternative with automatic shell stabilization.',
    author='Ángel Heredia',
    packages=find_packages(),
    url='https://github.com/anthares101/netpwn',
    keywords='windows macos linux shell reverse-shell tool hacking netcat tty pty cybersecurity reverse pwntools hacktoberfest kali',
    python_requires='>=3',
    install_requires=[
        'pwntools',
    ],
    entry_points='''
        [console_scripts]
        netpwn=netpwn.__main__:main
    ''',
)
