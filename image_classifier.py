from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
from tqdm import tqdm
from MY_modules import json_parser, imgPath_To_List

def img_classification_model(img_dir:str="key_frames"):
    processor = ViTImageProcessor.from_pretrained('Models/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('Models/vit-base-patch16-224')

    model_prediction = []
    key_frames_list = imgPath_To_List(img_dir)
    for img in tqdm(key_frames_list,desc="Classification",unit="frames"):
        image = Image.open(img)
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        model_prediction.append(model.config.id2label[predicted_class_idx])
    json_parser(model_prediction,output_file_name="keyframes_classified")
    print("Parsed data into JSON file")