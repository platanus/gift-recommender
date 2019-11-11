import torch
from PIL import Image
from torchvision import transforms
from .s3_manager import S3

neural_net_path = 'efficientnet_b0_fe.pth.tar'


class ImageFeatureExtractor(object):
    '''
    Extracts features from image
    '''
    def __init__(self, model_path: str = neural_net_path) -> None:
        S3.ensure_file(model_path)
        self.model = torch.load(model_path)
        self.model.eval()
        print('Image model loaded!')

    def compute_vector(self, image_tensor):
        return self.model(image_tensor)[0, :, 0, 0].detach().numpy()

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
