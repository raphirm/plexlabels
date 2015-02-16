__author__ = 'raphi'
import os;


class MediaFile:
    def __init__(self, filename):
        self.filename = filename
        self.parseInfos()


    def parseInfos(self):
        p = os.popen('mediainfo "' + self.filename + '"', "r")
        self.videoparts=[]
        self.audioparts=[]
        self.generalsection=[]
        self.textparts=[]
        v=-1
        a=-1
        g=-1
        t=-1
        active=""
        while 1:
            line = p.readline().rstrip()
            #print(line)

            if (line == "") or (line == "General"):
                # print("found  line:" +  line)
                if line != "General":
                    line = p.readline().rstrip('\n')
                if "General" in line:
                    g = g+1
                    active = "g"
                 #   print("appending item to generalsection")
                    self.generalsection.append({})
                if "Video" in line:
                    v = v+1
                    active = "v"
                  #  print("appending item to videoparts")
                    self.videoparts.append({})
                if "Audio" in line:
                    a = a+1
                    active = "a"
                   # print("appeding item to audioparts")
                    self.audioparts.append({})
                if "Text" in line:
                    t = t+1
                    active = "t"
                   # print("appeding item to audioparts")
                    self.textparts.append({})
                elif not line: break

                continue
            lineparts = []
            if active == "":
                continue
            else:
                lineparts = line.split(":")
            if active == "g":
                #print("appenting following line to generalsection:" + line)
                self.generalsection[g][lineparts[0].rstrip()] = lineparts[1].rstrip().lstrip()
            if active == "v":
                #print("appenting following line to videoparts:" + line)
                self.videoparts[v][lineparts[0].rstrip()] = lineparts[1].rstrip().lstrip()
            if active == "a":
                #print("appenting following line to audioparts:" + line)
                self.audioparts[a][lineparts[0].rstrip()] = lineparts[1].rstrip().lstrip()
            if active == "t":
                #print("appenting following line to textparts:" + line)
                self.textparts[t][lineparts[0].rstrip()] = lineparts[1].rstrip().lstrip()








        filename = self.filename

    def getLabels(self):
        labels=[]
        for audio in self.audioparts:
            if 'Language' in audio.keys():
                language = audio["Language"]
            else:
                language = "Unknown"
            if 'Channel(s)' in audio.keys():
                channels = audio["Channel(s)"]
            else:
                channels = "1 channels"
            chans = channels.split()
            chanint= int(chans[0])
            if chanint >= 5:
                labels.append(language)
        return labels