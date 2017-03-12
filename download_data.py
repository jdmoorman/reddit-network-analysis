import requests
import bz2


start_year = 2008
start_month = 1

end_year = 2008
end_month = 3

year = start_year
month = start_month

base = "http://files.pushshift.io/reddit/"
categories = ["comments/RC_", "submissions/RS_"]

while year*100+month < 100*end_year+end_month:
    for cat in categories:
        file_name = cat+str(year)+"-"+"0"*(2-len(str(month)))+str(month)
        url = base+file_name+".bz2"
        print(url)

        # Download the file from `url`, uncompress it, and save it locally under `file_name`.json

        r = requests.get(url, stream=True)
        with open(file_name+".json", 'wb') as out_file:
            decompressor = bz2.BZ2Decompressor()
            try:
                for chunk in r.iter_content(chunk_size=100*1024):
                    if chunk:
                        out_file.write(decompressor.decompress(chunk))
            except OSError:
                    print("No file found probably, writing empty file instead.")

    month += 1
    if month > 12:
        month = 1
        year += 1
