# s = ""
# for i in range (0, 129):
#     s += "{\"message\": \"delete:"+str(i)+"\", \"device_id\": \"B8C9C3\"},"

# print(s)

import requests
import time
url = 'https://saudafashion.credosense.cloud/api-esp/server-to-esp/'
# myobj = {'message': 'somevalue' , 'device_id': '03BD1A'}
head = {'Authorization': 'Token b5449e69849b098b3bbcd5ae00557b64dde870a1'}
for i in range (0, 129):
    time.sleep(.25)
    delete_value = 'delete:' + str(i)
    myobj = {'message': delete_value , 'device_id': '03BD1A'}
    print(myobj)
    x = requests.post(url, data = myobj, headers=head)

print(x.text)