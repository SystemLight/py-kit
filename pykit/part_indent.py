import os
import pprint
import re


def create_node(item: str):
    value = item.strip()
    return {
        'parent': None,
        'name': value[0:value.index('(')],
        'value': item,
        'space_count': re.match('^\s*', item).end(0),
        'children': []
    }


def find_all_top_call(tree, result=None):
    if result is None:
        result = []
    for item in tree:
        if len(item['children']) > 0:
            find_all_top_call(item['children'], result)
        else:
            result.append(item)
    return result


def delete_parent(node):
    del node['parent']
    if len(node['children']) > 0:
        for child_node in node['children']:
            delete_parent(child_node)


def parse_to_array_tree(content: str):
    result = []
    last_node = None

    for item in content.split('\n'):
        if not item:
            continue

        current_node = create_node(item)

        if last_node is None:
            last_node = current_node
        else:
            if current_node['space_count'] > last_node['space_count']:
                current_node['parent'] = last_node
            elif current_node['space_count'] == last_node['space_count']:
                current_node['parent'] = last_node['parent']
            else:
                is_root = False
                search_match_node = last_node
                while current_node['space_count'] <= search_match_node['space_count']:
                    search_match_node = search_match_node['parent']
                    if search_match_node is None:
                        is_root = True
                        break
                if not is_root:
                    current_node['parent'] = search_match_node

            last_node = current_node

        if current_node['parent'] is None:
            result.append(current_node)
        else:
            current_node['parent']['children'].append(current_node)

    # for node in result:
    #     delete_parent(node)

    return result


def gen_call_graph():
    call_graph = []
    with open('call_tree.txt', 'r', encoding='utf-8') as fp:
        top_list = find_all_top_call(parse_to_array_tree(fp.read()))
        index = 0
        for node in top_list:
            index += 1
            graph = []
            current_node = node
            while current_node['parent'] is not None:
                graph.append(f'{current_node["name"]}--->{current_node["parent"]["name"]}')
                current_node = current_node["parent"]
            call_graph.append(f'subgraph 子图-{index} \n direction TB\n' + ('\n'.join(graph)) + '\nend')

    with open('call_graph.mmd', 'w', encoding='utf-8') as fp:
        fp.write('flowchart TB\n' + '\n\n\n'.join(call_graph))

    os.system("mmdc -i call_graph.mmd -o call_graph.svg")


def parse_to_array_tree2(content):
    # 用于存储每行对应的节点
    node_stack = []
    result = []

    for line in content.split('\n'):
        # 去除行首和行尾的空白字符
        if not line:
            continue

        # 统计缩进空格数量
        indent = len(line) - len(line.lstrip())
        # 获取节点名称
        name = line[:line.index('(')] if '(' in line else line

        # 创建当前节点
        current_node = {
            'name': name,
            'value': line,
            'space_count': indent,
            'children': []
        }

        # 找到合适的父节点
        while node_stack and node_stack[-1]['space_count'] >= indent:
            node_stack.pop()

        if node_stack:
            node_stack[-1]['children'].append(current_node)
        else:
            result.append(current_node)

        # 将当前节点添加到栈中
        node_stack.append(current_node)

    return result
