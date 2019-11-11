import geffnet
import torch


if __name__ == '__main__':
    model = geffnet.efficientnet_b0(pretrained=True)
    feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
    torch.save(feature_extractor, 'efficientnet_b0_fe.pth.tar')
