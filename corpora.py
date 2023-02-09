import subprocess
cmd = ['python==3.9', '-m', 'textblob.download_corpora']
subprocess.run(cmd)
print("corpora downloaded successfully")
