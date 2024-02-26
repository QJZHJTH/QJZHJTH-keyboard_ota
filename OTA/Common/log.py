# -*-coding:utf-8 -*-
import logging
import time

from OTA.Common.utils import get_phone_time


class Logger:

    def __init__(self, logger, FilePath, device, CmdLevel=logging.INFO, FileLevel=logging.INFO):
        self.logger = logging.getLogger(logger)
        # 设置日志输出的默认级别
        self.logger.setLevel(logging.DEBUG)

        time_value = str(get_phone_time(device=device) + '- %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        # 日志输出格式
        # fmt = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        fmt = logging.Formatter(time_value)
        currentTime = time.strftime("%Y-%m-%d")
        self.logFileName = FilePath + '\\' + currentTime + ".log"

        # 文件输出到磁盘中
        fh = logging.FileHandler(self.logFileName)
        fh.setFormatter(fmt)
        fh.setLevel(FileLevel)

        self.logger.addHandler(fh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    logger = Logger("fox", CmdLevel=logging.DEBUG, FileLevel=logging.DEBUG)
    logger.logger.debug("debug")
    logger.logger.log(logging.ERROR, '%(module)s %(info)s', {'module': 'log日志', 'info': 'error'})
