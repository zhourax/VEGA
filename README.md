# VEGA![icon](assets/lyra.png): Learning Interleaved Image-Text Comprehension in Vision-Language Large Models

We propose a novel multimodal task called Interleaved Image-Text Comprehension (IITC) to evaluate a model's ability to process Interleaved image and text inputs that include redundant and misleading information. To assess and improve model performance on the IITC task, we have created the VEGA dataset, which consists of two subsets. These subsets are used for training and evaluating both the IITC task and the ITA task, the latter being a subtask designed to support the training of the IITC task.

![](assets/intro1.png)

# Dataset Structure

- Download VEGA Datasets here.
- Unzip the VEGADataset.zip and you will get the folder.

```
.
├── IITC_4k_test.json
├── IITC_8k_test.json
├── IITC_4k_train.json
├── IITC_8k_train.json
├── ITA_3picture_test.json
├── ITA_5picture_test.json
├── ITA_3picture_C_train.json
├── ITA_5picture_C_train.json
├── ITA_3picture_E_train.json
├── ITA_5picture_E_train.json
├── ITA_3picture_F_train.json
├── ITA_5picture_F_train.json
├── test_imgs
│   ├── 1001.0025v1
│   │   └── pdferror.png
│   ├── 1001.0357v1
│   │   └── Different_Capacity_regions_2dB.png
...
├── train_imgs
│   ├── 1001.0025v1
│   │   ├── bound1.png
│   │   ├── del3.png
...
```

The data in IITC*.json follows the following format:

```json
{"id": "The paper's ID on arXiv.", 
"title": "The paper's title.", 
"caption": "The caption of correct image.",
"context": "Interleaved image-text input.",
"question": "Question about a specific image.", 
"answer": "The answer."
"image_paths": "List of image paths.",
"truth_fig_idx": "Index of the correct image in image_paths."
}
```

The data in ITA*.json follows the following format:

```json
{"id": "List of paper's ID on arXiv.", 
"image_paths": "List of image paths.", 
"context": "Interleaved image-text input.", 
"answer": "The answer."
}
```

In all the JSON "context" fields, the picture is represented as "Picture id: <img>img_path</img>\n" where "id" indicates the position of the image in the conversation, starting from 1. For example:


```json
{
"context": "...The result illustrated in Figure~6[Picture 1] shows that the proposed network extracting patches features separately performs significantly better than previous methods extracting patches feature together.\nPicture 1: <img>test_imgs/1803.06598v1/Figs/stack_LAN.png</img>\nFigure. 6 Picture 2: <img>test_imgs/1803.06598v1/Figs/SIR_VS_CR_curve.png</img>\nFigure. 7...", 
}
```

### Evaluation

```python
git clone https://github.com/zhourax/VEGA
cd VEGA
pip install nltk
pip install rouge
```

 After setting your model in eval/IITC.py and eval/ITA.py.

```python
bash eval/IITC.sh
bash eval/ITA.py
```

# Citation
