import os

formats = ['.mp3', '.mp4', '.jpg', 'm4a', '.wav', '.jpeg', '.flac', '.mov']

path = '/Users/sergiorodrigo/Desktop/recuperado'
# path = '/Volumes/Seagate Backup Plus Drive/recuperado'
print(path)
folders = os.listdir(path)
for f in folders:
    folder = f"{path}/{f}"
    if os.path.isdir(folder):
        files = os.listdir(folder)
        if len(files) > 0:
            for fl in files:
                file_path = f"{folder}/{fl}"
                filename, file_extension = os.path.splitext(file_path)
                if file_extension not in formats:
                    command = f"sudo rm -rf {file_path}"
                    os.system(command)
                    print(f'{filename} {file_extension}<- deleted')
        else:
            command = f"sudo rm -rf {folder}"
            os.system(command)


# sudoPassword = 'randy@orton666'
# command = 'cd /Users/sergiorodrigo/Desktop/saved/recup_dir.9/ | pwd'
# # p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
# os.popen("sudo -S %s"%(command), 'w').write(sudoPassword)
# import subprocess
# list_dir = subprocess.Popen(["ls", "-l"])
# list_dir.wait()