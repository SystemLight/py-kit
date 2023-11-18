import logging


def create_log(log_name):
    class MyLog:

        def __init__(self):
            self.logger = logging.getLogger(log_name)
            self.logger.setLevel(logging.DEBUG)
            self.logger.handlers.clear()

            file = logging.FileHandler(f'{log_name}.log', encoding='utf-8')
            file.setFormatter(
                logging.Formatter("%(threadName)s - %(asctime)s - %(levelname)s - %(message)s")
            )
            file.setLevel(logging.DEBUG)
            self.logger.addHandler(file)

            control = logging.StreamHandler()
            control.setFormatter(
                logging.Formatter("%(threadName)s - %(asctime)s - %(levelname)s - %(message)s")
            )
            control.setLevel(logging.INFO)
            self.logger.addHandler(control)

        @staticmethod
        def _init_msg(tag, messages):
            return '[' + tag + '] ' + ' ## '.join(['%s'] * len(messages))

        def d(self, tag, *messages):
            self.logger.debug(MyLog._init_msg(tag, messages), *messages)

        def i(self, tag, *messages):
            self.logger.info(MyLog._init_msg(tag, messages), *messages)

        def w(self, tag, *messages):
            self.logger.warning(MyLog._init_msg(tag, messages), *messages)

        def e(self, tag, *messages):
            self.logger.error(MyLog._init_msg(tag, messages), *messages)

        def c(self, tag, *messages):
            self.logger.critical(MyLog._init_msg(tag, messages), *messages)

    return MyLog
