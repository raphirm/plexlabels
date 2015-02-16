__author__ = 'raphi'
import xml.etree.ElementTree as ET
from MediaInfo.MediaInfo import MediaFile
from HttpApi.HttpApi import HttpConn
import operator


def parseXML(xmlfile, conn, intrusive):
    root = ET.fromstring(xmlfile)
    for video in root:
        medias = list(video.iter("Media"))
        if len(medias) > 1:
            print("Duplicate, one needs to be deleted")
            __solveDuplicates(video, conn, intrusive)
        else:
            for media in video:
                for part in media:
                    labels = __getLables(part)
                    if intrusive:
                        if not labels:
                            print("deleting item " + media.attrib["id"])
                            conn.deleteItem(media.attrib["id"])
                        else:
                            print("updating item " + media.attrib["id"] + "with labels" + labels)
                            conn.updateItem(media.attrib["id"], labels)
                    else:
                        if not labels:
                            print("deleting item " + media.attrib["id"])
                            print("i didn't do it, no worries")
                        else:
                            print("updating item " + media.attrib["id"] + "with labels" + labels)
                            print("i didn't do it, no worries")


def __solveDuplicates(video, conn, intrusive):
    mediaLabels = {}
    for media in video:
        for part in media:
            labels = __getLables(part)
            print(media.attrib["id"])
            mediaLabels[media.attrib["id"]] = len(labels)
    sorted_labels = sorted(mediaLabels.items(), key=operator.itemgetter(1)).reverse()
    for media in video:
        for part in media:
            if media.attrib["id"] == sorted_labels.keys()[0]:
                labels = __getLables(part)
                if intrusive:
                    if not labels:
                        print("deleting item " + media.attrib["id"])
                        conn.deleteItem(media.attrib["id"])
                    else:
                        print("updating item " + media.attrib["id"] + "with labels" + labels)
                        conn.updateItem(media.attrib["id"], labels)
                else:
                    if not labels:
                        print("deleting item " + media.attrib["id"])
                        print("i didn't do it, no worries")
                    else:
                        print("updating item " + media.attrib["id"] + "with labels" + labels)
                        print("i didn't do it, no worries")
            else
                if intrusive:
                    print("deleting item " + media.attrib["id"])
                    conn.deleteItem(media.attrib["id"])
                else:
                    print("deleting item " + media.attrib["id"])
                    print("i didn't do it, no worries")


def __getLables(part):
    mediaFile = MediaFile(part.attrib["file"])
    labels = mediaFile.getLabels();

    return labels