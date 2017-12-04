import os
for filename in os.listdir("."):
    if filename.startswith("th"):
        os.rename(filename, filename+'.jpg')