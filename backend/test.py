import datetime
import time

if __name__ == '__main__':
    t=time.time()

    print(time.localtime(t))
    print(time.asctime(time.localtime(t)))



    # webview.create_window('Flask example', app)
    # webview.start()
