import torch
import torch.nn as nn
import sys
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F
import matplotlib.pyplot as plt

class myCNN(nn.Module):
    def __init__(self):
        super(myCNN, self).__init__()
        
        self.features = nn.Sequential(
            # Convolucional 1 - [3 - 8]
            nn.Conv2d(3, 8, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Convolucional 2 - [8 - 16]
            nn.Conv2d(8, 16, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Convolucional 3 - [16 - 32]
            nn.Conv2d(16, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            # Convolucional 4 - [32 - 64]
            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
        )
        
        self.classifier = nn.Sequential(
            # Red densa 
            nn.Linear(64*6*6, 512),
            nn.ReLU(),
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 4) #capa de salida
        )

        
    def forward(self, x):
        
        x = self.features(x)      
        
        x = F.max_pool2d(x, 2)
        
        # APLANADO
        x = x.view(-1, 64*6*6)
        
        # RED DENSA
        x = self.classifier(x)
        
        return x
    
    def get_activations_gradient(self):
        return self.gradients
    
    def get_activaions(self, x):
        return self.features(x)

class BrainTumor:

    def __init__(self):
        self.model = myCNN()
        # Carga de pesos
        self.model.load_state_dict(torch.load('./BrainModel/weights.pt'))
        # Solo se necesita la transformación de test
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((128, 128), antialias=True)])
        self.classes = ['glioma', 'meningioma', 'notumor', 'pituitary']

    def classifyTumor(self,img_path):
        # Abrimos la imagen y la transformamos
        img = Image.open(img_path).convert('RGB')
        img = self.transform(img)
        
        # Realizamos la predicción
        pred = self.classes[self.model(img).argmax().item()]
        
        return pred
    
    def img2Cam(self, img_path, save_path):

        self.model.eval()

        img = Image.open(img_path).convert('RGB')
        img = self.transform(img)

        logit = self.model(img)
        pred = logit.max(-1)[-1]

        activations = self.model.features[:-1](img)

        self.model.zero_grad()
        logit[0,pred].backward()

        pool_grad = self.model.features[-2].weight.grad.data.mean((1,2,3))

        for i in range(activations.shape[0]):
            activations[i,:,:]*=pool_grad[i]

        heatmap=torch.mean(activations,dim=0).detach().cpu().numpy()
        SZ = img.shape[2]
        heatmap=255*(heatmap-heatmap.min())/(heatmap.max()-heatmap.min())
        heatmap = Image.fromarray(heatmap.astype('uint8'))
        heatmap = heatmap.resize((SZ, SZ))
        img=img.squeeze(0)[0].numpy()

        plt.figure(figsize=(30,30))
        plt.axis('off')  # Elimina los ejes
        plt.imshow(img, cmap="gray")
        plt.imshow(heatmap, cmap="jet", alpha=0.8)

        # Ajusta el tamaño de la figura al contenido
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

        plt.savefig(save_path, bbox_inches='tight', pad_inches=0, format='jpeg')
        return plt