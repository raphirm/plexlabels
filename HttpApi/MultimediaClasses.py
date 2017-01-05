__author__ = 'raphi'
import xml.etree.ElementTree as ET
from MediaInfo.MediaInfo import MediaFile
import time
from HttpApi.HttpApi import HttpConn
import operator
import re


class Video:
    def __init__(self, video, conn):
        if "ratingKey" in video[0].attrib:
            self.video = video
            self.videoID = video[0].attrib['key']
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
    def deleteUnnessessaryContent(self):
        #If no English or German is under the supported languages (and Unknown, because w don't know) Delete the item directly!, f* french people!
        acceptedLanuages = ["eng.stereo.Audio", "ger.stereo.Audio", "ger.surround.Audio", "eng.surround.Audio", "eng.Subtitle", "ger.Subtitle", "Unknown.Audio"]
        if set(self.getLabels()).isdisjoint(acceptedLanuages):
            self.conn.deleteItem(self.videoID)
            print("delete-item "+self.videoID+"now...?")
        if len(self.media) >1:
            missinglabels = self.getLabels()
            candidates = list(self.media)
            keepers = []
            while len(missinglabels) > 0:

               # print("duplicates, need to analyse duplicates")
                highscore = 0
                winner = ''
                for m in candidates:
                    score = m.getRating()
                    if score > highscore:
                        highscore = score
                        winner = m

                missinglabelsafter =[ item for item in missinglabels if item not in winner.labels]

                if len(missinglabels) == len(missinglabelsafter):
                    candidates.remove(winner)
                else:
                    keepers.append(winner)
                    candidates.remove(winner)
                    missinglabels = missinglabelsafter
                    if len(missinglabels) > 0:
                        print("not all labels are OK, missing: " + str(missinglabelsafter))
            tobedeleted = [ item for item in self.media if item not in keepers]
            for element in tobedeleted:
                print (str(element)+" will get deleted")
                self.conn.deleteMedia(element.id, self.videoID)


class Media:
    def __init__(self, media, conn):
        if 'id' in media.attrib:
            mid = media.attrib['id']
            self.id = mid
            self.midAudio = []
            if 'videoResolution' in media.attrib:
                try:
                    self.resolution = int(media.attrib["videoResolution"])
                except ValueError:
                    self.resolution = 0
            else:
                self.resolution = 0
            for element in media.findall("./Part/*[@streamType='2']"):
                if 'language' in element.attrib:
                    if int(element.attrib["channels"]) > 4:
                        self.midAudio.append(element.attrib["languageCode"]+".surround")
                    else:
                        self.midAudio.append(element.attrib["languageCode"]+".stereo")

                    # print(mid + " " + element.attrib["language"])
                else:
                    self.midAudio.append("Unknown")
                    # print(mid + " " +  "Unkown")
            self.midSub = []
            for element in media.findall("./Part/*[@streamType='3']"):
                if 'language' in element.attrib:
                    self.midSub.append(element.attrib["languageCode"])
                    # print(mid + " " + element.attrib["language"])
                else:
                    self.midSub.append("Unknown")
                    # print(mid + " " + "Unkown")
            self.labels = [s + ".Subtitle" for s in self.midSub] + [s + ".Audio" for s in self.midAudio]
        else:
            print("Media has no id")
            self.id = 'not a valid Media created'

    def getRating(self):
        score = 0
        scoreslang = {
            'deu' : 1000,
            'eng'  : 100,

        }
        scoreschan = {
            'surround': 100,
            'stereo' : 10
        }
       # print (self.resolution)


        for audio in self.midAudio:
            lang = audio.split("." )
            langpoints = 1
            chanpoints = 1
            if len(lang) > 1:
                if(scoreslang.get(lang[0])):
                    langpoints = scoreslang.get(lang[0])
                if(scoreschan.get(lang[1])):
                    chanpoints = scoreschan.get(lang[1])
            points = langpoints * chanpoints
            score = score + points * 100
           # print(lang)

        for subtitle in self.midSub:
            langpoints = 1
            if(scoreslang.get(subtitle)):
                langpoints = scoreslang.get(subtitle)
            score = score + langpoints
           # print(subtitle)
        if self.resolution >= 1080:
            score = score *10
        elif self.resolution >= 720:
            score = score *5
        else:
            score =score *1
        #print(score)
        return score