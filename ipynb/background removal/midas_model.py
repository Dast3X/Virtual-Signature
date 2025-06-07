import cv2
import torch
import matplotlib.pyplot as plt
from enum import Enum
import os
import numpy as np


class ModelType(Enum):
    DPT_LARGE = 'DPT_Large'
    DPT_HYBRID = 'DPT_Hybrid'
    MIDAS_SMALL = 'MiDaS_small'


class Midas():
    def __init__(self, model_type: ModelType = ModelType.DPT_LARGE, use_cuda: bool = True):
        self.midas = torch.hub.load("isl-org/MiDaS", model_type.value)
        self.model_type = model_type
        if use_cuda:
            self.use_cuda()
        self.transform()

    def use_cuda(self):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.midas.to(self.device)
        print(f"Using {self.device}")
        self.midas.eval()

    def use_cpu(self):
        self.device = torch.device("cpu")
        self.midas.to(self.device)
        print(f"Using {self.device}")
        self.midas.eval()

    def transform(self):
        print("Transforming image")
        midas_transforms = torch.hub.load("isl-org/MiDaS", "transforms")
        self.transform = midas_transforms.dpt_transform if self.model_type in [ModelType.DPT_LARGE,
                                                                               ModelType.DPT_HYBRID] else midas_transforms.small_transform

    def predict(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_batch = self.transform(img).to(self.device)
        with torch.no_grad():
            prediction = self.midas(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        return prediction.cpu().numpy()

    def depth_colormap(self, frame):
        depth_map = self.predict(frame)
        depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_INFERNO)
        return depth_map

    def mask_nearest_object(self, frame, depth_threshold=300):
        depth_map = self.predict(frame)
        mask = depth_map < depth_threshold
        return mask
