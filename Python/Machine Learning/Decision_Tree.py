##计算给定数据集的信息熵 
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():     #为所有可能分类创建字典 
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] +=  1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)      #以2为底数求对数
    return shannonEnt

#创建数据  
def createDataSet():  
    dataSet = [[1,1,'yes'],  
               [1,1,'yes'],  
               [1,0,'no'],  
               [0,1,'no'],  
               [0,1,'no']]  
    labels = ['no surfacing', 'flippers']  
    return dataSet, labels  

#依据特征划分数据集  axis代表第几个特征  value代表该特征所对应的值  返回的是划分后的数据集  
def splitDataSet(dataSet, axis, value):  
    retDataSet = []  
    for featVec in dataSet:  
        if featVec[axis] == value:  
            reducedFeatVec = featVec[:axis]  
            reducedFeatVec.extend(featVec[axis+1:])  
            retDataSet.append(reducedFeatVec)
    return retDataSet


#选择最好的数据集(特征)划分方式  返回最佳特征下标  
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1          #特征个数
    baseEntropy = calcShannonEnt(dataEnt)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):               #遍历特征 第i个 
        featureSet = set([example[i] for example in dataSet])  #第i个特征取值集合
        newEntropy = 0.0
        for value in featureSet:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)    #该特征划分所对应的entropy
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#创建树的函数代码   python中用字典类型来存储树的结构 返回的结果是myTree-字典
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if calssList.count(classList[0]) == len(classList):    #类别完全相同则停止继续划分  返回类标签-叶子节点 
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)                      #遍历完所有的特征时返回出现次数最多的  
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value), subLabels)
    return myTree

#多数表决的方法决定叶子节点的分类 ----  当所有的特征全部用完时仍属于多类  
def majorityCnt(classList):  
    classCount = {}  
    for vote in classList:  
        if vote not in classCount.key():  
            classCount[vote] = 0;  
        classCount[vote] += 1
        sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)  #排序函数 operator中的
    return sortedClassCount[0][0]  

#使用决策树执行分类  
def classify(inputTree, featLabels, testVec):  
    firstStr = inputTree.keys()[0]  
    secondDict = inputTree[firstStr]  
    featIndex = featLabels.index(firstStr)   #index方法查找当前列表中第一个匹配firstStr变量的元素的索引  
    for key in secondDict.keys():  
        if testVec[featIndex] == key:  
            if type(secondDict[key]).__name__ == 'dict':  
                classLabel = classify(secondDict[key], featLabels, testVec)  
            else: classLabel = secondDict[key]  
    return classLabel


#决策树的存储  
def storeTree(inputTree, filename):         #pickle序列化对象，可以在磁盘上保存对象  
    import pickle  
    fw = open(filename, 'w')  
    pickle.dump(inputTree, fw)  
    fw.close()  
  
  
def grabTree(filename):               #并在需要的时候将其读取出来  
    import pickle  
    fr = open(filename)  
    return pickle.load(fr)  


# -*- coding: cp936 -*-
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle = 'sawtooth', fc = '0.8')
leafNode = dict(boxstyle = 'round4', fc = '0.8')
arrow_args = dict(arrowstyle = '<-')

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy = parentPt, xycoords = 'axes fraction',\
                            xytext = centerPt, textcoords = 'axes fraction',\
                            va = 'center', ha = 'center', bbox = nodeType, \
                            arrowprops = arrow_args)

# 使用文本注解绘制树节点
def createPlot():
    fig = plt.figure(1, facecolor = 'white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon = False)
    plotNode('a decision node', (0.5,0.1), (0.1,0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3,0.8), leafNode)
    plt.show()


#获取叶子节点数目和树的层数
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if(type(secondDict[key]).__name__ == 'dict'):
            numLeafs += getNumLeafs(secondDict[key])
        else: numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if(type(secondDict[key]).__name__ == 'dict'):
            thisDepth = 1+ getTreeDepth(secondDict[key])
        else: thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth


#更新createPlot代码以得到整棵树
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes   
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
#if you do get a dictonary you know it's a tree, and the first element will be another dict

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

