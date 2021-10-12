import os 
from pathlib import Path
from bs4 import BeautifulSoup
root = "html"
write_dir = ("./rawtxt/")
try:
    os.mkdir(Path(write_dir))
except FileExistsError:
    print(f"Dir {write_dir} exists.")
count = 0
for root, dirnames, filenames in os.walk(root):
    for filename in filenames:
        print(count)
        if not filename.endswith('.html'):
            continue
        print("adding", filename)
        with open(os.path.join(root, filename),encoding='utf-8') as file:
        
            soup = BeautifulSoup(file,features="html.parser")
             
            with open(Path(write_dir + filename[:-5] + ".txt"),'w') as wtxt:
                wtxt.write(''.join(soup.findAll(text=True)))
        count += 1