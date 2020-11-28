from os.path import splitext
from os import listdir
import numpy as np
from glob import glob
import torch
from torch.utils.data import Dataset
import logging
# from PIL import Image
import cv2
from exr2png import exr2numpy

class BasicDataset(Dataset):
    def __init__(self, imgs_dir, masks_dir, scale=1, mask_suffix=''):
        self.imgs_dir = imgs_dir
        self.masks_dir = masks_dir
        self.scale = scale
        self.mask_suffix = mask_suffix
        self.root = "data"
        assert 0 < scale <= 1, 'Scale must be between 0 and 1'

        self.ids = glob(self.root + "/*")
        logging.info(f'Creating dataset with {len(self.ids)} examples')

    def __len__(self):
        return len(self.ids)

    @classmethod
    def preprocess(cls, pil_img, scale):
        try:
            w, h = pil_img.shape
        except:
            w, h,_ = pil_img.shape
        newW, newH = int(scale * w), int(scale * h)
        assert newW > 0 and newH > 0, 'Scale is too small'
        # pil_img = pil_img.resize((newW, newH))
        pil_img = cv2.resize(pil_img, (newH, newH))
        # img_nd = np.array(pil_img)

        if len(pil_img.shape) == 2:
            pil_img = np.expand_dims(pil_img, axis=2)

        # HWC to CHW
        img_trans = pil_img.transpose((2, 0, 1))
        if img_trans.max() > 1:
            img_trans = img_trans / 255

        return img_trans

    def __getitem__(self, i):
        idx = self.ids[i]
        mask_file = [self.root + "/" + str(i) + "/Image0001.exr"]
        img_file = [self.root + "/" + str(i) + "/Camera.png"]
        # mask_file = glob(self.masks_dir + idx + self.mask_suffix + '.*')
        # img_file = glob(self.imgs_dir + idx + '.*')

        assert len(mask_file) == 1, \
            f'Either no mask or multiple masks found for the ID {idx}: {mask_file}'
        assert len(img_file) == 1, \
            f'Either no image or multiple images found for the ID {idx}: {img_file}'
        mask = exr2numpy(mask_file[0], maxvalue=25, normalize=True)
        # mask = Image.open(mask_file[0])
        img = cv2.imread(img_file[0])

        # print("Mask size ", mask.shape)
        # print("Image size ", img.shape)
        
        
        assert img.shape[:2] == mask.shape, \
            f'Image and mask {idx} should be the same size, but are {img.shape} and {mask.shape}'

        img = self.preprocess(img, self.scale)
        mask = self.preprocess(mask, self.scale)

        return {
            'image': torch.from_numpy(img).type(torch.FloatTensor),
            'mask': torch.from_numpy(mask).type(torch.FloatTensor)
        }


class CarvanaDataset(BasicDataset):
    def __init__(self, imgs_dir, masks_dir, scale=1):
        super().__init__(imgs_dir, masks_dir, scale, mask_suffix='_mask')
