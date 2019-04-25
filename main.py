from gis import Gis

gs = Gis()

gs.selectAllCities()
gs.selectAllEdges()

delimiter = '\n**************************************\n'

gs.printCities()
print(delimiter)

gs.printCities('population', 'F')
print(delimiter)

gs.selectCities('latitude', 4000, 5000)
gs.selectCities('longitude', 8500, 13000)
gs.printCities()
print(delimiter)

gs.selectAllEdges()

num = 3
gs.printPopulatedStates(num)
print(delimiter)

gs.testMinMaxConsDistance()
print(delimiter)

gs.selectAllCities()
gs.selectAllEdges()

gs.tour('Yakima, WA')

print(delimiter)

gs.unselectAllEdges()
gs.tour('Yakima, WA')
print(delimiter)

gs.selectAllCities()
gs.selectAllEdges()
gs.selectEdges(1500, 3000)

gs.minCut()
print(delimiter)
