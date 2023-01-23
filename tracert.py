import paramiko

username = 'azureuser'
password = 'Welcome2020!'
server = '13.76.28.0'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(server, 22, username, password)

stdin, stdout, stderr = ssh.exec_command('df -H')
disks = stdout.readlines()

for disk in disks:
	print(disk.rstrip("\n"))

print('\nSelect a filesystem to store the packet capture:')

stdin, stdout, stderr = ssh.exec_command('df -H --output=source')
disks = stdout.readlines()

for i, disk in enumerate(disks, start = 0):
	if 'Filesystem' in disk:
		continue
	print(i,disk.rstrip("\n"))

fileSystem = input('Input number: ')

try:
	if fileSystem == '0':
		raise Exception("Zero is not allowed")
	location = disks[int(fileSystem)].rstrip("\n")

except:
	print('Index is out of range or invalid input. Try again.')
	exit()

print("You have selected: ", location)

ethAdpt = input("Enter Ethernet Adapter: ")
cptFileSize = input("Enter Capture File Size: ")
numFilesCreate = input("Number of Files to Create: ")
port = input("Port Number to Capture [Optional]: ")
location2 = '/tmp'

print(ethAdpt, cptFileSize, numFilesCreate, port)

if not port:
	tcpdumpCMD = "sudo tcpdump -i " + ethAdpt + " -s 0 -C " + cptFileSize + " -W " + numFilesCreate + " -w " + location2 + "/" + server + "_test.pcap"
else:
	tcpdumpCMD = "sudo tcpdump -i " + ethAdpt + " -s 0 -C " + cptFileSize + " -W " + numFilesCreate + " -w " + location2 + "/" + server + "_test.pcap port " + port

print('Command to be executed: ', tcpdumpCMD)
print('Capturing packets... Exit to Stop')

stdin, stdout, stderr = ssh.exec_command(tcpdumpCMD)
print(stdout.read(), stderr.read())
