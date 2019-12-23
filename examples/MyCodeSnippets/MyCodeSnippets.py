#copy files dropped
for url in event.mimeData().urls():
    source = url.toLocalFile()
    print(source)

    destination = os.path.dirname(os.path.abspath(__file__)) + "\\UserResources\\" + url.fileName()
    print(destination)

    copyfile(source, destination)



#random name for objects
item.name += " " + str(random.randrange(100, 999))