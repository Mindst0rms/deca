from deca.gui.main import main
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    vfs = main()
