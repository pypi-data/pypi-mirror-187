from distutils.core import setup
setup(
  name = '102003105',         # How you named your package folder (MyLib)
  packages = ['102003105'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python package to find TOPSIS for Multi-Criteria Decision Analysis Method',   # Give a short description about your library
  author = 'Aditya Kuthiala',                   # Type in your name
  author_email = 'adityakuthiala1806@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/AdiK1806/Topsis-Aditya-102003105',   # Provide either the link to your github or to your website
    keywords=['topsis', 'TIET' ,'Thapar'],
    include_package_data=True,
    install_requires=['pandas', 'tabulate'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)