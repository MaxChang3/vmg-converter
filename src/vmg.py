from functools import reduce
from operator import getitem
from typing import List


class VMG:
    __params = [
        "Date:"
    ]
    def __init__(self, custom_params: List[str] = None):
        self.params = self.__params + custom_params

    def load(self, filepath: str):
        vmg_list = []
        with open(filepath, "r") as f:
            text_vmg = filter(lambda x: x.strip() != '', f.read().split('END:VMSG'))
            vmg_list = [*map(self.__parse, text_vmg)]
        return vmg_list

    def __parse(self, vmg: str):
        getTop = lambda keys, dic: reduce(getitem, keys, dic)
        res = {}
        relations = []
        for line in vmg.strip().split("\n"):
            top: dict = getTop(relations, res)
            piece = line.split(":")
            if line.startswith("BEGIN:"):
                begin_name = piece[1]
                relations.append(begin_name)
                top[begin_name] = {}
                continue
            if line.startswith("END:"):
                relations.pop()
                continue
            if relations[-1] == "VBODY":
                for param in self.params:
                    if (line.startswith(param)):
                        piece = [param[:-1], line[len(param):].strip()]
                        break
                else:
                    lastline = top.get('text', None)
                    top['text'] = (lastline + "\n" if lastline is not None else '') + line
                    continue
            name, item = piece
            top[name] = item.strip()
        return res['VMSG']
