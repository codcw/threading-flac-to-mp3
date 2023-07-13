# requires ffmpeg to run, will open window thats gonna ask for base and end directory,
# converting to 320kbps mp3, preserving tags


import subprocess, pathlib, os, threading
import tkinter as tk
from tkinter.filedialog import askdirectory
tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions
# ask for directory with files to convert
base_dir = pathlib.Path(askdirectory(title = 'Pick Input(.flac) Folder'))
# ask for target directory for converted files
end_dir = pathlib.Path(askdirectory(title = 'Pick Output(.mp3) Folder'))
files = [x for x in base_dir.glob('**/*.flac') if x.is_file()]  # get list of flac files in directory
def construct_ffmpeg_query(s, e):
    return ["ffmpeg",
            "-loglevel", "error",   # logging
            "-i", base_dir / s,     # input
            "-ab", "320k",          # converting tags
            end_dir / f"{e}.mp3"]   # output


files.sort(key = lambda a: os.path.getsize(base_dir / a), reverse = True)


def convert(file):
    args = construct(file.name, file.stem)
    res = subprocess.run(args)
    with threading.Lock():
        if res:
            print(file.name, " processed")


# Function that will be run in separate threads
def worker(item):
    if item is None:
        th = threading.active_count()
        return print(f'Number of active threads: {th}')
    convert(item)

threads = []
# Start a pool of worker threads
for task in files:
    t = threading.Thread(target = worker,
                         args = (task, ),
                         daemon = True)
    t.start()
    threads.append(t)

th = threading.active_count()
print(f'Number of active threads: {th}')

# Wait for all the jobs to finish
for t in threads:
    t.join()

print(f'Files processed: {th - 1}')