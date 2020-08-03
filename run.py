# import packaging.version
# import packaging.specifiers
import packaging.requirements
# import packaging.markers

from autoytdl.AYTDL import main

if __name__ == '__main__':
    main()


# this is a launcher but also a build tool for pyinstaller
# It is used as a memo and to help different contributors package the application in the same way
# On (arch) linux, I compile with:
# pyinstaller run.py --onedir --exclude scipy --exclude tk --exclude numpy --exclude PySide2 --exclude shiboken2 --exclude Pillow-PIL
