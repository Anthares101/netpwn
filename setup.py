from setuptools import setup, find_packages

setup(
    name='netpwn',
    version='1.0',
    license='GPL-2.0',
    author="Ángel Heredia",
    packages=find_packages(exclude=("tests",)),
    package_dir={'': 'netpwn'},
    url='https://github.com/anthares101/netpwn',
    keywords='windows macos linux shel lreverse-shell tool hacking netcat tty pty cybersecurity reverse pwntools hacktoberfest kali',
    install_requires=[
          'pwntools',
      ],
)