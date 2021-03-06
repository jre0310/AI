# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    return  [w, w, w, w, s, s, e, s, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # print "Start:" , problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    # get starting location of pacman
    startLoc = problem.getStartState()  

    # list to store the explored nodes 
    explored = [] 
    
    # Create the fringe as a stack and push the initial location 
    fringe = util.Stack()

    # Each node in the fringe will consist of a location, list of moves, and cost
    fringe.push((startLoc, [], 0))

    # Start the DFS
    while(not fringe.isEmpty()):

        # Pop a node from the fringe to use 
        currentNode, directions, cost = fringe.pop()
        
        # Check to see if the current node is a goal state, if it is, return the list of directions 
        if problem.isGoalState(currentNode):
            return directions
        
        # Check to make sure that the current node is not already in the set of explored nodes
        # If it is, it means that you looped around and there is not solution
        if currentNode not in explored:

            # Since it is not in the explored nodes, add it to the explored nodes
            explored.append(currentNode)
            
            # For each successor of the current node, if it is not in explored list, push it to the stack
            for node, direction, cost in problem.getSuccessors(currentNode):
                if node not in explored:
                    fringe.push((node, directions + [direction], cost))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    #breadth first uses queue
    fringe = util.Queue()
    visited = []

    #the fringe should consist the state, a list containing the actions executed
    #to reach the state, and cost (cost in dfs & bfs doesnt matter)
    #format same as that obtained from the defined function
    fringe.push((startState, [], 0))

    #keep popping till no more nodes in the fringe
    while not fringe.isEmpty():
        currentState, actions, costs = fringe.pop()
        #curcial as this prevents expanding the same node twice
        if not currentState in visited:
            #update visited status
            visited.append(currentState)
            #if this goal state return the actions to reach it
            if problem.isGoalState(currentState):
                return actions
            #push all successors not in visited
            for state, action, cost in problem.getSuccessors(currentState):
                if not state in visited:
                    fringe.push((state, actions + [action], cost))


    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # get starting location of pacman
    startLoc = problem.getStartState()  

    # list to store the explored nodes 
    explored = [] 
    
    # Create the fringe as a stack and push the initial location 
    fringe = util.PriorityQueue()

    # Each node in the fringe will consist of a location, list of moves, and cost
    fringe.push((startLoc, [], 0), 0)

    while(not fringe.isEmpty()):
        
        currentNode, directions, costs = fringe.pop()

        if problem.isGoalState(currentNode):
            return directions

        if currentNode not in explored:
            explored.append(currentNode)

            for nextNode, direction, cost in problem.getSuccessors(currentNode):
                if nextNode not in explored:
                    fringe.push((nextNode, directions + [direction], costs + cost), costs + cost)


    # this is a change that I made on my laptop

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    startLoc = problem.getStartState()

    explored = []

    fringe = util.PriorityQueue()

    fringe.push((startLoc, [], 0), 0)

    while(not fringe.isEmpty()):

        currentNode, directions, costs = fringe.pop()

        if problem.isGoalState(currentNode):
            return directions

        if currentNode not in explored:
            explored.append(currentNode)

            for nextNode, direction, cost in problem.getSuccessors(currentNode):
                if nextNode not in explored:
                    heuristicCost = costs + cost + heuristic(nextNode, problem)
                    fringe.push((nextNode, directions + [direction], costs + cost), heuristicCost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
