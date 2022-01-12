import os
cmd1 = 'sudo uhubctl -l 2 -a 0'
os.system (cmd1)
textlist = os.popen(cmd2).readlist()
for line in textlist:
    print (line)

