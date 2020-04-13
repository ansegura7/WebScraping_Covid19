# Web Scraping - Covid19 Data
Web scraping is the (generally automatic) process of collecting semi-structured data from the web, filtering and storing it, and then using it in another process.

## Motivation
Create a web scraper bot to obtain data on confirmed cases and deaths of Covid-19, in order to analyze them.

## Run Bot
To run the web scraper bot on Windows, type the following commands (below) at the **Command Prompt** or just run the batch file **run-win.bat** (which is in the /run folder).

``` console
  cd "..\code"
  conda activate base
  python web_scraper.py
```

**Important**: previously, add Anaconda Python paths to Environment Variables.

## Anaconda installation on Linux
1. Obtaining the latest version of Anaconda from https://www.anaconda.com/distribution/

2. Download latest version
``` console
  cd /tmp
  curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
```

3. Integrity check
``` console
  sha256sum Anaconda3-2020.02-Linux-x86_64.sh
```

4. Install
``` console
  bash Anaconda3-2019.03-Linux-x86_64.sh
```

5. Activation
``` console
  source ~/.bashrc
```

## Documentation
- https://realpython.com/tutorials/web-scraping/
- https://www.digitalocean.com/community/tutorials/como-instalar-anaconda-en-ubuntu-18-04-quickstart-es
- https://github.community/t5/How-to-use-Git-and-GitHub/Programatically-download-private-repository-using-Curl/td-p/30046#
- https://papelesdeinteligencia.com/herramientas-de-web-scraping/
- https://www.quora.com/Why-can-t-I-run-Python-in-CMD-but-can-in-Anaconda-Prompt

## Contributing and Feedback
Any kind of feedback/criticism would be greatly appreciated (algorithm design, documentation, improvement ideas, spelling mistakes, etc...).

## Author
- Created by Andrés Segura Tinoco
- Created on Apr 10, 2020

## License
This project is licensed under the terms of the MIT license.
