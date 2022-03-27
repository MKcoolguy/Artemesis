import subprocess    
cmd_line = "python dashboard/script.py"
p = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out = p.communicate()[0]
print(out)