import azure.cognitiveservices.speech as speechsdk
import pygame

class audio:
    def riconosci_audio():
        pygame.mixer.init()
        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        speech_key, service_region = "fcf5b7ab293f41daa91b9daabb2076b3", "francecentral"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="it-IT")
        # Creates a recognizer with the given settings
        pygame.mixer.music.load("./sound/beep.mp3")
        pygame.mixer.music.play()
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        print("Sto registrando:")

        # Performs recognition. recognize_once() returns when the first utterance has been recognized,
        # so it is suitable only for single shot recognition like command or query. For long-running
        # recognition, use start_continuous_recognition() instead, or if you want to run recognition in a
        # non-blocking manner, use recognize_once_async().

        result = speech_recognizer.recognize_once()
        pygame.mixer.music.load("./sound/golf.mp3")
        pygame.mixer.music.play()
        # Checks result.
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            return(result.text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
