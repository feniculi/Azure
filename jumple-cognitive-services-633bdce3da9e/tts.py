import requests
import subprocess
import os
import pygame
from xml.etree import ElementTree



class TextToSpeech(object):
    def __init__(self, subscription_key1, testo):
        self.subscription_key1 = subscription_key1
        self.tts = testo
        self.access_token = None
        self.get_token()
    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key1
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
        self.save_audio()

    def save_audio(self):
        base_url = 'https://francecentral.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', "Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)")
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)


        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('./sound/voice.wav', 'wb') as audio:
                audio.write(response.content)
                pygame.mixer.init()
                pygame.mixer.music.load("./sound/voice.wav")
                pygame.mixer.music.play()

                #print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
