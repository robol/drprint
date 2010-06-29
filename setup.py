from distutils.core import setup

setup (name='drprint',
       version='0.9.1',
       author='Leonardo Robol',
       author_email='leo@robol.it',
       url='http://www.robol.it/~leonardo/',
       license='GPL',
       packages = ['DrPrintGui'],
       py_modules=['DrPrintBackend'],
       data_files=[('bin', ['drprint']),
                   ('share/drprint',['drprint_gui.png']),
                   ('share/applications',['drprint.desktop']),
                   ('share/pixmaps', ['drprint.png']) ],
       )
