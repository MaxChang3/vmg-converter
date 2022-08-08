from typing import List
from xml.etree import ElementTree as ET
from vmg import VMG


def vmg2xml(vmg_list: List, filepath: str) -> None:
    ele = ET.Element("smses", {"count": str(len(vmg_list))})
    status = {
        "DELIVER": "1",
        "SUBMIT": "2",
    }
    for vmg in vmg_list:
        son = ele.makeelement("sms", {
            "protocol": "0",
            "address": vmg['VCARD']['TEL'],
            "date": vmg['VENV']['VBODY']['Date'],
            "type": status[vmg['X-MESSAGE-TYPE']],
            "body": vmg['VENV']['VBODY']['text']
        })
        ele.append(son)
    tree = ET.ElementTree(ele)
    tree.write(filepath, encoding='utf-8', xml_declaration=True, short_empty_elements=False)


if __name__ == "__main__":
    CUSTOM_VBODY_PARAMS = [
        "Date ",
    ]
    vmg = VMG(CUSTOM_VBODY_PARAMS)
    vmg_list = vmg.load('./sms.vmg')
    vmg2xml(vmg_list)