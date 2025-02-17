import atexit
import ctypes
import signal
import sys
import time
from Artificial import Artificial_AI
from rich import print


def main():
    ai = Artificial_AI()
    atexit.register(ai.cleanUp)

    try:
        signal.signal(signal.SIGINT, ai.handel_intrupt)
        signal.signal(signal.SIGTERM, ai.handel_intrupt)
    except KeyboardInterrupt as e:
        print(e)
    pass
    ai.welcome()
    try:
        ai.set_system_txt("you are chat bot which is very straight to the point")
    except Exception as e:
        print(e)
    ai.handle_running()


def check_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("checking up priority :- ")
        time.sleep(3)
        ctypes.windll.shell32.ShellExecuteW(
            None,  # Parent window handle
            "runas",  # Verb (e.g., "runas" for admin)
            sys.executable,  # Python executable
            " ".join(sys.argv),  # Script arguments
            None,  # Working directory
            1  # Show window
        )
        sys.exit()
        pass
    pass


if __name__ == '__main__':
    # check_admin()
    main()