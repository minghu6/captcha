# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.etc.path import add_parent_path
import os
import captcha_recognise_gui_controller as crgc
CLIENT_FILE = 'captcha_recognise_gui_controller.py'
def main():
    popen = None
    def start_gui(*args):

        from minghu6.etc.launchmods import PortableLauncher as launch

        launcher=launch('gui', ' '.join([CLIENT_FILE, *args]))
        launcher()

        #print('client pid ',launcher.popen.pid)
        return launcher.popen

    def start_listen_thread():
        def listen_thread():
            while True:
                nonlocal popen
                popen.terminate()
                popen = start_client()

        import threading
        threading.Thread(target=listen_thread).start()

    while True:
        if os.path.exists('.url'):
            with open('.url') as fr:
                url=fr.readline()
            print(url)
            popen = start_gui(url)
        else:
            popen = start_gui()

        popen.wait()
        #start_listen_thread()


if __name__ == '__main__':
   main()
