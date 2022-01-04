# s = ""
# for i in range (0, 129):
#     s += "{\"message\": \"delete:"+str(i)+"\", \"device_id\": \"B8C9C3\"},"

# print(s)

import requests
import time
url = 'https://cscloud.credosense.com/api-esp/server-to-esp/'
myobj = {'message': 'somevalue' , 'device_id': 'B8C9C3'}
head = {'Authorization': 'Token f7e979a1d0d3abb1909a3b6b1be59d76f1c04a72'}
for i in range (0, 129):
    time.sleep(1)
    delete_value = 'delete:' + str(i)
    myobj = {'message': delete_value , 'device_id': 'B8C9C3'}
    print(myobj)
    x = requests.post(url, data = myobj, headers=head)

print(x.text)