import torch
from PIL import Image
from torchvision import transforms
from .s3_manager import S3
from .image_autoencoder_model import VAE

feature_extractor_neural_net_path = 'efficientnet_b0_fe.pth.tar'
autoencoder_neural_net_path = 'img_feature_autoencoder.pth.tar'


class ImageFeatureExtractor(object):
    '''
    Extracts features from image
    '''
    def __init__(self) -> None:
        S3.ensure_file(feature_extractor_neural_net_path)
        S3.ensure_file(autoencoder_neural_net_path)
        self.fe_model = torch.load(feature_extractor_neural_net_path)
        self.fe_model.eval()
        self.encoder: VAE = torch.load(autoencoder_neural_net_path)
        self.encoder.eval()
        print('Image model loaded!')

    def compute_vector(self, image_tensor):
        raw_features = self.fe_model(image_tensor)[0, :, 0, 0]
        return self.encoder.encode(raw_features)[0].detach().numpy()

    @staticmethod
    def tensor_from_image(image) -> torch.Tensor:
        transformer = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
        return transformer(image).unsqueeze(0)


if __name__ == '__main__':
    img = Image.open('test_img.jpg')
    # img = Image.open('gnome.png')

    img = img.convert('RGB')

    img_fe = ImageFeatureExtractor()
    img = img_fe.tensor_from_image(img)
    print(img_fe.compute_vector(img))
