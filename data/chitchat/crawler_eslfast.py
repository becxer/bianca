from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import sys

first_src_urllist = [
    'https://www.eslfast.com/easydialogs/',
    'https://www.eslfast.com/robot/'
]

def parse_srcpage(src_urllist):
    res = []
    for src_url in src_urllist:
        with urllib.request.urlopen(src_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            all_anchors = soup.find_all("a")
            for anchor in all_anchors:
                if ".htm" in anchor['href'] and not ".html" in anchor['href'] and not anchor.has_attr('target'):
                    next_url = "/".join(src_url.split("/")[:-1]) + "/" + anchor['href']
                    print(next_url)
                    res.append(next_url)
    return res


second_src_urllist = parse_srcpage(first_src_urllist)
actual_page_list = parse_srcpage(second_src_urllist)

with open("source_url.txt", "w") as fp:
    for url in actual_page_list:
        fp.write(url + "\n")

actual_page_list = open("source_url.txt").read().strip().split("\n")
for url in actual_page_list:
    print(url)
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
        raw_file_name = url.replace("/","_")
        with open("raw/"+raw_file_name, "w") as fp_raw:
            fp_raw.write(html)

from os import listdir
from os.path import isfile, join
onlyfiles = [join("raw", f) for f in listdir("raw") if isfile(join("raw", f))]
dataset_cv = []
for fname in onlyfiles:
    with open(fname) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        cv = soup.find_all('p', {'class':"MsoNormal"})
        if len(cv) == 0:
            cv_td = soup.find_all('td', {'valign':"top"})[1]
            cv_list = cv_td.getText().replace("\\t","").replace("\\'","'").replace("\\n","\n").split("Repeat")
            for cv in cv_list:
                dialog = []
                cvs = cv.split("\n")
                for c in cvs:
                    if "A:" in c or "B:" in c:
                        dialog.append(c.strip())
                if len(dialog) != 0:
                    #print ("---------------")
                    total_dialog = ""
                    for d in dialog:
                        #print(d)
                        total_dialog += d + "\n"
                    total_dialog += "\n"
                    dataset_cv.append(total_dialog)
        else:
            cv = cv[0].getText().replace("\\'","'").replace("\\n","\n").strip().split("\n")
            #print("-----------------------")
            total_dialog = ""
            for c in cv:
                #print(c)
                total_dialog += c + "\n"
            total_dialog += "\n"
            dataset_cv.append(total_dialog)

with open("dataset_cv.txt", "w") as fp:
    print(len(dataset_cv))
    total_len = 0
    for dcv in dataset_cv:
        total_len += len(dcv.strip().split("\n"))
        fp.write(dcv)
    print(total_len)
