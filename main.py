# requires ffmpeg to run, will open window thats gonna ask for base and end directory,
# converting to 320kbps mp3, preserving tags


import subprocess, pathlib, os, threading
import tkinter as tk
from tkinter.filedialog import askdirectory
tk.Tk().withdraw()  # part of the import if you are not using other tkinter functions
# ask for directory with files to convert
base_dir = pathlib.Path(askdirectory(title = "Pick Input(.flac) Folder"))
# ask for target directory for converted files
end_dir = pathlib.Path(askdirectory(title = "Pick Output(.mp3) Folder"))
files = [x for x in base_dir.glob("**/*.flac") if x.is_file()]  # get list of flac files in directory


def construct_queries(flac_files):
    for flac_file in flac_files:
        flac = base_dir / flac_file.name
        mp3 = end_dir / f"{flac_file.stem}.mp3"
        yield (["ffmpeg",
                "-loglevel", "error",   # logging
                "-i", flac,             # input file
                "-ab", "320k",          # converting tags
                mp3], flac_file.name)   # output file


files.sort(key = lambda a: os.path.getsize(base_dir / a), reverse = True)

# worker function
def convert(ffmpeg_args, file_name):
    res = subprocess.run(ffmpeg_args, input = 'N', text = True)
    with lock:
        print("Finished: ", file_name)


threads = []
# Start a pool of worker threads
lock = threading.Lock()
print(f"Input directory:\t\"{base_dir}\"")
print(f"Output directory:\t\"{end_dir}\"")
for args in construct_queries(files):
    t = threading.Thread(target = convert,
                         args = args)
    t.start()
    threads.append(t)

# Wait for all the jobs to finish
for thread in threads:
    thread.join()

print("Total: ", len(threads))