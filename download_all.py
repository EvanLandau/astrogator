#Downloads all body files from the files specified in /data/object_files
import downloader
import os

def download_all(time):
    bodies = [] #List of bodies- what is returned (this will be quite large)
    manifest = open(os.path.join('data', 'object_files'), 'r') #Most of the code here is just to get a relative filepath
    to_read = manifest.read().split() #Gets list of files to read from
    manifest.close()
    for filename in to_read: #Open each file
        body_file = open(os.path.join('data', filename), 'r')
        for line in body_file:
            line = line.split()
            #print("Downloading " + line[0]) #Debug print statment for each body downloaded
            bodies.append(downloader.download_Body(line[0], line[1], time=time,mass=line[2]))