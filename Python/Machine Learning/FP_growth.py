class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name = nameValue
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc(self, numOccur):
        self.count += numOccur
    def disp(self, ind = 1):
        print (' '*ind, self.name, ' ',self.count)
        for child in self.children.values():
            child.disp(ind + 1)

def createTree(dataset, minSup = 1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0)+dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqitemSet = set(headerTable.keys())
    if len(freqiteamSet) == 0: return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
    retTree = treeNode("Null Set", 1, None)
    for tranSet, count in dataSet.item():
        localD = {}
        for item in tranSet:
            if item in freqitemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            ordereditems = [V[0] for v in sorted(localD, items(),\
                                                 key=lambda p:p[1], reverse = True)]
            updataTree(ordereditems, retTree, headerTable, count)
    return retTree, headerTable
def updataTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[item[0]] = treeNode(item[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[item[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        updataTree(items[1::], inTree.children[items[0]], headerTable, count)
def updataHeader(nodeToTest, targetNode):
    while (noodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeeLink = targetNode

def ascendTree(leafNode, prefixPath):
    if leadNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath(basePat, treeNode):
    conPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])]
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqitemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key = lambda p:p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree,myHead = createTree(condPattBases, minSup)
        if myHead != None:
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
            
