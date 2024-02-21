class Logger():

    def __init__(self, target_file: str, print_console: bool, write_log: bool):
        self.content = []
        self.msg =       "LOG:       "
        self.war =   "WARNING:   "
        self.err =     "ERROR:     "
        self.deb =     "DEBUG:     "
        self.print_console = print_console
        self.write_log = write_log
        self.target_file = target_file
        try:
            self.file = open(self.target_file, "w", encoding='UTF-8')
        except:
            self.warning("Couldnt open/create log file")

    def debug(self, message: str) -> None:
        if self.print_console:
            print(self.msg + message)
        self.content.append(self.msg + message)

    def log(self, message: str) -> None:
        if self.print_console:
            print(self.msg + message)
        self.content.append(self.msg + message)

    def warning(self, message: str) -> None:
        if self.print_console:
            print(self.war + message)
        self.content.append(self.war + message)

    def error(self, message: str) -> None:
        if self.print_console:
            print(self.err + message)
        self.content.append(self.err + message)

    def exc(self, message: str, exc_text: str) -> None:
        if self.print_console:
            print(self.err + message)
        self.content.append(self.err + message)
        raise exc_text
    def __del__(self):
        self.file.writelines(self.content)
        self.file.close()

TARGET_FILE = "log.txt"
logger = Logger(TARGET_FILE, True, True)
