# Download Google Image search results with free proxies

```python
pip install gimagedownload 
```

## First step

## Create a proxy pkl file using [freeproxydownloader]([freeproxydownloader · PyPI](https://pypi.org/project/freeproxydownloader/))

##### If you have already installed  [site2hdd]([site2hdd · PyPI](https://pypi.org/project/site2hdd/))   (before 2023-01-24  , you need to update it)

### pip install --upgrade site2hdd

##### or

### pip install --upgrade gimagedownload

```python
from site2hdd import download_url_list,get_proxies,download_webpage

xlsxfile,pklfile = get_proxies(
  save_path_proxies_all_filtered='c:\\newfilepath\\myproxiefile\\proxy', #  path doesn't have to exist, it will be created, last 
 # part (proxy) is the name of the file - pkl and xlsx will be added
 # important: There will be 2 files, in this case: c:\\newfilepath\\myproxiefile\\proxy.pkl and c:\\newfilepath\\myproxiefile\\proxy.xlsx

  http_check_timeout=4, # if proxy can't connect within 4 seconds to wikipedia, it is invalid

  threads_httpcheck=50, # threads to check if the http connection is working

  threads_ping=100 ,  # before the http test, there is a ping test to check if the server exists

  silent=False, # show results when a working server has been found

  max_proxies_to_check=20000, # stops the search at 20000
)
```

## CLI

```python
#You can download the pictures using the command line:
python "C:\Users\Gamer\anaconda3\envs\dfdir\Lib\site-packages\gimagedownload\__init__.py" -p c:\newfilepath\myproxiefile\proxy.pkl -s house,elephant,lion -d f:\googleimgdownload -v 3 -t 50 -r 7 -q 9
```

```python
#Underlines are converted to space
python "C:\Users\Gamer\anaconda3\envs\dfdir\googleimgs.py" -p c:\newfilepath\myproxiefile\proxy.pkl -s brazilian_food,ferrari,Los_Angeles -d f:\googleimgdownload -v 3 -t 50 -r 7 -q 9
```

## CLI Arguments

```python
#arguments: 
-p / --proxy_pickle_file  
The proxy pkl file created with freeproxydownloader
# pip install freeproxydownloader

-s / --search 
Search terms separated by comma: house,elephant,lion


-d / --download_folder 
Download folder, will be created if it doesn't exist 
default: os.path.join(os.getcwd(), "GOOGLE_IMAGE_DOWNLOADS")

-v / --variations 
Grab links from slightly different search terms
dog/DoG/Dog/doG (only uppercase/lowercase variations) 
with different proxies. Don't exaggerate. It might get very slow, but it helps to get more results. 3 or 4 is a good start 
default = 3

-t / --threads 
How many requests threads
default = 50

-r / --requests_timeout 
Timeout in seconds for requests
default = 7

-q / --thread_timeout 
Timeout in seconds for running thread. It should be higher than the timeout for requests to avoid problems. 
default = 9
```

## Import the function

```python
from gimagedownload import start_image_download
start_image_download(
   ProxyPickleFile=r'c:\newfilepath\myproxiefilexxx\proxy.pkl', # pip install freeproxydownloader
   search_terms=['halloween'],
   download_folder=r'f:\googleimgdownload',
   search_variations=3,
   threadlimit=50,
   RequestsTimeout=7,
   ThreadTimeout=9,
)
```

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/dl.png" alt="">

### Results "brazilian_food"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/brazilian_food.png" alt="">

### Results "elephant"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/elephant.png" alt="">

### Results "ferrari"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/ferrari.png" alt="">

### Results "house"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/house.png" alt="">

### Results "lion"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/lion.png" alt="">

### Results "los_angeles"

<img title="" src="https://github.com/hansalemaos/screenshots/raw/main/gimages/los_angeles.png" alt="">
