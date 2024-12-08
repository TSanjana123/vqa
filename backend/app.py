# print("start")
# from flask import Flask, request, jsonify
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import torch
# import io
# import traceback

# app = Flask(__name__)

# # # Load the BLIP model and processor
# # def load_model_and_processor():
# #     try:
# #         # Load the BLIP model
# #         model_path = "backend//blip_model_cap_all.pkl"
# #         model = torch.load(model_path)
# #         # model.eval()

# #         # Load the BLIP processor
# #         processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        
# #         # Ensure the model is of the correct type
# #         if not isinstance(model, BlipForConditionalGeneration):
# #             raise TypeError("Loaded model is not an instance of BlipForConditionalGeneration")
        
# #         return processor, model
# #     except Exception as e:
# #         print(f"Error loading model and processor: {e}")
# #         traceback.print_exc()
# #         raise

# # processor_loaded, model_loaded = load_model_and_processor()

# @app.route('/Ask', methods=['POST'])
# def get_caption():
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image file provided'}), 400
        
#         model_loaded = torch.load('backend//blip_model_cap_all.pkl')
#         print("model_loaded",model_loaded)
#         processor_loaded = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
#         image_file = request.files['image']

#         image = Image.open(image_file.stream).convert('RGB')
        
#         # Conditional image captioning
#         text = "a photography of"  # Example conditional text
#         print(text)
#         # inputs_conditional = processor_loaded(images=image, text=text, return_tensors="pt")
#         # output_conditional = model_loaded.generate(**inputs_conditional)
#         # caption_conditional = processor_loaded.decode(output_conditional[0], skip_special_tokens=True)
        
#         # # Unconditional image captioning
#         # inputs_unconditional = processor_loaded(images=image, return_tensors="pt")
#         # output_unconditional = model_loaded.generate(**inputs_unconditional)
#         # caption_unconditional = processor_loaded.decode(output_unconditional[0], skip_special_tokens=True)
#         # caption = caption_unconditional


#         inputs = processor_loaded(image,text,return_tensors='pt')
#         out = model_loaded.generate(**inputs)
#         caption = processor_loaded.decode(out[0],skip_special_tokens=True)
#         print(caption)
#         # return jsonify({
#         #     'conditional_caption': caption_conditional,
#         #     'unconditional_caption': caption_unconditional
#         # })
#         return jsonify({'caption': caption})
#     except Exception as e:
#         print("Exception occurred:", e)
#         traceback.print_exc()
#         return jsonify({'error': 'Internal Server Error'}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=4000)
# print("end0")





print("start")
from flask import Flask, request, jsonify  # Import Flask


from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import traceback
from flask_cors import CORS
import os
import google.generativeai as genai
print("after imports")
print("get model")
def getmodel():
    model_loaded = torch.load('backend//blip_model_cap_all.pkl')
    processor_loaded = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    return model_loaded,processor_loaded
print("before flask")
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
my_api = "AIzaSyAIwrJ_nekXtHomctw2QraDVFQmkDNeYwc"
os.environ['GOOGLE_API_KEY'] = my_api
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
print("model_loaded")
model_loaded,processor_loaded = getmodel()
print("before route")
@app.route('/Ask', methods=['POST'])
def get_caption():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        image_file = request.files['image']
        image = Image.open(image_file.stream).convert('RGB')
        
        # Image captioning
        text = "a photography of"
        inputs = processor_loaded(image, text, return_tensors='pt')
        out = model_loaded.generate(**inputs)
        caption = processor_loaded.decode(out[0], skip_special_tokens=True)
        print(caption)
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        response = vision_model.generate_content(["Explain the picture?", image])
        google_caption = response.text
        print(google_caption)
        k = google_caption + caption
        return jsonify({'caption': k})
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)



