import numpy as np


class Node:
    def __init__(self, nodeState, superNode, eachNode):
        self.nodeState = nodeState
        self.superNode = superNode
        self.eachNode = eachNode


class addNodes:
    def __init__(self):
        self.nodeListFront = []

    def add(self, node):
        
        self.nodeListFront.append(node)

    def nodeState(self, nodeState):

        i = 0
        while i < len(self.nodeListFront):
            node = self.nodeListFront[i]
            if (node.nodeState[0] == nodeState[0]).all():
                return True
            i += 1
        return False

    def checkingIsNull(self):

        if self.nodeListFront:
            return False
        else:
            return True

    def deleteNode(self):
        
        if self.checkingIsNull():
            raise Exception("empty")
        else:
            node = self.nodeListFront[-1]
            self.nodeListFront = self.nodeListFront[:-1]
            return node


class queofStack(addNodes):
    def deleteNode(self):
       
        if self.checkingIsNull():
            raise Exception("empty nodeListFront")
        else:
            node = self.nodeListFront[0]
            self.nodeListFront = self.nodeListFront[1:]
            return node


class Puzzle:
    def __init__(self, startPoint, startIndex, results, resultsIndex):
        self.startPoint = [startPoint, startIndex]
        self.results = [results, resultsIndex]
        self.resultantReq = None

    def nodeRelatives(self, nodeState):
       
        puzzleMatririx, (rowws, cols) = nodeState
        resultant = []

        if rowws > 0:
            puzzleMatririx1 = np.copy(puzzleMatririx)
            temp = puzzleMatririx1[rowws][cols]
            puzzleMatririx1[rowws][cols] = puzzleMatririx1[rowws - 1][cols]
            puzzleMatririx1[rowws - 1][cols] = temp
            resultant.append(('up', [puzzleMatririx1, (rowws - 1, cols)]))

        if cols > 0:
            puzzleMatririx1 = np.copy(puzzleMatririx)
            temp = puzzleMatririx1[rowws][cols]
            puzzleMatririx1[rowws][cols] = puzzleMatririx1[rowws][cols - 1]
            puzzleMatririx1[rowws][cols - 1] = temp
            resultant.append(('left', [puzzleMatririx1, (rowws, cols - 1)]))

        if rowws < 2:
            puzzleMatririx1 = np.copy(puzzleMatririx)
            temp = puzzleMatririx1[rowws][cols]
            puzzleMatririx1[rowws][cols] = puzzleMatririx1[rowws + 1][cols]
            puzzleMatririx1[rowws + 1][cols] = temp
            resultant.append(('down', [puzzleMatririx1, (rowws + 1, cols)]))

        if cols < 2:
            puzzleMatririx1 = np.copy(puzzleMatririx)
            temp = puzzleMatririx1[rowws][cols]
            puzzleMatririx1[rowws][cols] = puzzleMatririx1[rowws][cols + 1]
            puzzleMatririx1[rowws][cols + 1] = temp
            resultant.append(('right', [puzzleMatririx1, (rowws, cols + 1)]))

        return resultant

    def displayResult(self):
        resultantReq = self.resultantReq if self.resultantReq is not None else None
        print("starting state of the node:\n", self.startPoint[0], "\n")
        print("result state of node:\n", self.results[0], "\n")
        print("results :\n ")
        resultPath=[]
        resultPath = [eachNode for eachNode, everyCell in zip(resultantReq[0], resultantReq[1])]

        i = 0
        while i < len(resultantReq[0]):
            eachNode = resultantReq[0][i]
            everyCell = resultantReq[1][i]
            print(" move--->: ", eachNode, "\n", everyCell[0], "\n")
            i += 1

        print("resultant path is ", resultPath)


    def missedNodeState(self, nodeState):

        return not any((st[0] == nodeState[0]).all() for st in self.explored_nodes)


    def solving(self):
        self.visitedNodes = 0

        startPoint = Node(nodeState=self.startPoint, superNode=None, eachNode=None)
        nodeListFront = queofStack()
        nodeListFront.add(startPoint)

        self.explored_nodes = []

        while not nodeListFront.checkingIsNull():
            node = nodeListFront.deleteNode()
            self.visitedNodes += 1

            if (node.nodeState[0] == self.results[0]).all():
                resultantReq = []
                while node.superNode is not None:
                    resultantReq.append((node.eachNode, node.nodeState))
                    node = node.superNode
                resultantReq.reverse()
                each_node_of_action, every_cell = zip(*resultantReq)
                self.resultantReq = (list(each_node_of_action), list(every_cell))
                return

            self.explored_nodes.append(node.nodeState)

            new_nodeStates = [(eachNode, nodeState) for eachNode, nodeState in self.nodeRelatives(node.nodeState)
                              if not nodeListFront.nodeState(nodeState) and self.missedNodeState(nodeState)]

            [nodeListFront.add(Node(nodeState=nodeState, superNode=node, eachNode=eachNode)) for eachNode, nodeState in
             new_nodeStates]


print("-----------------------Start Matrix----------------------------------")

rows = int(input("Enter the number of rows of start matrix: "))
cols = int(input("Enter the number of columns of start matrix: "))

startMatrix = np.array([[int(input(f"Enter element [{i}][{j}]: ")) for j in range(cols)] for i in range(rows)])
startMatrix = np.array(startMatrix)
print("start matrix :",startMatrix)

print("------------------------Result Matrix---------------------------------")

print("Give input for result matrix :")
rows = int(input("Enter the number of rows of result matrix: "))
cols = int(input("Enter the number of columns of result matrix: "))

resultMatrix = [[int(input(f"Enter element [{i}][{j}]: ")) for j in range(cols)] for i in range(rows)]
resultMatrix = np.array(resultMatrix)

print("resultmatrix is ", resultMatrix)
startMatrixIndices = (1, 1)
resultmatrixIndices = (1, 0)

p = Puzzle(startMatrix, startMatrixIndices, resultMatrix, resultmatrixIndices)
p.solving()
p.displayResult()

