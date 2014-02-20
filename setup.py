from distutils.core import setup

setup (name='drprint',
       version='2.1',
       author='Leonardo Robol',
       author_email='leo@robol.it',
       url='http://www.robol.it/~leonardo/',
       license='GPL3',
       packages = ['DrPrintGui'],
       py_modules=['DrPrintBackend'],
       data_files=[('bin', ['drprint']),
                   ('share/drprint',['drprint_gui.png']),
                   ('share/applications',['drprint.desktop']),
                   ('share/pixmaps', ['drprint.png']), 
                   ('share/man/man1', ['drprint.1'])],
       )
