import logging
import logging.handlers


def build_log(log_path: str):
    """

    初始化日志系统基础配置

    :return:

    """
    logging.basicConfig(
        style='%',
        format='[%(levelname)s %(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO,
        handlers=[
            logging.handlers.RotatingFileHandler(log_path, maxBytes=1024 * 1024 * 30),
            logging.StreamHandler()
        ]
    )
