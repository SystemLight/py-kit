from tornado.template import Template, Loader

import os
import re
from typing import List, Optional, Callable, TypeVar

T = TypeVar("T")
ParseCallable = Callable[["TreeOperate", List[T], int], T]


def require(path):
    """

    有时你可能只是需要从文件中读取到json数据，这是require函数将根据
    获取到的path，返回dict对象，相当方便，该函数同样类似于json.load

    :param path:
    :return: dict

    """
    import json
    fp = open(path, "r")
    data = fp.read()
    fp.close()
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return {}


class GenerateCodeEngine:
    """

    生成代码引擎类

    使用方法::

        gec = GenerateCodeEngine()
        gec.catch_write("index.html", "template.html", {
            "anthor": "systemlight"
        })

    """

    def __init__(self, template_root_path=""):
        """

        构造函数

        :param template_root_path: 模板根目录

        """
        self.glob_content = {}
        self.template_root_path = template_root_path

        self.__start_match_tag = r"//start_user_code"
        self.__end_match_tag = r"//end_user_code"
        self.catch_match = r"{}(.*?){}".format(self.__start_match_tag, self.__end_match_tag)

    @property
    def start_match_tag(self):
        return self.__start_match_tag

    @start_match_tag.setter
    def start_match_tag(self, value):
        self.__start_match_tag = value
        self.catch_match = r"{}(.*?){}".format(self.__start_match_tag, self.__end_match_tag)

    @property
    def end_match_tag(self):
        return self.__end_match_tag

    @end_match_tag.setter
    def end_match_tag(self, value):
        self.__end_match_tag = value
        self.catch_match = r"{}(.*?){}".format(self.__start_match_tag, self.__end_match_tag)

    def register_glob_content(self, name, value):
        """

        注册全局方法或者变量，每个模板渲染时都将附带该内容

        :param name: 名称
        :param value: 内容
        :return: None

        """
        self.glob_content[name] = value

    def render(self, template_path, kwargs=None):
        """

        根据模板渲染并生成字符串返回

        :param template_path: 模板文件路径
        :param kwargs: 包含写入模板中的变量数据和函数等
        :return: 渲染后的内容

        """
        template_path = os.path.join(self.template_root_path, template_path)
        if kwargs is None:
            kwargs = {}
        with open(template_path, "r", encoding="utf-8") as fp:
            temp = Template(fp.read(), autoescape=None, loader=Loader(self.template_root_path))
        glob_content = {**self.glob_content, **kwargs}
        return temp.generate(**glob_content)

    def write(self, path, template_path, kwargs=None):
        """

        将渲染内容希尔到文件当中

        :param path: 目标文件路径
        :param template_path: 模板文件路径
        :param kwargs: 包含写入模板中的变量数据和函数等
        :return: None

        """
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(self.render(template_path, kwargs).decode())

    def catch_write(self, path, template_path, kwargs=None):
        """

        捕获用户代码写入方法，执行写入之前会先匹配用户代码

        :param path: 目标文件路径
        :param template_path: 模板文件路径
        :param kwargs: 其它额外参数，参考catch_user_code方法，包含写入模板中的变量数据和函数等
        :return: None

        """
        if kwargs is None:
            kwargs = {}
        user_code = self.catch_user_code(
            path=path,
            match=kwargs.get("match", None),
            code_count=kwargs.get("code_count", 1),
        )
        kwargs["user_code"] = user_code
        self.write(path, template_path, kwargs)

    def catch_user_code(self, path, match=None, code_count=1):
        """

        捕获目标路径文件中的用户代码

        :param path: 目标文件路径
        :param match: 匹配用户代码规则
        :param code_count: 用户代码数量
        :return: 匹配结果列表

        """
        if match is None:
            match = self.catch_match
        if not os.path.exists(path):
            return [""] * code_count
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()
        result = re.findall(match, content, re.S)
        result = list(map(lambda v: v.strip("\n "), result))
        size = len(result)
        if size < code_count:
            return result + [""] * (code_count - size)
        return result


class TreeOperate:
    """

    TreeOperate允许你操作一颗树型结构数据，支持数据导入和导出，数据必须含有key唯一标识，
    子元素必须存储在children键值下
    示例内容::
        _data = {
            "key": "1",
            "title": "root",
            "children": [
                {"key": "2", "title": "2", "children": [
                    {"key": "4", "title": "4"},
                    {"key": "5", "title": "5"}
                ]},
                {"key": "3", "title": "3", "children": [
                    {"key": "6", "title": "6"},
                    {"key": "7", "title": "7"}
                ]}
            ]
        }
        tree_root = TreeOperate.from_dict(_data)
        tree_root.find("2").append(TreeOperate.from_dict({"key": "8", "title": "8"}))
        print(tree_root.find("8"))
        tree_root.find("8").remove()
        print(tree_root.find("8"))

    """

    def __init__(self, key=None):
        self.key = key
        self.pid = None
        self.data = {}
        self.parent = None  # type: Optional[TreeOperate]
        self.__children = []  # type: List[TreeOperate]

    def __str__(self):
        return str({
            "key": self.key,
            "pid": self.pid,
            "data": self.data,
            "children": self.__children
        })

    @staticmethod
    def from_dict(data):
        """

        从dict对象中返回TreeOperate对象
        :param data: dict
        :return: TreeOperate

        """
        tree = TreeOperate(data.get("key", None))
        for d in data:
            if d not in ["key", "children"]:
                tree.data[d] = data[d]
        for i in data.get("children", []):
            tree.append(TreeOperate.from_dict(i))
        return tree

    @staticmethod
    def from_file(path):
        """

        从json文件中读取数据

        :param path: json文件路径
        :return: TreeOperate

        """
        return TreeOperate.from_dict(require(path))

    @property
    def children(self):
        return self.__children

    def append(self, sub_tree: "TreeOperate"):
        """

        为当前节点添加子节点，节点类型必须是TreeOperate类型
        :param sub_tree: 子类型节点
        :return: None

        """
        if not isinstance(sub_tree, TreeOperate):
            raise TypeError("sub_tree must be of type TreeOperate")
        sub_tree.pid = self.key
        sub_tree.parent = self
        self.__children.append(sub_tree)

    def find(self, key: str):
        """

        根据key值查找节点
        :param key: key值
        :return: TreeOperate

        """
        if self.key == key:
            return self
        else:
            for i in self.__children:
                result = i.find(key)
                if result:
                    return result
        return None

    def remove(self, key=None):
        """

        删除节点，如果传递key值，将删除当前节点下匹配的子孙节点，
        如果不传递key值将当前节点从父节点中删除
        :param key: [可选] key值
        :return:

        """
        if key is None:
            if self.parent is not None:
                self.parent.__children.remove(self)
        else:
            remove_child = self.find(key)
            if remove_child:
                remove_child.parent.__children.remove(remove_child)

    def parse(self, callback: ParseCallable, deep=0):
        """

        遍历定制解析规则，返回解析内容

        :param callback: Callable[["TreeOperate", List[T], int], T] 解析回调函数返回解析结果
        :param deep: 当前解析深度，默认不需要填写，用于回调函数接收判断所在层级
        :return: 解析结果

        """
        child_parse_list = []
        for i in self.__children:
            child_parse_list.append(i.parse(callback, deep + 1))
        return callback(self, child_parse_list, deep)

    def to_dict(self, flat=False):
        """

        输出dict类型数据，用于json化
        :param flat: 是否将data参数内容直接映射到对象
        :return: dict

        """
        result = dict(key=self.key, pid=self.pid)
        if flat:
            for j in self.data:
                result[j] = self.data[j]
        else:
            result["data"] = self.data
        children = []
        for i in self.__children:
            children.append(i.to_dict(flat))
        result["children"] = children
        return result


def domain_parse_jsx(_tree_obj: TreeOperate):
    """

    保存额外解析数据，解析函数会被所有树叶节点对象调用，如果需要保存一些遍历叶子节点时的数据内容，
    可以定义一个函数，并增加一个变量用于接受。

    :param _tree_obj:
    :return:

    """
    data_pool = set()

    def parse_jsx(self: "TreeOperate", child: List[str], deep=0) -> str:
        p_str = ""
        props = self.data["props"]
        data_pool.add(self.data["title"])
        for p in props:
            if isinstance(props[p], str):
                p_str += " {}={{\"{}\"}}".format(p, props[p])
            elif isinstance(props[p], bool):
                p_str += " {}={{{}}}".format(p, str(props[p]).lower())
            elif isinstance(props[p], int):
                p_str += " {}={{{}}}".format(p, props[p])
            else:
                p_str += " {}={{\"{}\"}}".format(p, props[p])
        return "\n{0}<{1}{3}>{2}\n{0}</{1}>".format("\t" * deep, self.data["title"], "".join(child), p_str)

    result = tree_obj.parse(parse_jsx)
    return result, data_pool


if __name__ == '__main__':
    tree_obj = TreeOperate.from_file("data.json")
    dom, import_pool = domain_parse_jsx(tree_obj)
    print(dom)
