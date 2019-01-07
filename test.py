import atexit
from time import sleep

@atexit.register
def clean():
    print("cleanup")

while True:
    sleep(1)
    print("hey there")
    pass
