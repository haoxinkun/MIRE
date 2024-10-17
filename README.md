# MIRE
Official Baseline for Multimodal Intent Recognition for Dialogue Systems

This project provides the baseline for the Multimodal Intent Recognition for Dialogue Systems competition, specifically including model training, evaluation, and conversion to the submission format.

## How to Use

### **Installation**

This project is based on an open-source training and inference framework, and first you need to **install LLaMA Factory**. Please refer to:
https://github.com/hiyouga/LLaMA-Factory

### Training

**Step 1:** Replace configurations

- Place the downloaded training dataset file `train.json` in `LLaMA-Factory/data/mire/train.json`
- Replace the data configuration `mire_baseline/configs/data_info.json` with the original LLaMA-Factory data configuration `LLaMA-Factory/data/data_info.json`
- Place the training configuration file `mire_baseline/configs/qwen2_vl_full_sft.yaml` in `LLaMA-Factory/examples/qwen2_vl_full_sft.yaml`

**Step 2:** Train using the training configuration to perform instruction supervision fine-tuning on a single machine:

```
FORCE_TORCHRUN=1 llamafactory-cli train examples/qwen2_vl_full_sft.yaml
```

### Inference

**Step 1:** Place the inference configuration `mire_baseline/configs/predict.yaml` in `LLaMA-Factory/examples/predict.yaml`. Make sure to modify the model address, test set, inference result save address, and other parameters in `predict.yaml`.

**Step 2:** Execute the inference command using the inference configuration:

```
llamafactory-cli train examples/predict.yaml
```

### Generate Submission File

Modify the test file and inference result file addresses in `mire_baseline/convert2submit.py`, then execute:

```
python mire_baseline/convert2submit.py
```

### Calculate Accuracy (Optional)

If you have labeled test files and corresponding inference results, you can calculate the inference accuracy. Modify the test file and inference result file addresses in `mire_baseline/cal_acc.py`, then execute:

```
python mire_baseline/cal_acc.py
```

After execution, this project will print out something like:

```json
{'f1': 0.5333333333333333, 'accuracy': 0.5, 'precision': 0.6, 'recall': 0.5}
```

Here, `f1` is the final evaluation metric.

## Task Introduction

This competition dataset consists entirely of classification tasks combining text with images, including two main categories: image scene classification and multimodal dialogue intent classification.

## 1）Image Scene Classification:

The specific scenario for image scene classification is when a user sends a picture to customer service, and it is required to determine which type of e-commerce scene the image belongs to. The specific type labels and their corresponding descriptions are as follows:

| Label                                   | Description                                                   |
|-----------------------------------------|--------------------------------------------------------------|
| Product Classification Option           | Product color, specifications options                        |
| Main Image of Product                   | Main image on the product page                               |
| Screenshot of Product Details Page      | Screenshots that may appear in various sections of the product detail page |
| Exception During Ordering (Purchase Failed Popup) | Screenshot of exceptions during the ordering process (showing purchase failed popup) |
| Order Details Page                      | A page displaying complete order information                 |
| Payment Page                            | Includes payment method selection and payment success page   |
| Consumer and Customer Service Chat Page | Chat pages between the consumer and platform/customer service in apps like Taobao |
| Comment Area Screenshot Page            | Screenshots of the comment area in Taobao or other apps     |
| Logistics Page - Logistics List Page    | A page presenting more than two logistic information         |
| Logistics Page - Tracking Page          | A page showing the logistics transportation path             |
| Logistics Page - Exception Page         | A page containing logistics exception information             |
| Refund Page                             | A page that contains refund information                       |
| Return Page                             | A page that contains return information                       |
| Exchange Page                           | A page that contains exchange information                     |
| Shopping Cart Page                      | Images of the shopping cart page in Taobao                   |
| Store Page                              | Screenshot of the store's home page                          |
| Promotional Page                        | Screenshots of promotions                                    |
| Coupon Receipt Page                     | Screenshots of receiving coupons on the store's home page or promotional pages |
| Bill/Account Page                       | Includes transaction details, asset lists, coupon/red envelope lists, etc. |
| Personal Information Page               | Various pages related to user personal information            |
| Complaint Reporting Page                | Complaint or reporting pages                                  |
| Physical Photography (Including After-Sales) | Photos taken by users with a camera, including photos after-sales (damages, missing items, discrepancies with description) or other photos taken with a camera |
| External App Screenshots                | Various screenshots from non-Taobao or Cainiao apps, including Jingdong, Pinduoduo, SMS, mobile system screenshots |
| Platform Intervention Page              | Screenshots of platform customer service intervention        |
| Other Category Images                   | Other images that cannot be determined                       |

## 2）Dialogue Intent Classification

The scenario for dialogue intent classification is determining the user's intent based on the dialogue history between the user and customer service, as well as the current question from the user. The dialogue history includes at least one image sent by the user, which may aid in intent judgment. The intent labels and their corresponding descriptions are as follows:

| Label                  | Description                                               |
|------------------------|----------------------------------------------------------|
| Feedback on Poor Sealing | Buyer feedback that the product's sealing is poor and will leak |
| Is it Usable           | Buyer inquires whether the product is usable              |
| Will it Rust           | Inquiry about whether the product will rust               |
| Drainage Methods       | Inquiry regarding the drainage methods of products (applicable products: washing machines, water heaters) |
| Packaging Differences   | Inquiry about the differences in product packaging       |
| Delivery Quantity      | Inquiry about the quantity of products delivered          |
| Feedback on Symptoms After Use | Buyer feedback regarding physiological reactions after use |
| Product Material       | Inquiry about specific materials of the product and its accessories |
| Efficacy Function      | Inquiry regarding the efficacy and function of the product |
| Is it Easily Faded     | Inquiry about whether the product fades easily            |
| Applicable Season      | Inquiry about the applicable season for the product       |
| Can it Adjust Light    | Inquiry whether the light source can be adjusted                      |
| Differences in Versions and Styles | Inquiry regarding the differences between two versions/models/styles/packages, etc. (excluding differences in quantity/weight/dimensions) |
| Single Item Recommendation | Consumer inquiry for recommendations on a particular category/item, not at SKU level |
| Usage Method/Amount    | Inquiry regarding the methods/steps/sequences for using the product, including but not limited to amount, time, and usage area |
| Control Methods        | Inquiry on how to control the product, whether it can be controlled via mobile/computer |
| Product Release Date   | Inquiry regarding the release date of the product        |
| Product Specifications  | Inquiry regarding product quantity, weight, content, and capacity  |
| Signal Condition       | Inquiry about the quality of signals for mobile use, and how to handle poor signals |
| Maintenance Method     | Inquiry about maintenance methods for the product          |
| Set Recommendations    | Consumer inquiry for recommendations on certain sets      |
| When Restocking        | Inquiry regarding restocking/delivery times               |
| Bubbles                | Inquiry on how to avoid and remove bubbles when applying film |

Contestants can obtain the competition dataset from the Tianchi platform, which includes:
- 1,000 labeled dialogue samples for training
- 10,000 unlabeled samples for preliminary test
- An additional 10,000 new test samples for the semifinals

## Baseline

This project's baseline uses the qwen2-vl-7b full SFT method, with a baseline accuracy of 80.60%. The specifics are as follows:

|                  | F1        | Precision | Recall |
|------------------|-----------|-----------|--------|
| Overall          | **0.806** | 0.8256    | 0.806  |
| Image Scene Classification Task | 0.9155 | 0.9253 | 0.918  |
| Dialogue Intent Classification Task | 0.6965 | 0.7259 | 0.694  |

## Official Q&A Group

![image-20241017192205038](images/qa_group.png)