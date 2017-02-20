import urllib.request
import bz2

base = "http://files.pushshift.io/reddit/"
categories = ["submissions/RS_", "comments/RC_"]

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


        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(url) as response:
            data = response.read() # a `bytes` object
            with open(file_name, 'wb') as out_file:
                try:
                    out_file.write(bz2.decompress(data))
                except OSError:
                    print("No file found probably, writing empty file instead.")