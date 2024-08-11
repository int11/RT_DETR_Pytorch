import torch
from src.data.coco.coco_dataset import CocoDetection, CocoDetection_memory_shared
from src.data.dataloader import DataLoader, default_collate_fn
from src.data import transforms as T


def rtdetr_train_dataset(
        img_folder="./dataset/coco/train2017/",
        ann_file="./dataset/coco/annotations/instances_train2017.json"):
    
    train_dataset = CocoDetection_memory_shared(
        img_folder=img_folder,
        ann_file=ann_file,
        transforms = T.Compose([T.RandomPhotometricDistort(p=0.5), 
                                T.RandomZoomOut(fill=0), 
                                T.RandomIoUCrop(p=0.8),
                                T.SanitizeBoundingBox(min_size=1),
                                T.RandomHorizontalFlip(),
                                T.Resize(size=[640, 640]),
                                # transforms.Resize(size=639, max_size=640),
                                # # transforms.PadToSize(spatial_size=640),
                                T.ToImageTensor(),
                                T.ConvertDtype(),
                                T.SanitizeBoundingBox(min_size=1),
                                T.ConvertBox(out_fmt='cxcywh', normalize=True)]),
        return_masks=False,
        remap_mscoco_category=True)
    return train_dataset


def rtdetr_train_dataloader( 
        train_dataset=None,
        range_num=None,
        batch_size=4,
        shuffle=True, 
        num_workers=4,
        collate_fn=default_collate_fn, 
        drop_last=True,
        **kwargs):
    
    if train_dataset == None:
        train_dataset = rtdetr_train_dataset()
    
    if range_num != None:
        train_dataset = torch.utils.data.Subset(train_dataset, range(range_num))

    return DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=shuffle, 
        num_workers=num_workers, 
        collate_fn=collate_fn, 
        drop_last=drop_last, 
        **kwargs)


def rtdetr_val_dataset(
        img_folder="./dataset/coco/val2017/",
        ann_file="./dataset/coco/annotations/instances_val2017.json"):
    
    val_dataset = CocoDetection_memory_shared(
        img_folder=img_folder,
        ann_file=ann_file,
        transforms=T.Compose([T.Resize(size=[640, 640]), 
                                T.ToImageTensor(), 
                                T.ConvertDtype()]),
        return_masks=False,
        remap_mscoco_category=True)
    return val_dataset
        

def rtdetr_val_dataloader(
        val_dataset=None,
        range_num=None,
        batch_size=4,
        shuffle=True,
        num_workers=4,
        collate_fn=default_collate_fn,
        drop_last=False,
        **kwargs):
    

    if val_dataset == None:
        val_dataset = rtdetr_val_dataset()
    
    if range_num != None:
        val_dataset = torch.utils.data.Subset(val_dataset, range(range_num))

    return DataLoader(
        val_dataset, 
        batch_size=batch_size, 
        shuffle=shuffle, 
        num_workers=num_workers, 
        collate_fn=collate_fn, 
        drop_last=drop_last, 
        **kwargs)
