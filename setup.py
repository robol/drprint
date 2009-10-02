from distutils.core import setup

setup (name='DrPrint',
       version='0.3',
       author='Leonardo Robol',
       author_email='leo@robol.it',
       url='http://www.robol.it/~leonardo/',
       license='GPL',
       packages = ['DrPrintGui'],
       py_modules=['DrPrintBackend'],
       data_files=[('bin', ['drprint']),
                   ('share/applications',['drprint.desktop']),
                   ('share/pixmaps', ['drprint.svg']) ],
       )
