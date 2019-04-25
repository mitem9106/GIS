import networkx as nx
import matplotlib.pyplot as plt

class Gis:
        def __init__(self):
                
                self.file = open('gis.dat', 'r')
                self.lines = self.file.readlines()
                self.file.close()
                
                self.cities = []
                self.states = []
                self.latitudes = []
                self.longitudes = []
                self.populations = []
                self.distances = []
                
                self.node = 0 #current node being added
                self.j = 0
                self.G = nx.Graph() #Graph that holds all the data
                self.curCity = " " #variable that keeps track of the current city while inputting its distances to other cities
                self.selected = nx.Graph() #Graph for holding selected cities
                self.selected2 = nx.Graph() #Secondary graph for holding selected cities within a set of already selected cities
                
                self.nodesSelected = False #Check to see if some cities have already been selected
                self.edgesSelected = False #Check to see if some edges have already been selected
                self.discovered = False
                self.discoveredE = False

                for line in self.lines: #loop through every line in the dat file
                        if line[0].isalpha(): #if the current line is city(node) data
                                self.j=0
                                self.temp = line.split(", ")[0]
                                self.cities.append(self.temp)
                                
                                self.temp = line.replace("[",",").split(",")[1]
                                self.temp = self.temp.strip(' ')
                                self.states.append(self.temp)
                                
                                self.temp = line.replace("[",",").split(",")[2]
                                self.latitudes.append(self.temp)
                                
                                self.temp = line.replace("[",",").replace("]",",").split(",")[3]
                                self.longitudes.append(self.temp)
                                
                                self.temp = line.replace("[",",").replace("]",",").split(",")[4]
                                self.temp = self.temp.strip('\n')
                                self.populations.append(self.temp)
                                
                                self.G.add_node(self.cities[self.node], name=self.cities[self.node], state=self.states[self.node], latitude=self.latitudes[self.node], longitude=self.longitudes[self.node], population=self.populations[self.node])
                                self.curCity = self.cities[self.node]
                                self.node=self.node+1
                        elif line[0].isdigit(): #if the current line is distance(edge) data
                                for i in range(len(line.split())-1,-1,-1):
                                        self.G.add_edge(self.curCity, self.cities[self.j], distance=int(line.split()[i]))
                                        #print(self.cities[self.j])
                                        self.j=self.j+1

        #select edges based on a lower and upper bound: selectEdges(lowerBound, upperBound(optional))
        def selectEdges(self, lowerBound, upperBound=None):
                if self.nodesSelected is False: #Check for selected cities
                        return(print("No cities selected!"))

                if upperBound is None: #if only one value is given, select edges up-to this value
                        upperBound = lowerBound
                        lowerBound = 0

                if self.edgesSelected is False: #if the set of edges is empty, take from all available edges
                        self.discoveredE = False
                        for i in self.G.edges:
                                u = i[0]
                                v = i[1]
                                if u in self.selected and v in self.selected: #find the edges between selected cities
                                        d = int(self.G.edges[u, v]['distance'])
                                        if d>=lowerBound and d<=upperBound: #select edges within the given parameters
                                                self.selected.add_edge(u, v, distance=self.G.edges[i]['distance'])
                                                self.discoveredE = True
                        if self.discoveredE is True:
                                self.edgesSelected = True
                        else:
                                print("No edges found!")
                else: #if the set of edges is not empty, take from the existing set
                        self.discoveredE = False
                        self.selected2.clear()
                        self.selected2.add_nodes_from(self.selected.nodes) 
                        for i in self.selected.edges:
                                u = i[0]
                                v = i[1]
                                if u in self.selected2 and v in self.selected2:
                                        d = int(self.selected.edges[u, v]['distance'])
                                        if d>=lowerBound and d<=upperBound:
                                                self.selected2.add_edge(u, v, distance=self.selected.edges[i]['distance'])
                                                self.discoveredE = True
                        if self.discoveredE is True:
                                self.selected2.add_nodes_from(self.selected.nodes(data=True))
                                self.selected.clear()
                                self.selected.add_nodes_from(self.selected2.nodes(data=True))
                                self.selected.add_edges_from(self.selected2.edges(data=True))
                        else:
                                print("No edges found!")
                
        #select cities based on a chosen attribute: selectCities('attribute', lowerBound, upperBound(optional))
        def selectCities(self, attribute, lowerBound, upperBound=None):
                if upperBound is None:
                        if attribute is 'name' or attribute is 'state':
                                upperBound = lowerBound
                        else:
                                upperBound = lowerBound
                                lowerBound = 0
                        
                if self.nodesSelected is True: #if some nodes have already been selected then we take from already selected nodes
                        self.selected2.clear()
                        self.discovered = False
                        for i in self.selected.nodes:
                                if attribute is not 'name' and attribute is not 'state': #if the attribute involves integers
                                        if int(self.selected.nodes[i][attribute])>=lowerBound and int(self.selected.nodes[i][attribute])<=upperBound:
                                                self.selected2.add_node(self.selected.nodes[i]['name'], name=self.selected.nodes[i]['name'], state=self.selected.nodes[i]['state'], latitude=self.selected.nodes[i]['latitude'], longitude=self.selected.nodes[i]['longitude'], population=self.selected.nodes[i]['population'])
                                                self.discovered = True
                                elif attribute is 'name': #if the attribute is name we have to get the value of the first character in the name
                                        c = self.selected.nodes[i][attribute]
                                        if ord(c[0])>=ord(lowerBound) and ord(c[0])<=ord(upperBound):
                                                self.selected2.add_node(self.selected.nodes[i]['name'], name=self.selected.nodes[i]['name'], state=self.selected.nodes[i]['state'], latitude=self.selected.nodes[i]['latitude'], longitude=self.selected.nodes[i]['longitude'], population=self.selected.nodes[i]['population'])
                                                self.discovered = True
                                elif attribute is 'state': #if the attribute is state we just have to compare the states'
                                        s = self.selected.nodes[i][attribute]
                                        if s[0] is lowerBound[0] and s[1] is lowerBound[1]:
                                                self.selected2.add_node(self.selected.nodes[i]['name'], name=self.selected.nodes[i]['name'], state=self.selected.nodes[i]['state'], latitude=self.selected.nodes[i]['latitude'], longitude=self.selected.nodes[i]['longitude'], population=self.selected.nodes[i]['population'])
                                                self.discovered = True
                        if self.discovered is True:
                                self.selected.clear()
                                self.selected.add_nodes_from(self.selected2.nodes(data=True))
                                self.unselectAllEdges()
                        else:
                                print("No cities found!")
                else: #if we haven't already selected some nodes then we take from the original graph
                        self.discovered = False
                        for i in self.G.nodes:
                                if attribute is not 'name' and attribute is not 'state': #if the attribute involves numeric values
                                        if int(self.G.nodes[i][attribute])>=lowerBound and int(self.G.nodes[i][attribute])<=upperBound:
                                                self.selected.add_node(self.G.nodes[i]['name'], name=self.G.nodes[i]['name'], state=self.G.nodes[i]['state'], latitude=self.G.nodes[i]['latitude'], longitude=self.G.nodes[i]['longitude'], population=self.G.nodes[i]['population'])
                                                self.discovered = True
                                elif attribute is 'name': #if the attribute is name we have to get the value of the first character in the name
                                        c = self.G.nodes[i][attribute]
                                        if ord(c[0])>=ord(lowerBound) and ord(c[0])<=ord(upperBound):
                                                self.selected.add_node(self.G.nodes[i]['name'], name=self.G.nodes[i]['name'], state=self.G.nodes[i]['state'], latitude=self.G.nodes[i]['latitude'], longitude=self.G.nodes[i]['longitude'], population=self.G.nodes[i]['population'])
                                                self.discovered = True
                                elif attribute is 'state': #if the attribute is state we just have to compare the states
                                        s = self.G.nodes[i][attribute]
                                        if s[0] is lowerBound[0] and s[1] is lowerBound[1]:
                                                self.selected.add_node(self.G.nodes[i]['name'], name=self.G.nodes[i]['name'], state=self.G.nodes[i]['state'], latitude=self.G.nodes[i]['latitude'], longitude=self.G.nodes[i]['longitude'], population=self.G.nodes[i]['population'])
                                                self.discovered = True
                        if self.discovered is True:
                                self.nodesSelected = True
                                self.unselectAllEdges()
                        else:
                                print("No cities found!")

        #selects all cities in the graph: selectAllCities()
        def selectAllCities(self): 
                self.selected.add_nodes_from(self.G.nodes(data=True))
                self.nodesSelected = True
                self.unselectAllEdges()

        #unselects all selected cities: unselectAllCities()
        def unselectAllCities(self): 
                self.selected.clear()
                self.nodesSelected = False

        #selects all edges in the graph: selectAllEdges()
        def selectAllEdges(self): 
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                if self.edgesSelected is False and self.nodesSelected is False: #take all given edges if none have yet been selected
                        self.selected.add_edges_from(self.G.edges(data=True))
                        self.edgesSelected = True
                else: #take all edges in the selected set
                        for i in self.G.edges:
                                u = i[0]
                                v = i[1]
                                if u in self.selected.nodes and v in self.selected.nodes:
                                        self.selected.add_edge(u, v, distance=self.G.edges[i]['distance'])
                        self.edgesSelected = True

        #unselects all selected edges: unselectAllEdges()
        def unselectAllEdges(self): 
                self.selected.remove_edges_from(self.selected)
                self.edgesSelected = False
                
        #prints the selected edges in no particular order: printEdges()
        def printEdges(self):
                if self.edgesSelected is False:
                        return(print("No edges selected!"))
                for i in self.selected.edges(data=True):
                        print(i)
                
        #prints a list of currently-selected cities in increasing order according to the attribute: printCities() or printCities('attribute', 'format')
        def printCities(self, attribute="name", choice='S'): 
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                
                if attribute is "name":
                        self.templst = sorted(list(self.selected.nodes))
                        
                        if choice is 'S': #print in short form
                                for i in self.templst:
                                        print(self.selected.nodes[i]['name'], ", ", self.selected.nodes[i]['state'], sep='')
                        elif choice is 'F': #print in full form
                                for i in self.templst:
                                        print(self.selected.nodes[i]['name'], ", ", self.selected.nodes[i]['state'], " [", self.selected.nodes[i]['latitude'], ", ", self.selected.nodes[i]['longitude'], "], ", self.selected.nodes[i]['population'], sep='')
                elif attribute is "state": #these elif statements sort the selected cities based on the requested attribute
                        self.templst = sorted((nx.get_node_attributes(self.selected, 'state')).items(), key=lambda x: x[1])
                elif attribute is "latitude":
                        self.templst = sorted((nx.get_node_attributes(self.selected, 'latitude')).items(), key=lambda x: int(x[1]))
                elif attribute is "longitude":
                        self.templst = sorted((nx.get_node_attributes(self.selected, 'longitude')).items(), key=lambda x: int(x[1]))
                elif attribute is "population":
                        self.templst = sorted((nx.get_node_attributes(self.selected, 'population')).items(), key=lambda x: int(x[1]))

                if choice is 'S' and attribute is not "name": #print in short form
                        for i in self.templst:
                                print(self.selected.nodes[i[0]]['name'], ", ", self.selected.nodes[i[0]]['state'], sep='')
                elif choice is 'F' and attribute is not "name": #print in full form
                        for i in self.templst:
                                print(self.selected.nodes[i[0]]['name'], ", ", self.selected.nodes[i[0]]['state'], " [", self.selected.nodes[i[0]]['latitude'], ", ", self.selected.nodes[i[0]]['longitude'], "], ", self.selected.nodes[i[0]]['population'], sep='')

        #build a graph out of the selected cities and edges: makeGraph()
        def makeGraph(self):
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                plt.subplot(111)
                nx.draw_networkx(self.selected)
                plt.show()

        #minimize the maximum distance between two cities: testMinMaxConsDistance()
        def testMinMaxConsDistance(self):
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                if self.edgesSelected is False:
                        return(print("No edges selected!"))
                print("Goal: minimize the maximum distance between any pair of")
                print("consecutive cities on path from source to destination\n")
                while True: #runs until the user enters no information
                        source = input('Source (City, State): ')
                        if source is '':
                                print("Target (City, State): ")
                                break
                        sourceCity = source.split(", ")[0]
                        sourceState = source.split(", ")[1]
                        
                        target = input('Target (City, State): ')
                        if target is '':
                                break
                        targetCity = target.split(", ")[0]
                        targetState = target.split(", ")[1]

                        if self.selected.has_node(sourceCity) is False: #make sure the requested source and target exist
                                print("Source city is not selected!")
                        elif self.selected.has_node(targetCity) is False:
                                print("Target city is not selected!")
                        else:
                                ss = self.selected.nodes[sourceCity]['state']
                                ts = self.selected.nodes[targetCity]['state']
                                if ss[0] is not sourceState[0] or ss[1] is not sourceState[1]:
                                        print("Source state is incorrect!")
                                elif ts[0] is not targetState[0] or ts[1] is not targetState[1]:
                                        print("Target state is incorrect!")
                                else:
                                        if nx.has_path(self.selected, source=sourceCity, target=targetCity) is False: #Make sure there is a path between source and target
                                                print("A path does not exist within the selected cities and edges!")
                                        else:
                                                path = nx.shortest_path(self.selected, source=sourceCity, target=targetCity, weight='distance') #determine the shortest path
                                                cost = nx.shortest_path_length(self.selected, source=sourceCity, target=targetCity, weight='distance') #determine the cost of the shortest path
                                                print("Cost of optimal solution: ", cost)
                                                print("\nPath from ", sourceCity, ", ", sourceState, " to ", targetCity, ", ", targetState, ":", sep='')
                                                for i in path:
                                                        print(i, ", ", self.selected.nodes[i]['state'], sep='')

                                
                        
        #Travelling salesman tour: tour('city, state')
        def tour(self, start):
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                if self.edgesSelected is False:
                        return(print("No edges selected!\n", "Traveling Salesman tour starting from ", start, " is not possible.", sep=''))
                temp = start #holds the source for printing
                start = temp.split(", ")[0] #get the city name
                pathsAvailable = True
                tsTour = nx.Graph() #separate graph for the tour
                tsPath = []
                tsTour.add_nodes_from(self.selected.nodes(data=True))
                tsTour.add_edges_from(self.selected.edges(data=True))
                for i in tsTour.nodes: #set each node to 'unvisited'
                        tsTour.nodes[i]['visited'] = 0
                tsPath.append(tsTour.nodes[start]) #add the starting city to the tour
                tsTour.nodes[start]['visited'] = 1 #mark the starting city as visited
                curNode = start
                tourLength = 0
                while True:
                        shortestPath = 9999999
                        pathsAvailable = False
                        for i in tsTour.nodes:
                                if tsTour.nodes[i]['visited'] is 0: #look at distance only if the city is unvisited
                                        if tsTour.has_edge(curNode, i) is True:
                                                if tsTour.edges[curNode, i]['distance']<=shortestPath: #find the closest city
                                                        shortestPath = tsTour.edges[curNode, i]['distance']
                                                        nextNode = i
                                                pathsAvailable = True
                        if pathsAvailable is False: #loop until there are no more unvisited cities
                                break
                        tsPath.append(tsTour.nodes[nextNode]) #add the closest city to the tour
                        tsTour.nodes[nextNode]['visited'] = 1 #mark the closest city as visited
                        tourLength = tourLength + tsTour.edges[curNode, nextNode]['distance'] #calculate the length of the tour
                        curNode = nextNode
                tsPath.append(tsTour.nodes[start]) #add the starting city to the end of the tour

                if len(tsPath) is 2: #if the only city visited was the starting city
                        return(print("Traveling Salesman tour starting from ", temp, " is not possible.", sep=''))
                print("Traveling Salesman Tour starting from", temp, "is as follows\n")
                
                remainder = len(tsPath)%4
                linesOf4 = len(tsPath)//4
                if remainder is 0: #if the number of cities in the tour is a multiple of 4
                        for i in range(linesOf4):
                                bp1 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp2 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp3 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp4 = tsPath[0]['name']
                                tsPath.pop(0)
                                print(tsTour.nodes[bp1]['name'], ", ", tsTour.nodes[bp1]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp2]['name'], ", ", tsTour.nodes[bp2]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp3]['name'], ", ", tsTour.nodes[bp3]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp4]['name'], ", ", tsTour.nodes[bp4]['state'], sep='')
                elif len(tsPath) < 4: #if the number of cities in the tour is less than 4
                        bp = tsPath[1]['name']
                        print(temp, end=" --> ")
                        print(tsTour.nodes[bp]['name'], ", ", tsTour.nodes[bp]['state'], sep='', end=" --> ")
                        print(temp)
                elif len(tsPath) > 4 and remainder is not 0: #if the number of cities in the tour is greater than 4 but not a multiple of 4
                        for i in range(linesOf4):
                                bp1 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp2 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp3 = tsPath[0]['name']
                                tsPath.pop(0)
                                bp4 = tsPath[0]['name']
                                tsPath.pop(0)
                                print(tsTour.nodes[bp1]['name'], ", ", tsTour.nodes[bp1]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp2]['name'], ", ", tsTour.nodes[bp2]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp3]['name'], ", ", tsTour.nodes[bp3]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp4]['name'], ", ", tsTour.nodes[bp4]['state'], sep='', end=" --> \n")
                        if remainder is 1:
                                print(temp)
                        elif remainder is 2:
                                bp = tsPath[0]['name']
                                print(tsTour.nodes[bp]['name'], ", ", tsTour.nodes[bp]['state'], sep='', end=" --> ")
                                print(temp)
                        elif remainder is 3:
                                bp1 = tsPath[0]['name']
                                bp2 = tsPath[1]['name']
                                print(tsTour.nodes[bp1]['name'], ", ", tsTour.nodes[bp1]['state'], sep='', end=" --> ")
                                print(tsTour.nodes[bp2]['name'], ", ", tsTour.nodes[bp2]['state'], sep='', end=" --> ")
                                print(temp)
                print("Tour length: ", tourLength)

        #Find the minimum cut of a set of selected cities and edges: minCut()
        def minCut(self):
                if self.nodesSelected is False:
                        return(print("No cities selected!"))
                try:
                        cut_value, partition = nx.stoer_wagner(self.selected, weight='distance') #get the weight of the min-cut and the edges in the min-cut
                except nx.NetworkXError:
                        return(print("The graph must be connected to get the minimum cut!"))
                print("The edges in a min-cut are as follows.\n")
                for i in partition[0]:
                        for j in self.selected.edges(i):
                                print("(", j[0], ", ", self.selected.nodes[j[0]]['state'], " , ", j[1], ", ", self.selected.nodes[j[1]]['state'], ")", sep='')
                        
                print("\nWeight of the min-cut: ", cut_value)

        #Find the n most populated states containing the selected cities: printPopulatedStates(num)
        def printPopulatedStates(self, num):
                if self.nodesSelected is False:
                        print("No cities selected!")
                states = {}
                for i in self.selected.nodes(data=True): #create a dictionary of the states and their total populations (based on the selected cities)
                        curState = i[1]['state']
                        states[curState] = int(states.get(curState, 0)) + int(i[1]['population'])
                if num > len(states): #if the user entered a number higher than the number of selected states
                        num = len(states)
                print(num, "most populated states.")
                print("--------------------------------------------------")
                
                for n in range(num):
                        largest = 0
                        for key, value in states.items():
                                if value >= largest: #find the most populated state
                                        largest = value
                                        largestState = key
                        print(largestState, largest)
                        states.pop(largestState)
                        
                        
                        
                
