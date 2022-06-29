import numpy as np
import math as mt
import time
import networkx as nx



class People:
    def __init__(self,n):
        self.Graph = nx.DiGraph()
        
    def add_node(self,id):
        self.Graph.add_node(id)
        
    def add_edge(self,deptor,creditor,cost=0):
        self.Graph.add_edge(deptor,creditor,weight = cost)
        
class Settle:
    def __init__(self,n,edges):
        self.net_amount = {}
        self.transactions = []
        self.N = n
        
        p=People(n)
        
        for i in range(self.N):
            p.add_node(i)
        for edge in edges:
            p.add_edge(edge[0],edge[1],cost=edge[2])
        """p.add_edge(0,2,cost=20)
        p.add_edge(1,2,cost=14)
        p.add_edge(2,3,cost=5)
        p.add_edge(2,1,cost=5)
        p.add_edge(0,1,cost=8)
        p.add_edge(9,3,cost=5)
        p.add_edge(7,8,cost=12)
        p.add_edge(6,3,cost=6)
        p.add_edge(9,2,cost=14)
        p.add_edge(5,4,cost=4)
        p.add_edge(7,2,cost=3)"""
        
        self.graph = p.Graph
        
    def get_depts(self):
        depts = {}
        nodes = list(self.graph.out_edges)
        for i in range(len(nodes)):
            deptor = nodes[i][0]
            creditor = nodes[i][1]
            if deptor in depts:
                depts[deptor] += self.graph.edges[deptor,creditor]['weight']
            else:
                depts[deptor] = self.graph.edges[deptor,creditor]['weight']
        
        for node in range(self.N):
            if node not in depts:
                depts[node] = 0 
        
        return depts
    
    def get_credits(self):
        credits = {}
        nodes = list(self.graph.out_edges)
        for i in range(len(nodes)):
            deptor = nodes[i][0]
            creditor = nodes[i][1]
            if creditor in credits:
                credits[creditor] += self.graph.edges[deptor,creditor]['weight']
            else:
                credits[creditor] = self.graph.edges[deptor,creditor]['weight']
                
        for node in range(self.N):
            if node not in credits:
                credits[node] = 0 
                
        return credits
    
    def cal_net_amount(self):
        net_amounts = {}
        depts = self.get_depts()
        credits = self.get_credits()
        for node in range(self.N):
            net_amounts[node] = credits[node] - depts[node]
        
        return net_amounts
        
    def settle_up(self):
        
        
        self.net_amount = self.cal_net_amount()
        print(self.net_amount)
        while(self.N>=2):
            max_namount = np.NINF
            min_namount = np.inf
            min_index = 0
            max_index = 0
            for node,namount in self.net_amount.items():
                if namount> max_namount:
                    max_namount = namount
                    max_index = node
                if namount < min_namount:
                    min_namount = namount
                    min_index = node
            
           
            if (max_namount > abs(min_namount)):
                self.net_amount[max_index] = max_namount - abs(min_namount)
                self.net_amount.pop(min_index)
                self.transactions.append((min_index,max_index,abs(min_namount)))
                self.N -= 1
                
            elif (max_namount < abs(min_namount)):
                self.net_amount[min_index] = min_namount + max_namount
                self.net_amount.pop(max_index)
                self.transactions.append((min_index,max_index,max_namount))
                self.N -= 1
                
            else:
                self.net_amount.pop(min_index)
                self.net_amount.pop(max_index)
                self.transactions.append((min_index,max_index,max_namount))
                self.N = self.N - 2

            
        

 
if __name__=='__main__':
    
    n = int(input("Number of nodes: "))
    edges = []
    ans = ""
    while(ans!="y"):
        edge = []
        node1 = int(input("Enter node: "))
        edge.append(node1)
        node2 = int(input("Enter node: "))
        edge.append(node2)
        dept = float(input("Enter dept: "))
        edge.append(dept) 
        edges.append(edge)  
        ans = input("Do you want to stop3? (y/n): ") 
    print(edges)
    
    settle = Settle(n,edges)
    settle.settle_up()
    for tr in settle.transactions:
        print(f"Node {tr[0]} pays node {tr[1]}, {tr[2]} euros")