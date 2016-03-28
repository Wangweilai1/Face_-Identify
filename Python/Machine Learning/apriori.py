def createc1(dataset):
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    return map(frozenset,c1)

def scanD(D,ck,minsuppor):
    sscnt = {}
    for tid in D:
        for can in ck:
            if can.issubset(tid):
                if not sscnt.has_key(can):sscnt[can] = 1
                else: sscnt[can] += 1
    numitems = float(len(D))
    retlist = []
    supportdata = {}
    for key in sscnt:
        support = sscnt[key]/numitems
        if support >= minsupport:
            relist.insert(0,key)
        supportdata[key] = support
    return relist,supportdata

# aprior
def apriorigen(lk,k):
    retlist = []
    lenlk = len(lk)
    for i in range(lenlk):
        for j in range(i+1, lenlk):
            l1 = list(lk[i])[:k-2];
            l2 = list(lk[j])[:k-2];
            l1.sort();l2.sort()
            if l1 == l2:
                relist.append(lk[i] | l2[j])
    return relist
def apriori(dataset, minsupport = 0.5):
    c1 = createc1(dataset)
    d = map(set, dataset)
    l1,supportdata = scand(D,c1,minsupport)
    l = [l1]
    k = 2
    while (len(l[k-2]) > 0):
        ck = apriorigen(l[k-2], k)
        lk, supk = scand(D, ck, minsuport)
        suportdata.updata(supk)
        l.append(lk)
        k += 1
    return l,supportdata

#关联规则生成函数
def generaterules(L,supportdata,minconf = 0.7):
    bigfulelist = []
    for i in range(1, len(L)):
        for freqset in L[i]:
            H1 = [frozenset([item]) for item in freqset]
            if (i > 1):
                rulesfromconseq(freset, H1, supportdata, bigfulelist, minconf)
            else:
                calcconf(freqset, H1, supportdata, bigrulelist,minconf)
    return bigrulelist

def calcconf(freqset, H, suportdata, br1, minconf = 0.7):
    prunedh = []
    for conseq in H:
        conf = supportdata[freqset]/supportdata[freqset - conseq]
        if conf >= minconf:
            print (freqset - conseq, '-->', conseq, 'conf:',conf)
            br1.append((freqset - conseq, conseq, conf))
            prunedh.append(conseq)
    return prunedh

def rulesfromconseq(freqset, H, supportdata, br1, minconf = 0.7):
    m = len(H[0])
    if (len(freqset) > (m + 1)):
        hmp1 = apriorigen(H, m+1)
        hmp1 = calcconf(freqset, hmp1,supportdata,br1,minconf)
        if(len(hmp1) > 1):
            rulesfromconseq(freqset.hmp1,supportdata,br1,minconf)
            


#收集议案
from time import sleep
from votesmart import votesmart
votesmart.apikey = '49024thereoncewasamanfromnantucket94040'
def getactionids():
    actionidlist = [];billtitlelist = []
    fr = open('recent20bills.txt')
    for line in fr.readlines():
        billnum = int(line.split('\t')[0])
        try:
            billdetail = votesmart.votes.getbill(billnum)
            for action in billdetail.actions:
                if action.level == 'house' and\
                   (action.stage == 'passage' or\
                    acrion.stage == 'amendment vote'):
                    actionidd = int(action.actinid)
                    print ('bill: %d has actionid : %d' %(billnum, actionid))
                    actionidlist.append(actionid)
                    billtitlelist.append(line.strip().split('\t')[1])
        except:
            print ("problem getting bill %d" %billnum)
        sleep(1)
    return actionidlist,billtitlelist

def gettranslist(actionidlist,billtitlelist):
    itemmeaning = ['republican', 'democratic']
    for billtitle in billtitlelist:
        itemmeaning.append('%s -- nay'%billtitle)
        itemmeaning.append('%s -- yea'%billtitle)
    transdict = {}
    votecount = 2
    for actionid in actioninlist:
        sleep(3)
        print ('getting votes for actionid: %d'%actionid)
        try:
            votelist = votesmart.votes.getbillactionvotes(actionid)
            for vote in votelist:
                if not transdict.has_key(vote.candidatename):
                    transdict[vote.candidatename] = []
                    if vote.officepartices == 'democratic':
                        transdict[vote.candidatename].append(1)
                    elif vote.officepartices == 'republican':
                        transdict[vote.candidatename].append(0)
                if vote.action == 'Nay':
                    transdict[vote.candidatename].append(votecount)
                elif vote.action == 'Yea':
                    transdict[vote.candidatename].append(votecount + 1)
        except:
            print ("problem getting actionid: %d" % actionid)
        votecount += 2
    return transdict,itemmeaning
