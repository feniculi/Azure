import os
import uuid
import time

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import FaceAttributeType, HairColorType, TrainingStatusType, Person

SUBSCRIPTION_KEY_ENV_NAME = "856c1901bee14606a91fa5f08c321e02"
FACE_LOCATION = "westeurope"

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

def get_accessories(accessories):
    """Helper function for face_detection sample.

    This will return a string representation of a person's accessories.
    """

    accessory_str = ",".join([str(accessory) for accessory in accessories])
    return accessory_str if accessory_str else "No accessories"


def get_emotion(emotion):
    """Helper function for face_detection sample.

    This will determine and return the emotion a person is showing.
    """

    max_emotion_value = 0.0
    emotion_type = None

    for emotion_name, emotion_value in vars(emotion).items():
        if emotion_name == "additional_properties":
            continue
        if emotion_value > max_emotion_value:
            max_emotion_value = emotion_value
            emotion_type = emotion_name
    return emotion_type


def get_hair(hair):
    """Helper function for face_detection sample.

     This determines and returns the hair color detected for a face in an image.
    """

    if not hair.hair_color:
        return "invisible" if hair.invisible else "bald"
    return_color = HairColorType.unknown
    max_confidence = 0.0

    for hair_color in hair.hair_color:
        if hair_color.confidence > max_confidence:
            max_confidence = hair_color.confidence
            return_color = hair_color.color

    return return_color
def image_analysis_in_stream(subscription_key):
    """ImageAnalysisInStream.

    This will analyze an image from a stream and return all available features.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))

    faces = [jpgfile for jpgfile in os.listdir(IMAGES_FOLDER)]
    faces_ids = []

    for face in faces:
        with open(os.path.join(IMAGES_FOLDER, face), "rb") as face_fd:
            # result type: azure.cognitiveservices.vision.face.models.DetectedFace
            result = face_client.face.detect_with_stream(
                face_fd,
                # You can use enum from FaceAttributeType, or direct string
                return_face_attributes=[
                    FaceAttributeType.age,  # Could have been the string 'age'
                    'gender',
                    'headPose',
                    'smile',
                    'facialHair',
                    'glasses',
                    'emotion',
                    'hair',
                    'makeup',
                    'occlusion',
                    'accessories',
                    'blur',
                    'exposure',
                    'noise'
                ]
            )
            for face in result:
                image_file_name=(str(face_fd).split("/"))[-1]
                print("Face attributes of {}   Rectangle(Left/Top/Width/Height) : {} {} {} {}".format(
                    image_file_name,
                    face.face_rectangle.left,
                    face.face_rectangle.top,
                    face.face_rectangle.width,
                    face.face_rectangle.height)
                )
                print("Face attributes of {}   Accessories : {}".format(image_file_name, get_accessories(face.face_attributes.accessories)))
                print("Face attributes of {}   Age : {}".format(image_file_name, face.face_attributes.age))
                print("Face attributes of {}   Blur : {}".format(image_file_name, face.face_attributes.blur.blur_level))
                print("Face attributes of {}   Emotion : {}".format(image_file_name, get_emotion(face.face_attributes.emotion)))
                print("Face attributes of {}   Exposure : {}".format(image_file_name, face.face_attributes.exposure.exposure_level))
                if face.face_attributes.facial_hair.moustache + face.face_attributes.facial_hair.beard + face.face_attributes.facial_hair.sideburns > 0:
                    print("Face attributes of {}   FacialHair : Yes".format(image_file_name))
                else:
                    print("Face attributes of {}   FacialHair : No".format(image_file_name))
                print("Face attributes of {}   Gender : {}".format(image_file_name, face.face_attributes.gender))
                print("Face attributes of {}   Glasses : {}".format(image_file_name, face.face_attributes.glasses))
                print("Face attributes of {}   Hair : {}".format(image_file_name, get_hair(face.face_attributes.hair)))
                print("Face attributes of {}   HeadPose : Pitch: {}, Roll: {}, Yaw: {}".format(
                    image_file_name,
                    round(face.face_attributes.head_pose.pitch, 2),
                    round(face.face_attributes.head_pose.roll, 2),
                    round(face.face_attributes.head_pose.yaw, 2))
                )
                if face.face_attributes.makeup.eye_makeup or face.face_attributes.makeup.lip_makeup:
                    print("Face attributes of {}   Makeup : Yes".format(image_file_name))
                else:
                    print("Face attributes of {}   Makeup : No".format(image_file_name))
                print("Face attributes of {}   Noise : {}".format(image_file_name, face.face_attributes.noise.noise_level))
                print("Face attributes of {}   Occlusion : EyeOccluded: {},   ForeheadOccluded: {},   MouthOccluded: {}".format(
                    image_file_name,
                    "Yes" if face.face_attributes.occlusion.eye_occluded else "No",
                    "Yes" if face.face_attributes.occlusion.forehead_occluded else "No",
                    "Yes" if face.face_attributes.occlusion.mouth_occluded else "No")
                )

                print("Face attributes of {}   Smile : {}".format(image_file_name, face.face_attributes.smile))

        if not result:
            print("Unable to detect any face in {}".format(face))

        detected_face = result[0]
        faces_ids.append(detected_face.face_id)

        # print("\nImage {}".format(face))
        # print("Detected age: {}".format(detected_face.face_attributes.age))
        # print("Detected gender: {}".format(detected_face.face_attributes.gender))
        # print("Detected emotion: {}".format(detected_face.face_attributes.emotion.happiness))
    print("\n")

    i=0;
    for i in range(0,len(faces_ids)):
        print (i)
        for j in range(i+1,len(faces_ids)):
            # Verification example for faces of the same person.
            verify_result = face_client.face.verify_face_to_face(
                faces_ids[i],
                faces_ids[j],
            )
            if verify_result.is_identical:
                print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(faces[i], faces[j], verify_result.confidence))
            else:
                print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(faces[i], faces[j], verify_result.confidence))


def _detect_faces_helper(face_client, image_url):
    """Detect Faces Helper.

    This will detect the faces found in the image with url image_url using the provided FaceClient instance and return the faces identified in an image.
    """

    detected_faces = face_client.face.detect_with_url(url=image_url)
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(len(detected_faces), image_url))
    if not detected_faces[0]:
        raise Exception("Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")
    return detected_faces


image_analysis_in_stream(SUBSCRIPTION_KEY_ENV_NAME)
