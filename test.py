"""
这是一个测试模块是否正常工作的文件
"""
import multiprocessing
from run import run, stop
import time
process = run()
time.sleep(10)
stop(process=process)