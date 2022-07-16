class Lock:
    """
    协程锁对象
    """

    def __init__(self, *, loop=None):
        # 创建一个_waiters等待队列，用于在锁被释放时恢复当前协程，实际上_waiters存储的是每一个被挂起的协程任务，
        # 似乎说协程任务不太准确，更准确一点应该是挂起的协程的一个断点位置对象
        self._waiters = collections.deque()

        # 标识符，用于标记锁的状态
        self._locked = False

        # 获取事件循环
        if loop is not None:
            self._loop = loop
        else:
            self._loop = events.get_event_loop()

    def locked(self):
        """

        查看当前锁是释放还是锁住的状态

        """
        return self._locked

    @coroutine
    def acquire(self):
        """

        获取锁

        """

        # 如果没有被某个协程锁定，或者所有被挂起来的协程都被取消了，那么立即返回，让协程得到锁并且设置标识符为True
        if not self._locked and all(w.cancelled() for w in self._waiters):
            self._locked = True
            return True

        # 如果锁已经被获取了，就是说标识符是False或者有被挂起来的协程任务，那么为当前需要执行的协程创建一个Future对象，
        # 实际上在这里就打上断点了，把它添加到挂起的队列里面
        fut = self._loop.create_future()
        self._waiters.append(fut)
        try:
            # 弹出当前协程，主事件循环就会去执行其它协程
            yield from fut
            self._locked = True
            return True
        except futures.CancelledError:
            if not self._locked:
                self._wake_up_first()
            raise
        finally:
            self._waiters.remove(fut)

    def release(self):
        """

        释放锁

        """

        # 设置下标识符号，调用_wake_up_first方法唤醒第一个被挂起来的协程对象
        if self._locked:
            self._locked = False
            self._wake_up_first()
        else:
            raise RuntimeError('Lock is not acquired.')

    def _wake_up_first(self):
        """

        唤醒第一个被挂起来的协程对象

        """
        for fut in self._waiters:
            if not fut.done():
                # 随便设置个结果，有结果这个协程的断点就能接着走了
                fut.set_result(True)
                break
