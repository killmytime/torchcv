import torchvision.models as models
import torch
import torch.nn.functional as functional
from PIL import Image
from torchvision import transforms

alexnet = models.alexnet(pretrained=True)
print(alexnet)

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
alexnet.eval()
out = alexnet(batch_t)
print(out.shape)
with open('imagenet_classes.txt') as f:
    labels = [line.strip() for line in f.readlines()]

# _, index = torch.max(out, 1)
percentage = functional.softmax(out, dim=1)[0] * 100
# print(labels[index[0]], percentage[index[0].item()])
_, indices = torch.sort(out, descending=True)
print([(labels[idx], percentage[idx].item()) for idx in indices[0][:5]])