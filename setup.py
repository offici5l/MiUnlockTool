import subprocess

subprocess.run(["python3", "-m", "ensurepip"])
subprocess.run(["pip3", "install", "requests"])
subprocess.run(["pip3", "install", "pycryptodomex"])
subprocess.run(["pip", "install", "termcolor"])