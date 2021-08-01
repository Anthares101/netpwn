from setuptools import setup, find_packages

setup(
    name='netpwn',
    version='1.0.post4',
    license='GPL-2.0',
    author="Ángel Heredia",
    packages=find_packages(exclude=("*tests*",)),
    url='https://github.com/anthares101/netpwn',
    keywords='windows macos linux shell reverse-shell tool hacking netcat tty pty cybersecurity reverse pwntools hacktoberfest kali',
    install_requires=[
          'pwntools',
      ],
    entry_points='''
        [console_scripts]
        netpwn=netpwn.netpwn:main
    ''',
)
