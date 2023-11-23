import platform
import os

def long_beep(duration_seconds):
    system_platform = platform.system()

    if system_platform == 'Windows':
        import winsound
        frequency = 2500 
        duration = int(duration_seconds * 1000) 
        winsound.Beep(frequency, duration)
    elif system_platform == 'Linux' or system_platform == 'Darwin':
        os.system(f"echo -n '\a'; sleep {duration_seconds}")
    else:
        print("Unsupported operating system")

