import json
import tkinter as tk
from typing import Union, Callable

from pykit.misc import ProxyWatcher, Proxy, ProxyClass


class WidgetManagerProxyWatcher(ProxyWatcher):
    widget_map = {}
    widget_instance_map = {}

    def __init__(self, proxy_master: "Proxy"):
        super().__init__(proxy_master)

        self.proxy_widget_map = WidgetManagerProxyWatcher.widget_map

    @staticmethod
    def get_widget(id_flag: str):
        return WidgetManagerProxyWatcher.widget_map.get(id_flag)

    @staticmethod
    def _set_widget(id_flag, widget):
        if id_flag:
            if isinstance(widget, Proxy):
                WidgetManagerProxyWatcher.widget_map[id_flag] = widget.container
            else:
                WidgetManagerProxyWatcher.widget_map[id_flag] = widget

    def _get_widget(self, widget_class, args, kwargs):
        return widget_class(self.container, *args, **kwargs)

    def proxy_deploy_widget(self, widget_config: dict):
        id_flag = widget_config.get('id')
        widget = widget_config.get('widget')  # type: Union[Callable, dict]
        deploy = widget_config.get('deploy')  # type: Union[Callable, dict]

        register_config = {}

        if callable(widget):
            widget_instance = widget(self.container)
        else:
            instance = widget.get('instance')  # type: Union[Callable, str]
            prop = widget.get('prop', {})

            if isinstance(instance, str):
                instance_config = WidgetManagerProxyWatcher.widget_instance_map.get(instance)
                instance = instance_config.get('instance')

                common_prop = instance_config.get('prop', {})
                common_prop.update(prop)
                prop = common_prop

                register_config = instance_config

            widget_instance = instance(self.proxy_master.container, **prop)

        after_instance = register_config.get('after_instance')
        if after_instance:
            after_instance(widget_instance)

        if callable(deploy):
            deploy(widget_instance)
        else:
            if isinstance(widget_instance, Proxy):
                descendants = deploy.get('descendants', [])
                widget_instance.descendants(descendants)

            pack = deploy.get('pack')
            if pack:
                if pack is True:
                    widget_instance.pack()
                else:
                    widget_instance.pack(**pack)

        self._set_widget(id_flag, widget_instance)

        return self.proxy_master

    def proxy_get_widget(self, id_flag: str):
        return self.get_widget(id_flag)

    def proxy_pack_factory(self, invoke):
        return lambda *args, **kwargs: self.proxy_pack(invoke, args, kwargs)

    def proxy_pack(self, invoke, args, kwargs):
        invoke(*args, **kwargs)
        return self.proxy_master

    def proxy_descendants(self, descendants):
        for widget_config in descendants:
            self.proxy_deploy_widget(widget_config)
        return self.proxy_master

    def proxy_registry(self, widget_name, widget_instance):
        self.registry(widget_name, widget_instance)

    @staticmethod
    def registry(widget_name, widget_instance):
        if not isinstance(widget_instance, dict):
            widget_instance = {"instance": widget_instance}
        WidgetManagerProxyWatcher.widget_instance_map[widget_name] = widget_instance

    @staticmethod
    def modify(widget_name, widget_instance):
        if not isinstance(widget_instance, dict):
            widget_instance = {"instance": widget_instance}
        WidgetManagerProxyWatcher.widget_instance_map[widget_name].update(widget_instance)


def create_proxy_widget(widget):
    return ProxyClass(
        widget,
        WidgetManagerProxyWatcher
    )


class Container:

    def __init__(self, master, after_instance=None):
        self.master = master
        self.proxyFrame = create_proxy_widget(tk.Frame)
        Container.registry('ProxyFrame', self.proxyFrame)

        if after_instance:
            Container.modify('ProxyFrame', {
                "after_instance": after_instance
            })

    def parse(self, descendants):
        return self.proxyFrame(self.master).descendants(descendants).pack(fill=tk.BOTH, expand=tk.TRUE)

    def parse_str(self, descendants):
        return self.parse(json.loads(descendants))

    def parse_file(self, descendants):
        with open(descendants, 'r') as fp:
            return self.parse(json.load(fp))

    @staticmethod
    def get(id_flag):
        return WidgetManagerProxyWatcher.get_widget(id_flag)

    @staticmethod
    def registry(widget_name, widget_instance):
        WidgetManagerProxyWatcher.registry(widget_name, widget_instance)

    @staticmethod
    def modify(widget_name, widget_instance):
        WidgetManagerProxyWatcher.modify(widget_name, widget_instance)
