__author__ = 'raphi'
import xml.etree.ElementTree as ET
from MediaInfo.MediaInfo import MediaFile
import time
from HttpApi.HttpApi import HttpConn
import operator


class Video:
    def __init__(self, video, conn):
        if "ratingKey" in video[0].attrib:
            self.videoID = video[0].attrib['ratingKey']
            self.conn = conn
            self.media = []
            for m in video.findall("./Video/Media"):
                self.media.append(Media(m, conn))
        else:
            self.videoID = 'not a valid Video created'
    def getLabels(self):
        labels = []
        sub = []
        audio = []
        for m in self.media:
            sub = list(set(sub)| set(m.midSub))
            audio = list(set(audio) | set(m.midAudio))
        sub = [s + ".Subtitle" for s in sub]
        audio = [s + ".Audio" for s in audio]

        labels = list(set(sub)|set(audio))
        return labels
class Media:
    def __init__(self, media, conn):
        if 'id' in media.attrib:
            mid = media.attrib['id']
            self.id = mid
            self.midAudio = []
            for element in media.findall("./Part/*[@streamType='2']"):
                if 'language' in element.attrib:
                    self.midAudio.append(element.attrib["language"])
                    # print(mid + " " + element.attrib["language"])
                else:
                    self.midAudio.append("Unknown")
                    # print(mid + " " +  "Unkown")
            self.midSub = []
            for element in media.findall("./Part/*[@streamType='3']"):
                if 'language' in element.attrib:
                    self.midSub.append(element.attrib["language"])
                    # print(mid + " " + element.attrib["language"])
                else:
                    self.midSub.append("Unknown")
                    # print(mid + " " + "Unkown")

        else:
            print("Media has no id")
            self.id = 'not a valid Media created'
