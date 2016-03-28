urlSep = ['<','>','//','(',')', r'"', r"'", ' ', '\t', '\n']
urlTag = ['http://']

def is_sep(ch):
    for c in urlSep:
        if c == ch:
            return True
    return False

def find_first_sep(i,s):
    s_len = len(s)
    while i < s_len:
        if is_sep(s[i]):
            return i
        i+=1
    return s_len

def GetUrl(strPage):
    rtList = []
    for tag in urlTag:
        i = 0
        strPage = str(strPage)
        strPageLen = len(strPage)
        tagLen = len(tag)
        i = strPage.find(tag, i, strPageLen)
        while i != -1:
            begin = i
            end = find_first_sep(begin + tagLen, strPage)
            rtList.append(strPage[begin:end])
            i = strPage.find(tag, end, strPageLen)

    return rtList
