import xml.etree.ElementTree as ET


def merge_struct(first, second):
    fd = dict(first)
    sd = dict(second)
    if fd["teg"] != sd["teg"]:
        return (-1, {"err": "wrong args",})
    change=0
    fd["atrib"].update(sd["atrib"])
    if fd["Childs"] == {}:
        fd["Childs"] = sd["Childs"]
        change += len(sd["Childs"])
    elif sd["Childs"] != {}:
        ff = fd["Childs"]
#        print("ff as made in m_s ", ff)
        (tmp, fd["Childs"]) = merge_childs_struckt(first["Childs"].values(), second["Childs"].values())
        change+=tmp
#        if tmp >0:
#            print("was", ff, "\nadd ", sd["Childs"], change, "\nresult ", fd["Childs"])
#            print("FD ", fd,"\nSD ",sd)
    return (change, fd)


def merge_childs_struckt(fc, sc):
#    print("fc in m_c_s ", fc)
#    print("sc in m_c_s ", sc)
    changes = 0
    result = {}
    for fe in fc:
        in2 = False
        for se in sc:
            if fe["teg"] == se["teg"]:
                (tmp, result[fe["teg"]]) = merge_struct(fe, se)
                changes+=tmp
                in2 = True
        if (not in2):
            result[fe["teg"]] = fe
    for se in sc:
        in1 = False
        for fe in fc:
            if fe["teg"] == se["teg"]:
                in1 = True
        if (not in1):
            result[se["teg"]] = se
            changes+=1
    return (changes, result)


def struct_from_tree(root: ET.Element):
    result = {"teg": root.tag, "list": False}
    if root.attrib == {}:
        result["atrib"] = {}
    else:
        result["atrib"] = root.attrib
    if list(root) != []:
        result["Childs"] = list_to_dict(list(root))
    else:
        result["Childs"] = {}
    return result

def list_to_dict(list: []):
    if list == []:
        return "Empty list"
    internal = []
    for el in list:
        internal.append(struct_from_tree(el))
    result = {}
    for el in internal:
        if internal.count(el) == 1:
            result[el["teg"]] = el
        else:
            teg = el["teg"]
            inlist = []
            for inel in internal:
                if teg == inel["teg"]:
                    inlist.append(inel)
            result[teg] = merge_teg(inlist)
    return result


def merge_teg(list: []):
    if list == []:
        return "empty list"
    elif not all_the_same(list):
        return "differ in list"
    haschilds = False
    withChailds = []
    for el in list :
        if el.__contains__("Childs") :
            haschilds = True
            withChailds.append(el)
    if withChailds != []:
        result = withChailds[0]
    result["list"] = True
    for el in list:
        result["atrib"].update(el["atrib"])
        if ( haschilds ) and el["Childs"] != {}:
            result["Childs"].update(el["Childs"])
    return result

def all_the_same(list: []):
    teg = list[0]["teg"]
    for el in list:
        if el["teg"] != teg:
            return False
    return True
