import time
from threading import Thread, Lock


def fiber(start: Optional[Callable] = None, end: Optional[Callable] = None):
    """

    `装饰器`，封装一个函数作为线程执行，允许传入开始和结束的回调函数

    :param start: 开始执行函数的回调
    :param end: 结束执行函数的回调
    :return: 函数封装器

    """

    def decorator(func):
        def wrap(*args):
            def task():
                if start:
                    start(*args)
                func(*args)
                if end:
                    end(*args)

            threading.Thread(target=task).start()

        return wrap

    return decorator


class StopTask(Exception):
    ...


class TaskThread(Thread):

    def __init__(self, name=None, target=None, args=(), kwargs=None):
        super().__init__(name=name, target=target, args=args, kwargs=kwargs, daemon=True)

        self._is_run_flag = False
        self._is_stop = False

    @property
    def is_stop(self):
        return self._is_stop

    @property
    def is_run_flag(self):
        return self._is_run_flag

    def run(self) -> None:
        self._is_run_flag = True
        self._is_stop = False
        try:
            while self._is_run_flag:
                if self._target:
                    self._target(*self._args, **self._kwargs)
        except StopTask:
            ...
        finally:
            del self._target, self._args, self._kwargs
        self._is_stop = True

    def stop(self, block=False):
        self._is_run_flag = False
        while not self._is_stop and block:
            time.sleep(0.1)
        return self._is_stop


class Task:

    def __init__(self, task_func):
        self._task_func = task_func
        self._task_thread = None
        self._mutex = Lock()

    def start(self, *args):
        """

        同一个任务无法重复创建

        :return:

        """
        with self._mutex:
            if self._task_thread is None:
                self._task_thread = TaskThread(target=self._task_func, args=args)
                self._task_thread.start()

    def restart(self, *args):
        self.destroy()
        self.start(*args)

    def stop_task(self):
        raise StopTask

    def destroy(self, block=False):
        with self._mutex:
            if self._task_thread:
                self._task_thread.stop(block)
                self._task_thread = None
