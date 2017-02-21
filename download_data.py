import urllib.request
import requests
import bz2

base = "http://files.pushshift.io/reddit/"
categories = ["comments/RC_", "submissions/RS_"]

for cat in categories:
    year = 2005
    month = 12

    while year*100+month < 200701:
        file_name = cat+str(year)+"-"+"0"*(2-len(str(month)))+str(month)
        url = base+file_name+".bz2"
        print(url)
        month += 1
        if month > 12:
            month = 1
            year += 1

        # Download the file from `url` and save it locally under `file_name`.json

        r = requests.get(url, stream=True)
        with open(file_name+".json", 'wb') as out_file:
            decompressor = bz2.BZ2Decompressor()
            for chunk in r.iter_content(chunk_size=100*1024):
                try:
                    if chunk:
                        out_file.write(decompressor.decompress(chunk))
                except OSError:
                    print("No file found probably, writing empty file instead.")