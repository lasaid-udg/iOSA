import logging
import traceback
import pathlib

LOG_PATH = pathlib.Path("bin/log.log")
WINDOWS_CMD_LOG_PATH = pathlib.Path("log.log")
FORMAT = "%(asctime)s %(levelname)s %(message)s"
ENCODE = "utf-8"
FILEMODE = "a"


class Log():
    def __init__(self) -> None:
        """
        Logfile for tracebacks, exceptions and events

        Atributes
        ----------

        Methods
        -------
        insert_log_info(s)
            insert event to log file
        insert_log_error(s)
            insert error (with traceback) to log file

        """
    
    def insert_log_info(self, s: str) -> None:
        """
        Insert to log a succesful event

        Parameters
        ----------
        s : string
            string with the event info

        Returns
        -------
        None

        Raises
        ------
        OSError
            Can't open the log file
        """

        log = logging
        try:
            log.basicConfig(filename=LOG_PATH, filemode=FILEMODE, encoding=ENCODE,
                                format=FORMAT,
                                level=logging.INFO
                                )
        except FileNotFoundError:
            log.basicConfig(filename=WINDOWS_CMD_LOG_PATH, filemode=FILEMODE, encoding=ENCODE,
                                format=FORMAT,
                                level=logging.INFO
                                )
        log.info(s)

    def insert_log_error(self, var='') -> None:
        """
        Insert to log an error with the traceback tree

        Parameters
        ----------
        s : string
            string with the error info

        Returns
        -------
        None

        Raises
        ------
        OSError
            Can't open the log file
        """
        
        s = str(traceback.format_exc())
        log = logging

        try:
            log.basicConfig(filename=LOG_PATH, filemode=FILEMODE, encoding=ENCODE,
                            format=FORMAT,
                            level=logging.ERROR
                            )
        except FileNotFoundError:
            log.basicConfig(filename=WINDOWS_CMD_LOG_PATH, filemode=FILEMODE, encoding=ENCODE,
                            format=FORMAT,
                            level=logging.ERROR
                            )
        if var == '':
            log.error(s)
        else:
            # print("VAR:", var)
            log.error(s + '\n%s', var)
