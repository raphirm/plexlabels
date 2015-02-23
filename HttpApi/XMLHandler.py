__author__ = 'raphi'
import xml.etree.ElementTree as ET
from MediaInfo.MediaInfo import MediaFile
import time
from HttpApi.HttpApi import HttpConn
import operator


def parseXML(xmlfile, conn, intrusive, interval):
    root = ET.fromstring(xmlfile)
    for video in root:
        medias = list(video.iter("Media"))
        validity = 0
        if interval != 0:
            validity = float(video.attrib["addedAt"]) + interval * 1.5 - time.time()
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
                            labels.append("movie")
                            conn.updateItem(video.attrib["key"], labels)
                            print("updating item " + video.attrib["key"] + " with labels " + ', '.join(labels))
                    else:
                        if not labels:
                            print("deleting item " + video.attrib["key"])
                            print("i didn't do it, no worries")
                        else:
                            labels.append("movie")
                            print("updating item " + video.attrib["key"] + " with labels " + ', '.join(labels))
                            print("i didn't do it, no worries")


def __solveDuplicates(video, conn, intrusive):
    mediaLabels = {}
    mediaLabelss = {}
    for media in video:
        for part in media:
            labels = __getLables(part)
            print(media.attrib["id"])
            mediaLabels[media.attrib["id"]] = len(labels)
            mediaLabelss[media.attrib["id"]] = labels
    sorted_labels = sorted(mediaLabels, key=mediaLabels.__getitem__)
    print(mediaLabelss);
    labelsToMovie = {}
    selectedMovies = []
    for key in mediaLabelss:
           for lang in mediaLabelss[key]:
              movieArray = []
              if lang in labelsToMovie: 
               movieArray=labelsToMovie[lang]
              movieArray.append(key)
              labelsToMovie[lang] = movieArray 
    print(labelsToMovie)
    for lang in labelsToMovie:
        if len(labelsToMovie[lang]) == 1:
         selectedMovies.append(labelsToMovie[lang][0])
    for lang in labelsToMovie:
        if len(labelsToMovie[lang]) != 1:
         if set(selectedMovies) & set(labelsToMovie[lang]): 
          print("Already exclusive, cool, discard")
         else:
          print("Add first to selectedMovies")
          selectedMovies.append(labelsToMovie[lang][0])
         print("Whats up?:" + ", ".join(labelsToMovie[lang]) + " and " + ", ".join(selectedMovies))
    print(selectedMovies)
    for media in video:
        for part in media:
            if media.attrib["id"] in selectedMovies:
                labels = __getLables(part)
                if intrusive:
                    if not labels:
                        print("deleting item " + video.attrib["key"])
                        conn.deleteItem(video.attrib["key"])
                    else:
                        print("updating item " +video.attrib["key"] + " with labels " + ', '.join(labels))
                        labels.append("movie")
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
