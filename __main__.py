__author__ = 'raphi'
from MediaInfo.MediaInfo import MediaFile
from HttpApi.XMLHandler import parseXML
from HttpApi.HttpApi import HttpConn

if __name__ == "__main__":
    import sys;
    overviews = []
    conn = HttpConn(sys.argv[1], sys.argv[2], sys.argv[3])
    intrusive = False
    if len(sys.argv) >= 5:
        if(sys.argv[4] == "intrusive"):
            intrusive = True
            print("make it intrusive")
    if conn.testconnection():
        overviews = conn.getoverview();
    for section in overviews:
        parseXML(section, conn, intrusive)