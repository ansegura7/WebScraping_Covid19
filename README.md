# Web Scraping - Covid19 Data
Web scraping is the (generally automatic) process of collecting semi-structured data from the web, filtering and storing it, and then using it in another process.

## Motivation
Create a web scraper bot to obtain data on confirmed cases and deaths of Covid-19, in order to analyze them.

## Run Bot
There are several ways to run this web scraper bot on Windows:

1. Type the following commands (below) at the **Anaconda Prompt**.

``` console
  cd "WebScraping_Covid19\code\"
  python web_scraper.py
```

2. Type the following commands (below) at the **Windows Command Prompt**. Previously, Anaconda Python paths must be added to: Environment Variables -> User Variables.

``` console
  cd "WebScraping_Covid19\code\"
  conda activate base
  python web_scraper.py
```

3. Directly run the batch file **run-win.bat** (found in the run/ folder).

### Automate Execution
In order to automate the process, a Task can be created in the **Windows Task Scheduler**, to configure the execution of the web scraper bot every x hours.

![task-sch-0-img](https://github.com/ansegura7/WebScraping_Covid19/blob/master/img/task-sch-0.PNG?raw=true)

1. Create a new **Task** in Windows Task Scheduler.

![task-sch-1-img](https://github.com/ansegura7/WebScraping_Covid19/blob/master/img/task-sch-1.PNG?raw=true)

2. Set up a **Trigger** that runs the task every day every x hours.

![task-sch-2-img](https://github.com/ansegura7/WebScraping_Covid19/blob/master/img/task-sch-2.PNG?raw=true)

3. In the **Action** tab, select the .bat file and the folder from where the Task will be executed.

![task-sch-3-img](https://github.com/ansegura7/WebScraping_Covid19/blob/master/img/task-sch-3.PNG?raw=true)

## Documentation
Below, some useful links:
- <a href="https://realpython.com/tutorials/web-scraping/" target="_blank" >Python Web Scraping Tutorials</a>
- <a href="https://papelesdeinteligencia.com/herramientas-de-web-scraping/" target="_blank" >10 Web Scraping Tools (Spanish)</a>
- <a href="https://www.quora.com/Why-can-t-I-run-Python-in-CMD-but-can-in-Anaconda-Prompt/" target="_blank" >Run Anaconda Python in CMD</a>
- <a href="https://www.thewindowsclub.com/how-to-schedule-batch-file-run-automatically-windows-7/" target="_blank" >Schedule a Batch file to run Automatically</a>

## Contributing and Feedback
Any kind of feedback/criticism would be greatly appreciated (algorithm design, documentation, improvement ideas, spelling mistakes, etc...).

## Author
- Created by Andrés Segura Tinoco
- Created on Apr 10, 2020

## License
This project is licensed under the terms of the MIT license.
