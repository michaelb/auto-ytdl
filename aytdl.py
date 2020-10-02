# import packaging.version
# import packaging.specifiers
# import packaging.markers
import os


# the packaging module is only useful to build the app
try:
    import packaging.requirements
except Exception:
    print("Fetching auto-ytdl pip dependencies. (install as --user)")
    os.system("python -m pip install --user packaging")


from autoytdl.AYTDL import main

if __name__ == '__main__':
    main()


# this is a launcher but also a build tool for pyinstaller
# It is used as a memo and to help different contributors package the application in the same way
# On (arch) linux, I compile with:
# pyinstaller aytdl.py --onedir --exclude scipy --exclude tk --exclude numpy --exclude PySide2 --exclude shiboken2 --exclude Pillow-PIL
