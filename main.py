# requires ffmpeg to run, will open window thats gonna ask for base and end directory,
# converting to 320kbps mp3, preserving tags


import subprocess, pathlib, os, threading
import tkinter as tk
from tkinter.filedialog import askdirectory
tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions
base_dir = pathlib.Path(askdirectory())     # ask for directory with files to convert
end_dir = pathlib.Path(askdirectory())      # ask for target directory for converted files
files = [x for x in base_dir.glob('**/*.flac') if x.is_file()]  # get list of flac files in directory
construct = lambda s, e: ["ffmpeg", "-loglevel", "error", "-i", base_dir / s, "-ab", "320k", end_dir / f"{e}.mp3"]


def sortfunc(a):
    return os.path.getsize(base_dir / a)


files.sort(key=sortfunc, reverse=True)


def convert(file):
    args = construct(file.name, file.stem)
    res = subprocess.run(args)
    if res:
        print(file.name, " processed")


# Define a function that will be run in separate threads
def worker(item):
    if item is None:
        th = threading.active_count()
        return print(f'Number of active threads: {th}')
    convert(item)


threads = []
# Start a pool of worker threads
for task in files:
    t = threading.Thread(target=worker, args=(task, ))
    t.daemon = True
    t.start()
    threads.append(t)

th = threading.active_count()
print(f'Number of active threads: {th}')

# Wait for all the jobs to finish
for t in threads:
    t.join()

print(f'Files processed: {th}')
