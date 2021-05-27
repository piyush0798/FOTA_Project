import os
import hashlib
import time
import paho.mqtt.client as mqtt
import paramiko
from past.builtins import raw_input
from datetime import datetime

broker = "49.248.39.182"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def on_log(client, userdata, level, buf):
  print("log:" + buf)


def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("connected OK")
    print("Broker connected")
  else:
    print("Bad connection Returned code=", rc)


client = mqtt.Client("Package_serv")
client.on_connect = on_connect
client.on_log = on_log
print("Connecting to the broker", broker)
client.connect(broker)
client.loop_start()
client.publish("Firmware/SOC1", "Hello Broker waiting for authentication.....")
time.sleep(2)
client.loop_stop()

username = input('Enter host username\n')
#username = "sdr"
password = input('Enter the password\n')
#password = "PIYush@123"
if username == 'sdr' and password == 'PIYush@123':
    ssh.connect(hostname='49.248.39.182', port=22, username=username, password=password)
    client.publish("Firmware/SOC1", "Authenticaion successfull!!")
else:
  print('Wrong credentials,access denied')

# localfile = raw_input("Enter the path of your file: ")
timestamp = datetime.now()
localfile = 'C:\\Users\\piyus\\OneDrive\\Desktop\\FOTA\\firmware2.py'.format(timestamp.strftime("%d/%m/%Y, %H:%M:%S"))
# assert os.path.exists(localfile), "No file found at this location :, " + str(localfile)
# remotefile = raw_input("Enter the destination path of your file: ")
# assert os.path.exists(remotefile), "No file found at this location :, " + str(remotefile)
# f = open(remotefile,'r+')
remotefile = "/home/sdr/Desktop/FOTA/firmware2.py".format(timestamp.strftime("%d/%m/%Y, %H:%M:%S"))


# get hashes
def sha1(filename):
  BUF_SIZE = 65536  # read stuff in 64kb chunks!
  sha1 = hashlib.sha1()
  with open(filename, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      sha1.update(data)
  return sha1.hexdigest()

sftp_client = ssh.open_sftp()
existing_file="C:\\Users\\piyus\\OneDrive\\Desktop\\FOTA\\existing.py"
remote_existing_file = '/home/sdr/Desktop/FOTA/firmware1.py'
sftp_client.get(remote_existing_file, existing_file)


filename = existing_file
old_hash = sha1(filename)
filename = localfile
new_hash = sha1(filename)

client.publish("Firmware/SOC1", "Checking for updates......")
client.publish("Firmware/SOC1",".....")
time.sleep(2)
client.publish("Firmware/SOC1",".....")
time.sleep(2)
client.publish("Firmware/SOC1",".....")
time.sleep(2)
client.publish("Firmware/SOC1",".....")
time.sleep(2)
if new_hash != old_hash:
  print('Found update')
  client.publish("Firmware/SOC1", "New firmware available")
else:
  print('No update')
  client.publish("Firmware/SOC1", "No updates found")
  os.remove(localfile)

# localpath = "C:\\Users\\piyus\\OneDrive\\Desktop\\FOTA Project\\firmware1.py"
# filepath = "/home/sdr/Desktop/FOTA/firmware2"



sftp_client.put(localfile, remotefile)
client.publish("Firmware/SOC1", "File transfer successfull!")

print('Well Done!! .. File transfer successfull')
sftp_client.close()
ssh.close()
