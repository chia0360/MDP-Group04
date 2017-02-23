# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


class Node:
    def __init__(self, x, y):
        self.XNode = x
        self.YNode = y
        self.GCost = 0
        self.HCost = 0
        self.FCost = 0
        self.CameFrom = None
