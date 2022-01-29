from typing import Callable, Union, Any, Sequence, Optional, List, Tuple


class UpdateListIgnoreKey:
    ...


class UpdateList(list):
    """

    `UpdateList的子元素必须是字典DICT`

    主要方法update_or_append()，该方法是对list类型拓展，
    当update的数据对象存在时对其更新，注意请保证UpdateList
    的子项是dict类型而不要使用值类型，值类型对于UpdateList毫无意义

    on_update hook函数，接收old_val(旧数据), p_object(新数据)，需要返回更新数据
    on_append hook函数，接收p_object(添加数据)，需要返回添加数据
    on_fetch_key hook函数，当key属性定义为函数时需要同时定义如何捕获key值

    key 支持字符串，字符串指定子元素中的更新参考值
        支持函数，接收val(当前数据)，key(参考key值)该key值由on_fetch_key返回，函数返回bool值True为更新，False为添加

    on_fetch_key作用::
        定义on_fetch_key来告知update如何捕获我们想要的类型的key值，
        on_fetch_key只有当key属性定义为函数时才有意义，并且保证传入相同item时返回内容要一致。

    """

    def __init__(
        self,
        key: Union[str, Tuple[Callable[[dict, Any], bool], Callable[[dict], Any]]],
        seq: Sequence[dict] = ()
    ):
        super().__init__(seq)

        if isinstance(key, str):
            self.key = key  # 对象key值，可以是函数，函数接收val, key返回布尔值代表满足条件
            self.on_fetch_key = None  # 当key设置为函数时必须定义的回调，传入item对象返回该对象key值内容
        elif isinstance(key, tuple):
            self.key, self.on_fetch_key = key
        else:
            raise ValueError('Unsupported key type')

        self.on_update: Optional[Callable[[dict, dict], dict]] = None  # 当元素是更新时调用的更新方法，如果元素是插入时不调用，如果不定义该回调默认直接替换
        self.on_append: Optional[Callable[[dict], dict]] = None  # 当元素update方法触发的是添加时调用的回调函数，可以自定义append类型

        self._index_map = None
        self._reset_index_map()

    def __getitem__(self, iid):
        if isinstance(self.key, str) or callable(self.key):
            return super().__getitem__(self._index_map[iid])
        return super().__getitem__(iid)

    def __setitem__(self, key, value):
        raise NotImplementedError('Please use append or update_or_append settings')

    def append(self, __object) -> None:
        super().append(__object)
        self._set_index_map(__object, len(self) - 1)

    def update_or_append(self, current_item: dict):
        """

        类似于append方法，不同的是当内容存在时会对内容进行更新，更新逻辑遵从update_callback
        而当内容不存在时与append方法一致进行末尾加入内容

        :param current_item: 内容对象
        :return: None

        """
        if not self.on_update:
            self.on_update = lambda o, p: p
        if not self.on_append:
            self.on_append = lambda p: p

        old_index = -1
        old_item = None

        if isinstance(self.key, str):
            current_value = current_item.get(self.key, UpdateListIgnoreKey)
            if not isinstance(current_value, UpdateListIgnoreKey):
                cache_index = self._index_map.get(current_value, -1)
                if cache_index > -1:
                    old_index, old_item = cache_index, super().__getitem__(cache_index)
        elif callable(self.key):
            try:
                fetch_key = self.on_fetch_key(current_item)
                cache_index = self._index_map.get(fetch_key, -1)
                if cache_index > -1:
                    old_index, old_item = cache_index, super().__getitem__(cache_index)
            except TypeError:
                raise TypeError('Function `on_fetch_key` is not defined')
        else:
            raise TypeError('`key` is TypeError')

        if old_index == -1:
            self.append(self.on_append(current_item))
        else:
            # 更新数据不用设置索引
            super().__setitem__(old_index, self.on_update(old_item, current_item))

    def bulk_update_or_append(self, data: List[dict]):
        for i in data:
            self.update_or_append(i)

    def remove(self, __object) -> None:
        super().remove(__object)
        self._reset_index_map()

    def extend(self, __iterable) -> None:
        super().extend(__iterable)
        self._reset_index_map()

    def insert(self, __index, __object) -> None:
        super().insert(__index, __object)
        self._reset_index_map()

    def reverse(self) -> None:
        super().reverse()
        self._reset_index_map()

    def pop(self, __index=...):
        super().pop(__index)
        self._reset_index_map()

    def find(self, callback: Callable[[Any], bool]):
        """

        返回满足回调函数的内容

        :param callback: 回调函数，返回布尔类型用于判断是否满足要求
        :return: (索引，值)

        """
        for index, item in enumerate(self):
            if callback(item):
                return index, item
        return -1, None

    def _reset_index_map(self):
        self._index_map = {}
        if isinstance(self.key, str):
            for index, item in enumerate(self):
                self._index_map[item[self.key]] = index
        elif callable(self.key):
            try:
                for index, item in enumerate(self):
                    self._index_map[self.on_fetch_key(item)] = index
            except TypeError:
                raise TypeError('Function `on_fetch_key` is not defined')
        else:
            raise TypeError('`key` is TypeError')

    def _set_index_map(self, __item, __index):
        if isinstance(self.key, str):
            self._index_map[__item[self.key]] = __index
        elif callable(self.key):
            self._index_map[self.on_fetch_key(__item)] = __index


if __name__ == '__main__':
    def _key(_item, fetch_key):
        return _item['id'] + _item['fkey'] == fetch_key


    def _on_fetch_key(_item):
        return _item['id'] + _item['fkey']


    # 定义复杂场景
    ulist = UpdateList((_key, _on_fetch_key))
    ulist.append({'id': 3, 'fkey': 3, 'value': 6})
    ulist.append({'id': 4, 'fkey': 6, 'value': 6})
    ulist.append({'id': 5, 'fkey': 7, 'value': 6})

    item = {'id': 6, 'fkey': 4, 'value': 20}
    ulist.update_or_append(item)

    print(ulist[10])
    print(ulist._index_map)
