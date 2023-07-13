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
def convert(args, file_name):
    res = subprocess.run(args)
    with threading.Lock():
        if res:
            converted_files_count += 1
            print("CONVERTED: ", file_name)
        else:
            failed_files.append(file_name)
            print("ERROR: ", file_name)


threads = []
failed_files = []
converted_files_count = 0
# Start a pool of worker threads
for args in construct_queries(files):
    t = threading.Thread(target = convert,
                         args = args)
    t.start()
    threads.append(t)

print(f"Input directory:\t\"{base_dir}\"")
print(f"Output directory:\t\"{end_dir}\"")
print("Number of active threads: ", threading.active_count())

# Wait for all the jobs to finish
for thread in threads:
    thread.join()

print("Files converted: ", converted_files_count)
if failed_files:
    print("Files failed: ", len(failed_files))
    for failed_file in failed_files:
        print("Failed - ", failed_file)