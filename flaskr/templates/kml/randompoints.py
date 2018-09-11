#!C:\Python36\python3.exe
# import random
# def run():
#    latitude = random.randrange(-90,90)
#    longitude = random.randrange(-180, 180)
#    kml = '''<?xml version="1.0" encoding="UTF-8"?>\n
#       <kml xmlns="http://www.opengis.net/kml/2.2">\n
#       <Placemark>\n
#       <name>Random Placemark blah blah</name>\n
#       <Point>\n
#       <coordinates>%d,%d</coordinates>\n
#       </Point>\n
#       </Placemark>\n
#       </kml>'''%(longitude, latitude)
#    f = open('flaskr/templates/kml/kml2.kml','w')
#    f.write(kml)
#    f.close()

def run(index):
    with open("flaskr/templates/kml/shapes/test"+str(index)+".kml") as f:
        with open("flaskr/templates/kml/kml2.kml", "w") as f1:
            for line in f:
                f1.write(line)
    f1.close()
    f.close()
         