if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
call python "C:\Users\Nadina\Documents\code\DownloadSyncer\download_syncer.py" XPS
exit