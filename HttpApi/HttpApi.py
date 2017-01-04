__author__ = 'raphi'
import http.client
import xml.etree.ElementTree as ET
import time

class HttpConn:
    def __init__(self, host, token, sections):
        self.host = host
        self.token = "X-Plex-Token=" + token
        self.sections = sections

    def testconnection(self):
        connection = http.client.HTTPConnection(self.host + ":32400")

        connection.request("GET", "/?" + self.token)
        errorcode = connection.getresponse().status
        if errorcode < 400:
            return True
        else:
            return False

    def getoverview(self):
        sectionoverview = []
        sections = self.sections.split(",")
        for section in sections:
            connection = http.client.HTTPConnection(self.host + ":32400")
            connection.request("GET", "/library/sections/" + section + "/all?duplicate=1&" + self.token)
            sectionoverview.append(connection.getresponse().read())
        return sectionoverview
    def getnew(self):
        sectionoverview = []
        sections = self.sections.split(",")
        for section in sections:
            connection = http.client.HTTPConnection(self.host + ":32400")
            connection.request("GET", "/library/sections/" + section + "/recentlyAdded?" + self.token)
            sectionoverview.append(connection.getresponse().read())
        return sectionoverview
    def updateItem(self, itemid, labels):
        connection = http.client.HTTPConnection(self.host + ":32400")
        connection.request("GET", itemid+"?"+self.token);
        item = connection.getresponse().read()
        updatestring = parseItem(item, labels)


        #print(itemid + "/" + updatestring + "&" + self.token)
        if updatestring != "False":
            connection.request("PUT", itemid + "/" + updatestring + "&" + self.token)
        time.sleep(0.5)
    def deleteItem(self, itemid):
        connection = http.client.HTTPConnection(self.host + ":32400")
        connection.request("DELETE", itemid + "?" + self.token)
        time.sleep(0.5)

    def getItem(self, itemid):
        connection = http.client.HTTPConnection(self.host+ ":32400")
        connection.request("GET", itemid + "?" + self.token)
        return connection.getresponse().read()

    def deleteMedia(self, mediaid, videoid):
        connection = http.client.HTTPConnection(self.host + ":32400")
        connection.request("DELETE", videoid + "/media/" + mediaid + "?" + self.token)
        time.sleep(0.5)



if __name__ == "__main__":
    import sys;

    bla = HttpConn(sys.argv[1], sys.argv[2], sys.argv[3])
    if bla.testconnection():
        overviews = bla.getoverview();


def parseItem(item, lls):
    root = ET.fromstring(item)
    collections = []
    labels = []
    manual = False
    for collection in root.findall('Video/Collection'):
        if not ".audio" in collection.attrib["tag"]:
            collections.append(collection.attrib["tag"])
    for label in root.findall('Video/Label'):
        if not ".audio" in label.attrib["tag"]:
            labels.append(label.attrib["tag"])
        if "Manualtag" in label.attrib["tag"]:
            manual = True
    #print(", ".join(collections) + " and " + ", ".join(labels))
    updatestring = ""
    i = 0
    for collection in collections:
        if i == 0:
            updatestring = "?"
        else:
            updatestring = updatestring + "&"
        updatestring = updatestring + "collection[" + repr(i) + "].tag.tag=" + collection
        i = i + 1
    j = 0
    for label in labels:
        if i == 0:
            updatestring = "?"
        else:
            updatestring = updatestring + "&"
        updatestring = updatestring + "label[" + repr(j) + "].tag.tag=" + label
        j = j + 1


    for label in lls:
            if not updatestring:
                updatestring = "?"
            else:
                updatestring = updatestring + "&"
            updatestring = updatestring + "label[" + repr(
                i) + "].tag.tag=" + label
            j = j + 1
            i = i + 1
    #updatestring = "?label[0].tag.tag=movie&collection[0].tag.tag=movie"
    #print(updatestring)

    if manual == True:
        print("Ignoring element because its tagged as manual tag")
        return "True"
    else:
        return updatestring.encode("ascii", "ignore").decode()
