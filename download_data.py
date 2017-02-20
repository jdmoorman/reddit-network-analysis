import urllib.request

base = "http://files.pushshift.io/reddit/"
categories = ["comments/RC_", "submissions/RS_"]

for cat in categories:
    year = 2008
    month = 7

    while year*100+month < 201502:
        file_name = cat+str(year)+"-"+"0"*(2-len(str(month)))+str(month)+".bz2"
        url = base+file_name
        month += 1
        if month > 12:
            month = 1
            year += 1


        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read() # a `bytes` object
            out_file.write(data)