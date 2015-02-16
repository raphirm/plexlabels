__author__ = 'raphi'
import xml.etree.ElementTree as ET
from MediaInfo.MediaInfo import MediaFile
from HttpApi.HttpApi import HttpConn
import operator


def parseXML(xmlfile, conn, intrusive, interval):
    root = ET.fromstring(xmlfile)
    for video in root:
        medias = list(video.iter("Media"))
        validity = 0  
        if interval != 0:
            validity = part.attrib["addedAt"] + interval * 1.5 - localtime()
        if validity < 0:
            continue
        if len(medias) > 1:
            print("Duplicate, one needs to be deleted")
            __solveDuplicates(video, conn, intrusive)
        else:
            for media in video:
                for part in media:
                    labels = __getLables(part)
                    if intrusive:
                        if not labels:
                            print("deleting item " + video.attrib["key"])
                            conn.deleteItem(video.attrib["key"])
                        else:
                            print("updating item " + video.attrib["key"] + " with labels " + ', '.join(labels))
                            conn.updateItem(video.attrib["key"], labels)
                    else:
                        if not labels:
                            print("deleting item " + video.attrib["key"])
                            print("i didn't do it, no worries")
                        else:
                            print("updating item " + video.attrib["key"] + " with labels " + ', '.join(labels))
                            print("i didn't do it, no worries")


def __solveDuplicates(video, conn, intrusive):
    mediaLabels = {}
    for media in video:
        for part in media:
            labels = __getLables(part)
            print(media.attrib["id"])
            mediaLabels[media.attrib["id"]] = len(labels)
    sorted_labels = sorted(mediaLabels, key=mediaLabels.__getitem__)
    for media in video:
        for part in media:
            if media.attrib["id"] == sorted_labels[0]:
                labels = __getLables(part)
                if intrusive:
                    if not labels:
                        print("deleting item " + video.attrib["key"])
                        conn.deleteItem(video.attrib["key"])
                    else:
                        print("updating item " +video.attrib["key"] + " with labels " + ', '.join(labels))
                        conn.updateItem(video.attrib["key"], labels)
                else:
                    if not labels:
                        print("deleting item " + video.attrib["key"])
                        print("i didn't do it, no worries")
                    else:
                        print("updating item " + video.attrib["key"] + " with labels " + ', '.join(labels))
                        print("i didn't do it, no worries")
            else:
                if intrusive:
                    print("deleting media " + media.attrib["id"] + video.attrib["key"])
                    conn.deleteMedia(media.attrib["id"], video.attrib["key"])
                else:
                    print("deleting media " + media.attrib["id"] + video.attrib["key"])
                    print("i didn't do it, no worries")



def __getLables(part):
    mediaFile = MediaFile(part.attrib["file"])
    labels = mediaFile.getLabels();

    return labels
