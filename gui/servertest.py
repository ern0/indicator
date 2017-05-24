import urllib,sys
serverurl="http://localhost:8080/light/"
print urllib.urlopen(serverurl + sys.argv[1]).read()
#print serverurl + sys.argv[1]
