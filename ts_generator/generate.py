import subprocess as sp
import os
import time
from threading import Thread

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

stream1 = os.getenv("stream_kantipur")
stream2 = os.getenv("stream_zeetv")
stream3 = os.getenv("stream_abpnews")
stream4 = os.getenv("stream_radio_kantipur")
stream_home = os.getenv("stream_home")

ts_list = []


def run(stream_dir, stream_name, stream):
    cmd = """ffmpeg -y -i {0} -f hls -s:v 960x540 -hls_list_size 5 -hls_time 5 -hls_flags delete_segments -hls_allow_cache 0 -b:v 168k \
    -b:a 125k -maxrate 202k -hls_segment_filename {1}/{2}_%04d.ts -strict -2 {3}/{4}.m3u8""".format(stream, stream_dir, stream_name, stream_dir, stream_name)
    p = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
    p.communicate()


if __name__ == '__main__':
    t1 = Thread(target=run, args=[stream_home+"/kantipur", 'kantipur', stream1])
    t2 = Thread(target=run, args=[stream_home+"/zeetv", 'zeetv', stream2])
    t3 = Thread(target=run, args=[stream_home+"/abpnews", 'abpnews', stream3])
    t4 = Thread(target=run, args=[stream_home+"/radio_kantipur", 'radio_kantipur', stream4])
    t1.start()
    t2.start()
    t3.start()
    t4.start()
