import numpy as np
import random
import heapq as hq
import math
class makeNode:
    def __init__(self,row,col,g,h,makeNode):
        self.row = row
        self.col = col 
        self.g = g
        self.h = h
        self.parent = makeNode
    def priority_fun(self):
        return self.g + self.h
    def __lt__(self,other):
        return self.priority_fun()<other.priority_fun()
    def getParent():
        return self.parent


class makeNode2(makeNode):
    def __init__(self,row,col,g,h,w,makeNode):
        super().__init__(row,col,g,h,makeNode)
        #self.w = w
        self.w = 2*w - 1
    def priority_fun(self):
        return (self.g/self.w) + self.h
    def __lt__(self,other):
        return self.priority_fun()>other.priority_fun()


class focalMakeNode(makeNode):
    def __init__(self,row,col,g,h,w,makeNode):
        super().__init__(row,col,g,h,makeNode)
        #self.w = 2*w - 1
        self.w = w
    def priority_fun(self):
        x = self.h
        y = self.g
        #f = self.g + ((2*self.w-1)*self.h)
        #f = (self.g/self.w) + self.h
        #XDP
        #f = float((1/(2*self.w)))*float(y + (2*self.w - 1)*x + math.sqrt((y - x)**2 + 4*self.w*y*x))
        #XUP
        f = float((1/(2*self.w))) * float(y + x + math.sqrt((y + x)**2 + 4*self.w*(self.w-1)*(x**2)))
        return f 
    def __lt__(self,other):
        return self.priority_fun()<other.priority_fun()

class solution:
    def __init__(self,g,makeNode):
        self.cost = g
        self.node = makeNode
    def __lt__(self,other):
        return self.cost<other.cost



def print_list(list,string):
    star = "*****"
    print(star+string+" start "+star)
    for i in list:
        print(i.row,i.col,i.priority_fun())
    print(star+string+" end "+star)



def IOSPathfinding(map,strow,stcol,enrow,encol,w):
    dimx = map.shape[0]
    dimy = map.shape[1]

    dirx = [1,0,-1,0,1,-1,-1,1]
    diry = [0,1,0,-1,1,1,-1,-1]
    cost = [1,1,1,1,1.414,1.414,1.414,1.414]
    nodeExpand = 1

    opn = []
    focal = []
    closed = []
    anopen = []
    #answer = []
    opnDict = {}
    focalDict = {}
    closedDict = {}
    #answerDict = {}
    h = abs(enrow-strow) + abs(encol-stcol)

    u = makeNode(strow,stcol,0,h,None)
    fu = focalMakeNode(strow,stcol,0,h,w,None)
    anop = makeNode2(strow,stcol,0,h,w,None)

    soln = solution(float('inf'),None)

    opnDict[(u.row,u.col)] = u.g
    focalDict[(fu.row,fu.col)] = fu.g

    hq.heappush(opn,u)
    hq.heappush(focal,fu)
    hq.heappush(anopen,anop)
    #hq.heappush(answer,soln)
    while True:
        #print(len(opn),"open")
        if(len(opn)==0):
            break
        hq.heapify(opn)
        hq.heapify(focal)
        hq.heapify(anopen)
        #print_list(opn,"Open")
        #print_list(focal,"Focal")
        if soln.cost<=(opn[0].priority_fun())*w:
            print(soln.cost,"AnswerIOS")
            print(nodeExpand,"NodeExpandIOS")
            return nodeExpand,soln.cost,True
            break
        else:
            if focal[0].priority_fun()<soln.cost:
                #print(focal[0].priority_fun())
                u = hq.heappop(focal)
                delete = opnDict.pop((u.row,u.col))
                delete = focalDict.pop((u.row,u.col))
                closed.append(u)
                closedDict[(u.row,u.col)] = u.g
                #Should I remove from open??
                for i in opn:
                    if i.row == u.row and i.col==u.col:
                        opn.remove(i)
                        hq.heapify(opn)
                        break
                for i in anopen:
                    if i.row == u.row and i.col == u.col:
                        anopen.remove(i)
                        hq.heapify(anopen)
                        break

                if u.row == enrow and u.col == encol:
                    # if u.g <= w*focal[0].priority_fun():
                    #     soln = solution(u.g,u)
                    #     return nodeExpand,soln.cost,True
                    if u.g<soln.cost:
                        print("Temporary solution")
                        soln = solution(u.g,u)
                        if soln.cost <= (w*anopen[0].priority_fun()):
                            print(soln.cost,"AnswerIOS")
                            print(nodeExpand,"NodeExpandIOS")
                            return nodeExpand,soln.cost,True
                        #hq.heappush(answer,soln)
                else:
                    for it in range(8):
                        p = u.row+dirx[it]
                        q = u.col+diry[it]
                        if(0<=p and p<dimx and 0<=q and q<dimy and map[p][q] != -1 and not ((p,q) in closedDict) and not ((p,q) in opnDict) and not ((p,q) in focalDict) ):
                            #Do i need to see whether there is an another way to find optimal path
                            nodeExpand += 1
                            h = abs(p-enrow) + abs(q-encol)
                            c = makeNode(p,q,u.g+cost[it],h,u)
                            cfu = focalMakeNode(p,q,u.g+cost[it],h,w,u)
                            anop = makeNode2(p,q,u.g+cost[it],h,w,u)
                            opnDict[(p,q)] = u.g + cost[it]
                            focalDict[(p,q)] = u.g + cost[it]
                            hq.heappush(opn,c)
                            hq.heappush(focal,cfu)
                            hq.heappush(anopen,anop)
            else:
                n = hq.heappop(opn)

                print("In open")
                
                delete = opnDict.pop((n.row,n.col))
                if not ((n.row,n.col) in closedDict) :
                    closed.append(n)
                    closedDict[(n.row,n.col)] = n.g

                for i in anopen:
                    if i.row == n.row and i.col == n.col:
                        anopen.remove(i)
                        hq.heapify(anopen)
                        break

                #print("Yes")
                for it in range(8):
                    p = n.row+dirx[it]
                    q = n.col+diry[it]  
                    if(0<=p and p<dimx and 0<=q and q<dimy and map[p][q] != -1):
                        if((p,q) in opnDict and opnDict[(p,q)]>n.g +cost[it]):
                            #print("In open")
                            #print(p,q)
                            opnDict[(p,q)] = n.g + cost[it]
                            for i in opn:
                                if i.row == p and i.col==q:
                                    i.g = opnDict[(p,q)]
                                    #print(p,q,i.priority_fun())
                                    hq.heapify(opn)
                                    break
                            for i in anopen:
                                if i.row == n.row and i.col == n.col:
                                    i.g = opnDict[(p,q)]
                                    hq.heapify(anopen)
                                    break
    #                     # elif (p,q) in focalDict and focalDict[(p,q)]>n.g +1:
    #                     #         #Update cost of child in focal
    #                     #     print("In focal")
    #                     #     focalDict[(p,q)] = n.g + 1
    #                     #     for i in focal:
    #                     #         if i.row == p and i.col==q:
    #                     #             i.g = focalDict[(p,q)]
    #                     #             hq.heapify(focal)
    #                     #             break
                        elif(not ((p,q) in closedDict) and not ((p,q) in opnDict)):
                            #print("In None")
                            nodeExpand += 1
                            h = abs(p-enrow) + abs(q-encol)                                
                            c = makeNode(p,q,n.g+cost[it],h,n)
                            cfu = focalMakeNode(p,q,n.g+cost[it],h,w,n)
                            anop = makeNode2(p,q,n.g+cost[it],h,w,n)
                            opnDict[(p,q)] = n.g + cost[it]
                            focalDict[(p,q)] = n.g + cost[it]
                            hq.heappush(opn,c)
                            hq.heappush(focal,cfu)
                            hq.heappush(anopen,anop)
    #                     # else:
    #                     #     #print("In close or open")
    return nodeExpand,-1,False
    #     if(len(focal)==0):
    #         break
    #     #hq.heapify(opn)
    #     hq.heapify(focal)
    #     u = hq.heappop(focal)
    #     # if((u.row,u.col) in focalDict):
    #     #     print("Yes")
    #     # else:
    #     #     print("No")
    #     delete = focalDict.pop((u.row,u.col))
    #     closed.append(u)
    #     closedDict[(u.row,u.col)] = u.g
    #     if u.row == enrow and u.col == encol:
    #         return nodeExpand,soln.cost,True
    #     for it in range(4):
    #         p = u.row+dirx[it]
    #         q = u.col+diry[it]
    #         if(0<=p and p<dimx and 0<=q and q<dimy and map[p][q] != -1 and not ((p,q) in closedDict) and not ((p,q) in focalDict)):
    #                         #Do i need to see whether there is an another way to find optimal path
    #             #print(p,q)
    #             nodeExpand += 1
    #             h = abs(p-enrow) + abs(q-encol)
    #             #c = makeNode(p,q,u.g+1,h,u)
    #             cfu = focalMakeNode(p,q,u.g+1,h,w,u)
    #             #opnDict[(p,q)] = u.g + 1
    #             focalDict[(p,q)] = u.g + 1
    #             #hq.heappush(opn,c)
    #             hq.heappush(focal,cfu)
    # return nodeExpand,-1,False



                



def AStarEpsilon(map,strow,stcol,enrow,encol,w):
    dimx = map.shape[0]
    dimy = map.shape[1]

    dirx = [1,0,-1,0,1,-1,-1,1]
    diry = [0,1,0,-1,1,1,-1,-1]
    cost = [1,1,1,1,1.414,1.414,1.414,1.414]

    nodeExpand = 1

    opn = []
    closed = []
    
    
    opnDict = {}
    closedDict = {}
    
    h = abs(enrow-strow) + abs(encol-stcol)

    u = makeNode(strow,stcol,0,h,None)

    opnDict[(u.row,u.col)] = u.g
    
    hq.heappush(opn,u)

    while True:
        #print(len(focal))
        hq.heapify(opn)
        #print_list(opn,"Open")
        if(len(opn)==0):
            break
        focal = []
        v = opn[0]
        #print("Best node from open",v.row,v.col,v.priority_fun())
        for i in opn:
            if i.priority_fun()  <= v.priority_fun() * w:
                #print("yes")
                focal.append(i)
        maxi = float('inf')
        for i in focal:
            if(i.h<maxi):
                maxi = i.h
                u = i

        #print_list(focal,"Focal")

        for i in opn:
            if i.row == u.row and i.col==u.col:
                opn.remove(i)
                opnDict.pop((i.row,i.col))
                hq.heapify(opn)
                break
        
        closed.append(u)
        closedDict[(u.row,u.col)] = u.g
        #print("extracted from focal",u.row,u.col)

        
        if u.row == enrow and u.col == encol:
            print(u.g,"AnswerAEps")
            print(nodeExpand,"NodeExpandAEps")
            return nodeExpand,u.g,True
        
        for it in range(8):
                        p = u.row+dirx[it]
                        q = u.col+diry[it]
                        if(0<=p and p<dimx and 0<=q and q<dimy and map[p][q] != -1 and not ((p,q) in closedDict) and not ((p,q) in opnDict) ):
                            #Do i need to see whether there is an another way to find optimal path
                            #print("Child")
                            #print(p,q)
                            nodeExpand += 1
                            h = abs(p-enrow) + abs(q-encol)
                            c = makeNode(p,q,u.g+cost[it],h,u)
                            #print(p,q,c.priority_fun())
                            #cfu = focalMakeNode(p,q,u.g+1,h,w,u)
                            opnDict[(p,q)] = u.g + cost[it]
                            #focalDict[(p,q)] = u.g + 1
                            hq.heappush(opn,c)
                            #hq.heappush(focal,cfu)
                        # elif((p,q) in closedDict and closedDict[(p,q)]>u.g + 1):
                        #     #print("Updating closed dict")
                        #     #print(p,q)
                        #     delete = closedDict.pop((p,q))
                        #     nodeExpand += 1
                        #     h = abs(p-enrow) + abs(q-encol)
                        #     c = makeNode(p,q,u.g+1,h,u)
                        #     #print(p,q,c.priority_fun())
                        #     opnDict[(p,q)] = u.g + 1
                        #     hq.heappush(opn,c)
                        elif((p,q) in opnDict and opnDict[(p,q)]>u.g +cost[it]):
                            #print("child")
                            #print(p,q)
                            opnDict[(p,q)] = u.g + cost[it]
                            for i in opn:
                                if i.row == p and i.col==q:
                                    i.g = opnDict[(p,q)]
                                    #print(p,q,i.priority_fun())
                                    hq.heapify(opn)
                                    break
        
        #v = opn[0]
        #print("Best node from open1",v.row,v.col)
    return nodeExpand,-1,False




def AStarSearch(map,strow,stcol,enrow,encol,w):
    dimx = map.shape[0]
    dimy = map.shape[1]

    dirx = [1,0,-1,0,1,-1,-1,1]
    diry = [0,1,0,-1,1,1,-1,-1]
    cost = [1,1,1,1,1.414,1.414,1.414,1.414]

    nodeExpand = 1

    opn = []
    closed = []
    
    opnDict = {}
    closedDict = {}
    
    h = abs(enrow-strow) + abs(encol-stcol) 

    u = makeNode(strow,stcol,0,h,None)

    opnDict[(u.row,u.col)] = u.g
    
    hq.heappush(opn,u)

    while True:
        #print(len(opn))
        if(len(opn)==0):
            break
        hq.heapify(opn)
    
        u = hq.heappop(opn)
        
        for i in opn:
            if i.row == u.row and i.col==u.col:
                opn.remove(i)
                opnDict.pop((i.row,i.col))
                hq.heapify(opn)
                break
        
        closed.append(u)
        closedDict[(u.row,u.col)] = u.g


        
        if u.row == enrow and u.col == encol:
            print(u.g,"AnswerAStar")
            print(nodeExpand,"NodeExpandAStar")
            return nodeExpand,u.g,True
        
        for it in range(8):
                        p = u.row+dirx[it]
                        q = u.col+diry[it]
                        if(0<=p and p<dimx and 0<=q and q<dimy and map[p][q] != -1 and not ((p,q) in closedDict) and not ((p,q) in opnDict) ):
                            #Do i need to see whether there is an another way to find optimal path
                            #print("yes")
                            nodeExpand += 1
                            h = abs(p-enrow) + abs(q-encol)
                            c = makeNode(p,q,u.g+cost[it],h,u)
                            opnDict[(p,q)] = u.g + cost[it]
                            hq.heappush(opn,c)
                        elif((p,q) in closedDict and closedDict[(p,q)]>u.g + cost[it]):
                            #print("yes")
                            delete = closedDict.pop((p,q))
                            nodeExpand += 1
                            h = abs(p-enrow) + abs(q-encol)
                            c = makeNode(p,q,u.g+cost[it],h,u)
                            opnDict[(p,q)] = u.g + cost[it]
                            hq.heappush(opn,c)
                        elif((p,q) in opnDict and opnDict[(p,q)]>u.g +cost[it]):
                            #print("yes")
                            opnDict[(p,q)] = u.g + cost[it]
                            for i in opn:
                                if i.row == p and i.col==q:
                                    i.g = opnDict[(p,q)]
                                    #hq.heapify(opn)
                                    break

    return nodeExpand,-1,False






def init():
    random.seed = 0
    a = []
    i = 0
    f = open("dao-map/den401d.map","r")
    dimx = -1
    dimy = -1

    for s in f:
        #print(len(s))
        if i >= 4:
            temp = []
            for j in range(len(s)):
                #print(s[j])
                if s[j] == '@' or s[j] =='T':
                    temp.append(-1) 
                else:
                    temp.append(0)
            a.append(temp)
        else:
            inp = s.split(" ")
            if inp[0] == "height":
                dimx = int(inp[1])
            elif inp[0] == "width":
                dimy = int(inp[1])
        i += 1
    a = np.array(a)
    #print(a)
    # dimx = a.shape[0]
    # dimy = a.shape[1]
    #print(dimx,dimy,a.shape)
    #strow = -1
    #stcol = -1,enrow = -1,encol = -1,
    nodeExpandIOS = 0
    nodeExpandAEps = 0
    nodeExpandAStar = 0
    ratio_soln_cost_ios = 0
    ratio_soln_cost_AEps = 0
    ratio_node_expand_ios = 0
    ratio_node_expand_AEps = 0
    instances = 40
    for j in range(instances):
        while True:
            while True:
                strow = random.randint(0,dimx-1)
                stcol = random.randint(0,dimy-1)
                if (a[strow][stcol] != -1):
                    while True:
                        enrow = random.randint(0,dimx-1)
                        encol = random.randint(0,dimy-1)
                        if (a[enrow][encol] != -1):
                            break
                    break
            # strow = 19
            # stcol = 38
            # enrow = 27
            # encol = 41
            flag = True
            print(strow,stcol,enrow,encol,abs(enrow-strow)+abs(encol-stcol))
            w=1.75
            node1,val1,flag = IOSPathfinding(a,strow,stcol,enrow,encol,w)
            if flag:
                nodeExpandIOS += node1
            flag = False
            node2,val2,flag = AStarEpsilon(a,strow,stcol,enrow,encol,w)
            if flag:
                nodeExpandAEps += node2
            flag = False
            node3,val3,flag = AStarSearch(a,strow,stcol,enrow,encol,1.0)
            if flag:
                ratio_soln_cost_ios += val1/val3
                ratio_soln_cost_AEps += val2/val3
                ratio_node_expand_ios += node1/node3
                ratio_node_expand_AEps += node2/node3
                nodeExpandAStar += node3
                break
    nodeExpandIOS/= instances
    nodeExpandAEps/= instances
    nodeExpandAStar/= instances
    ratio_soln_cost_ios/=instances
    ratio_soln_cost_AEps/=instances
    ratio_node_expand_ios/=instances
    ratio_node_expand_AEps/=instances
    print(nodeExpandIOS,"Average Node Expansion(IOS)")
    print(nodeExpandAEps,"Average Node Expansion(AEPs)")
    print(nodeExpandAStar,"Average Node Expansion(AStar)")
    print(ratio_soln_cost_ios,"Average ratio of solution cost(IOS)")
    print(ratio_soln_cost_AEps,"Average ratio of solution cost(AEPs)")
    print(ratio_node_expand_ios,"Average ratio of node expansion(IOS)")
    print(ratio_node_expand_AEps,"Average ratio of node expansion(AEPs)")
def main():
    init()
if __name__=="__main__": 
    main() 