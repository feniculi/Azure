#import httplib, urllib, base64, json, uuid, requests
import http.client, urllib.request, urllib.parse, urllib.error, base64, uuid, requests, json
subscription_face_key = '2e89fed7a55d4f5697db7f5a20c8f6f0'

class face_rec:
    def create_group_person(personGroupId, user_data=None):

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_face_key
        }

        payload = {
            'name': personGroupId,
            'userData': user_data
        }
        url = 'https://testfacerosa.cognitiveservices.azure.com/face/v1.0/persongroups/' + personGroupId
        try:
            res = requests.put(url, data=json.dumps(payload), headers=headers)
            if res.status_code == 200:
                res.status_code = 200 #istruzione inutile
            else:
                error = res.json()
                errorCode = error["error"]["code"].encode("utf8")
                errorMessage = error["error"]["message"].encode("utf8")
                print (str(errorMessage))
        except requests.exceptions.RequestException as e:
            print ("Errore group person ")

    def create_person(personGroupId, name, user_data=None):

        headers = {
        # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_face_key
        }
        #Request Body
        params = {
        # Request headers
            'personGroupId': personGroupId,
        }

        payload = {
            'name': name,
            'userData': user_data
        }
        url = 'https://testfacerosa.cognitiveservices.azure.com/face/v1.0/persongroups/' + personGroupId + '/persons'

        try:
            res = requests.post(url, params=params, data=json.dumps(payload), headers=headers)
            if res.status_code == 200:
                print(str(res.json()["personId"]))
                return res.json()["personId"]

            else:
                print("codice errore" + str(res.status_code) + "\n")
                print(res.json())
                error = res.json()
                errorCode = error["error"]["code"].encode("utf8")
                errorMessage = error["error"]["message"].encode("utf8")
                print ("errore:" + str(errorMessage))
                return None
        except requests.exceptions.RequestException as e:
            print ("Errore create person ")
            return None


    def add_face(personGroupId, person_id, target_face=None, user_data=None):

        url = "https://testfacerosa.cognitiveservices.azure.com/face/v1.0/persongroups/"
        url+= personGroupId + "/persons/" + person_id + "/persistedFaces"

        #Request Header
        headers = {
          'ocp-apim-subscription-key': subscription_face_key,
          'Content-Type': "application/octet-stream",
          'cache-control': "no-cache",
        }

        image_path = "./photo/ultima_foto.jpg"
        image_data = open(image_path, "rb").read()

        params = {
            'personGroupId': personGroupId,
            'personId': person_id,
            'userData': user_data,
            'targetFace': target_face,
        }

        try:
            res = requests.post(url, headers=headers, params=params, data=image_data)
            if res.status_code == 200:
                return res.json()["persistedFaceId"]
            else:
                print("Errore:"+str(res.status_code)+ str(res.json()))
                error = res.json()
                errorCode = error["error"]["code"].encode("utf8")
                errorMessage = error["error"]["message"].encode("utf8")
                print ("errore:" + str(errorMessage))
                return("Errore: nessun viso riconosciuto")

        except requests.exceptions.RequestException as e:
            print ("errore")

    def train(personGroupId):

       url = "https://testfacerosa.cognitiveservices.azure.com/face/v1.0/persongroups/"
       url += personGroupId
       url += "/train"

       #Request Header
       headers = {
          'ocp-apim-subscription-key': subscription_face_key,
          'Content-Type': "application/json"
       }

       #Request Body
       payload = {
           'personGroupId': personGroupId
       }

       try:
           res = requests.post(url, data=json.dumps(payload), headers=headers)
           if res.status_code == 202:
               res.status_code = 202
           else:
               print ("errore1")

       except requests.exceptions.RequestException as e:
           print ("errore")


    def detect(personGroupId):
        url = "https://testfacerosa.cognitiveservices.azure.com/face/v1.0/detect"

        image_path = "./photo/ultima_foto.jpg"
        image_data = open(image_path, "rb").read()

        headers = {
          'ocp-apim-subscription-key': subscription_face_key,
          'Content-Type': "application/octet-stream",
          'cache-control': "no-cache",
        }

        #Request Parameter
        params = {
            'returnFaceId': True,
            'returnFaceLandmarks': False,
            'returnFaceAttributes': "age,gender"
        }

        try:
            res = requests.post(url, headers=headers, params=params, data=image_data)
            if res == []:
                print("non ho rilevato una faccia1")
            else:
                if res.status_code == 200:
                    data = res.json()
                    if data == []:
                        print("non ho rilevato una faccia2")

                    else:
                        return data
                else:
                    error = res.json()

        except requests.exceptions.RequestException as e:
            print("Errore")


    def identify(personGroupId, face_ids, max_candidates_return=1, threshold=None):
        url = 'https://testfacerosa.cognitiveservices.azure.com/face/v1.0/identify'
        #Request Header
        headers = {
          'ocp-apim-subscription-key': subscription_face_key,
          'Content-Type': "application/json"
        }
        #Request Body
        payload = {
            'personGroupId': personGroupId,
            'faceIds': face_ids,
            'maxNumOfCandidatesReturned': max_candidates_return,
            'confidenceThreshold': threshold,
        }
        risposta= requests.post(url, data=json.dumps(payload), headers=headers)
        return risposta.json()

    def get_a_person(personGroupId,personId):
        url = "https://testfacerosa.cognitiveservices.azure.com/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId
        headers = {
          'ocp-apim-subscription-key': subscription_face_key,
          'Content-Type': "application/json"
        }
        nome= ((requests.get(url, headers=headers)).json()["name"])
        return nome
