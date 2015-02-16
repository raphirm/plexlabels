__author__ = 'raphi'
import http.client
class HttpConn:
    def __init__(self, host, token, sections):
        self.host = host
        self.token = "X-Plex-Token="+token
        self.sections = sections

    def testconnection(self):
        connection = http.client.HTTPConnection(self.host + ":32400" )

        connection.request("GET", "/?"+self.token)
        errorcode = connection.getresponse().status
        if errorcode < 400:
            return True
        else:
            return False
    def getoverview(self):
        sectionoverview = []
        sections=self.sections.spli(",")
        for section in sections:
            connection = http.client.HTTPConnection(self.host + ":32400" )
            sectionoverview.append(connection.request("GET", "/library/sections/"+section+"/all?"+self.token))
        return sectionoverview
    def updateItem(self, itemid, labels):
        print("placeholder")
    def deleteItem(self, itemid):
        print("placeholder")
    def deletePart(self, partid):
         print("placeholder")


if __name__ == "__main__":
    import sys;
    bla = HttpConn(sys.argv[1], sys.argv[2], sys.argv[3])
    if bla.testconnection():
        overviews = bla.getoverview();


