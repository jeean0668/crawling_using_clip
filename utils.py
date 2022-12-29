import torch
import clip
from torch.nn import CosineSimilarity
from PIL import Image

class Similarity():
    def __init__(self):
        
        model_name = 'ViT-B/32'
        self.device = "cuda" if torch.cuda.is_available() else 'cpu'
        self.model, self.preprocess = clip.load(model_name, device = self.device)
        
    def generate_text_features(self, text):
        tokenized_text = clip.tokenize([text]).to(self.device)
        text_features = self.model.encode_text(tokenized_text)
        return text_features
    
    def generate_image_features(self, image):
        image_features = self.model.encode_image(image)
        return image_features

    def calculate_cosine_similarity(self, image_features, text_features):
       
        logits_per_image, logits_per_text = self.model(image_features, text_features)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        return probs

    def calculation(self, image_directory, text):
        
        tokenized_text = clip.tokenize([text]).to(self.device)
        image = self.preprocess(Image.open(image_directory)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            #text_features = self.generate_text_features(text)
            #image_features = self.generate_image_features(image)
            similarity = self.calculate_cosine_similarity(image, tokenized_text)
        return similarity

    
        
        
        