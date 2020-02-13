import subprocess as sp
import os
import time
from threading import Thread

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

stream1 = os.getenv("stream_kantipur")
stream2 = os.getenv("stream_zeetv")
stream3 = os.getenv("stream_abpnews")
stream_home = os.getenv("stream_home")

pid = 0
ts_list = []


def run(stream_dir, stream_name, stream):
    cmd = """ffmpeg -y -i {0} -c:v libx264 -s:v 960x540 -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_list_size 0 -hls_time 10 -hls_allow_cache 0 -b:v 168k \
    -b:a 125k -maxrate 202k -hls_segment_filename {1}/{2}_%04d.ts -strict -2 {3}/{4}.m3u8""".format(stream, stream_dir, stream_name, stream_dir, stream_name)
    p = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
    global pid
    pid = p.pid
    p.communicate()


def remove_previous_ts():
    try:
        if pid > 0:
            while pid > 0:
                with open(stream_home+"/kantipur.m3u8", "r") as f:
                    lines = f.readlines()
                    ts_list.append(lines[-1].replace('\n',''))

                print(ts_list)
                if len(ts_list) == 3:
                    with open(stream_home+"/kantipur.m3u8", "w") as f:
                        line = f.read()
                        if line == ts_list[0]:
                            print(line)

                time.sleep(10)
        else:
            print("pid not > 0")
            time.sleep(2)
            remove_previous_ts()
    except FileNotFoundError:
        print("file not found")
        time.sleep(2)
        remove_previous_ts()


if __name__ == '__main__':
    t1 = Thread(target=run, args=[stream_home+"/kantipur", 'kantipur', stream1])
    t2 = Thread(target=run, args=[stream_home+"/zeetv", 'zeetv', stream2])
    t3 = Thread(target=run, args=[stream_home+"/abpnews", 'abpnews', stream3])
    t1.start()
    t2.start()
    t3.start()
    # t2 = Thread(target=remove_previous_ts)
    # t2.start()
