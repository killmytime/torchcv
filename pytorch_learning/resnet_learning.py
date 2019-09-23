import torchvision.models as models
import torch
import torch.nn.functional as functional
from PIL import Image
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

img = Image.open("dog.jpg")
img_t = transform(img)
batch_t = torch.unsqueeze(img_t, 0)
with open('imagenet_classes.txt') as f:
    labels = [line.strip() for line in f.readlines()]
resnet = models.resnet101(pretrained=True)
resnet.eval()
out = resnet(batch_t)
# Forth, print the top 5 classes predicted by the model
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
_, indices = torch.sort(out, descending=True)
print([(labels[idx], percentage[idx].item()) for idx in indices[0][:5]])