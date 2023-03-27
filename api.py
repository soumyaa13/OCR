from fastapi import FastAPI
import boto3
import json

app = FastAPI()


@app.get('/get_image_data')
def ocr_implement():
    documentName = "test-images/test6.jpg"
# Amazon Textract client
    textract = boto3.client('textract')
# Call Amazon Textract
    with open(documentName, "rb") as document:
        response = textract.analyze_document(Document={'Bytes': document.read()},
                                             FeatureTypes=["FORMS"])

    # print(response)
    # Print text
    print("\nText\n========")
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' + item["Text"] + '\033[0m')
            text = text + " " + item["Text"]
    print(text.split())
    # Amazon Comprehend client
    comprehend = boto3.client('comprehend')
    # Detect sentiment
    sentiment = comprehend.detect_sentiment(LanguageCode="en", Text=text)
    print("\nSentiment\n========\n{}".format(sentiment.get('Sentiment')))
    # Detect entities

    entities = comprehend.detect_entities(LanguageCode="en", Text=text)
    print("\nEntities\n========")
    res = '{'
    for entity in entities["Entities"]:
        print("{}\t=>\t{}".format(entity["Type"], entity["Text"]))
        res = res+'"'+entity["Type"]+'":"'+entity["Text"]+'",'

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' + item["Text"] + '\033[0m')
    res = res[:-1]+'}'
    data = json.loads(res)

    return data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
