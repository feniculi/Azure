import sys
import requests
import time
from io import BytesIO
from PIL import Image, ImageDraw

from stt import audio
from qna import qna
from tts import TextToSpeech
from photo import photo
from face import face_rec

#subscription_key Speech
subscription_key_tts="fcf5b7ab293f41daa91b9daabb2076b3"

# group that collects all the faces
personGroupId="darcu0"

# insertion: text or speech
insertion="text"
#redundancy: yes or not
redundancy="yes"

#formatting the personGroupId
format="no"
if format=="yes":
    from msrest.authentication import CognitiveServicesCredentials
    from azure.cognitiveservices.vision.face import FaceClient
    #face_base_url = "https://{}.api.cognitive.microsoft.com".format("francecentral")
    ENDPOINT="https://testfacerosa.cognitiveservices.azure.com/"
    KEY="2e89fed7a55d4f5697db7f5a20c8f6f0"
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    #face_client = FaceClient(endpoint=face_base_url, credentials=CognitiveServicesCredentials("2e89fed7a55d4f5697db7f5a20c8f6f0"))
    face_client.person_group.delete(person_group_id=personGroupId)
    face_rec.create_group_person(personGroupId)

# get the x1,y1 and x2,y2 points of a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

# say something and if needed return something
def say(text,risp=None):
    TextToSpeech(subscription_key_tts,text)
    input("\n############### Premi invio per saltare audio ###############")
    if (risp is not None):
        if insertion=="speech":
            #input("Premi Invio, aspetta il beep e rispondi.")
            content=audio.riconosci_audio()
        else:
            content=input(text)
        print("\nHo capito:", content)
        return content

#ask a question to the qna knowledge base
def question(content):
    print ("Alla domanda: " + content + " rispondo con: ")
    result = qna.get_answers (content, 1)

    #elaborazione del testo
    stri=""
    text=str(result["answers"][0]["answer"])
    text1= text.split("(")
    stri=text1[0]
    #text2= text.split("]")
    for i in text1[1:]:
    	text2= str(i).split(")")
    	for i in text2[1:]:
    		stri=stri+i
    print (stri)
    say(stri)

if __name__ == "__main__":

    say("Vieni qua, fatti identificare!")
    print("\n########## START ##########")

    #train the group
    face_rec.train(personGroupId)

    input("\n############### Guarda la telecamera e premi invio###############")
    faceid=None

    #until a face is not recognized take a photo
    while (faceid is None):
        photo.take_photo()
        faceid=[]
        faceid=face_rec.detect(personGroupId)
        time.sleep(2)

    #for each face detected
    for single in faceid:
        singleface_id=[0] # da modificare
        singleface_id[0]= single["faceId"]

        #rectangle points
        rect=str(single["faceRectangle"]["left"])+","+str(single["faceRectangle"]["top"])+","+str(single["faceRectangle"]["width"])+","+str(single["faceRectangle"]["height"])

        #For each face returned use the face rectangle and draw a red box.
        image_path = "./photo/ultima_foto.jpg"
        image_data = open(image_path, "rb").read()
        img = Image.open(BytesIO(image_data))
        draw = ImageDraw.Draw(img)
        draw.rectangle(getRectangle(single), outline='red')
        img.show()

        #face recognition
        id_rec=face_rec.identify(personGroupId, singleface_id)

        #if the face is not recognized
        if("error" in str(id_rec)):
            #ask name
            person=say("Non mi sembra di conoscerti, qual'è il tuo nome? ",1)
            #creat person profile
            id_person=face_rec.create_person(personGroupId, person)
            #add the face to the person profile
            riconosciuto=face_rec.add_face(personGroupId, id_person, str(rect))

        #if the face is recognized
        else:
            try:
                id_rec=str(id_rec[0]["candidates"][0]["personId"])
                nome=face_rec.get_a_person(personGroupId, id_rec)
                if redundancy=="yes":
                    risp=say("Sei " + nome + "?",1)
                    if (("Sì" in risp) | ("si" in risp)):
                        face_rec.add_face(personGroupId, id_rec,str(rect))
                        risp=say("Che bello! Prova a farmi una domanda su trenitalia?",1)
                        question(risp)
                    else:
                        #ask name
                        person=say("E allora come ti chiami?",1)
                        #creat person profile
                        id_person=face_rec.create_person(personGroupId, person)
                        #print("Aggiungo viso a:" + person)
                        face_rec.add_face(personGroupId, id_person,str(rect))
                else:
                    risp=say("Ciao " + nome)
                    risp=say("Che bello rivederti! Prova a farmi una domanda su trenitalia?",1)
                    question(risp)
            except:
                #ask name
                person=say("Non mi sembra di conoscerti, qual'è il tuo nome? ",1)
                #creat person profile
                id_person=face_rec.create_person(personGroupId, person)
                #add the face to the person profile
                riconosciuto=face_rec.add_face(personGroupId, id_person,str(rect))
