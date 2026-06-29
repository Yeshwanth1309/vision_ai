import os
from dotenv import load_dotenv

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv("VISION_ENDPOINT")
key = os.getenv("VISION_KEY")

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def analyze_image(image_bytes):

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE,
            VisualFeatures.READ
        ]
    )

    data = {
        "tags": [],
        "objects": [],
        "people": [],
        "text": []
    }

    if result.tags:
        for tag in result.tags.list:
            data["tags"].append({
                "name": tag.name,
                "confidence": round(tag.confidence * 100, 2)
            })

    if result.objects:
        for obj in result.objects.list:
            if obj.tags:
                data["objects"].append({
                    "name": obj.tags[0].name,
                    "confidence": round(obj.tags[0].confidence * 100, 2)
                })

    if result.people:
        for person in result.people.list:
            data["people"].append({
                "confidence": round(person.confidence * 100, 2)
            })

    if result.read:
        for block in result.read.blocks:
            for line in block.lines:
                data["text"].append(line.text)

    return data