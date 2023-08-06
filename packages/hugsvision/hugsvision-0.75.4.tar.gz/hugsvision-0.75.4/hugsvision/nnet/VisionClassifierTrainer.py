# -*- coding: utf-8 -*-

import os
from datetime import datetime

import torch

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support as f_score

from transformers import Trainer
from transformers.training_args import TrainingArguments
from transformers.feature_extraction_utils import FeatureExtractionMixin

from tqdm import tqdm
from PIL import Image

from hugsvision.dataio.ImageClassificationCollator import ImageClassificationCollator

class VisionClassifierTrainer:

  """
  🤗 Constructor for the image classifier trainer
  """
  def __init__(
    self,
    output_dir        :str,
    model_name        :str,
    model             :torch.nn.Module,
    feature_extractor :FeatureExtractionMixin,
    train             :torch.utils.data.Dataset,
    test              :torch.utils.data.Dataset,
    max_epochs    = 1,
    cores         = 4,
    batch_size    = 8,
    lr            = 2e-5,
    eval_metric   = "accuracy",
    fp16          = False,
    classification_report_digits = 4,
  ):

    self.model_name        = model_name
    self.train             = train
    self.test              = test
    self.output_dir        = output_dir
    self.lr                = lr
    self.batch_size        = batch_size
    self.max_epochs        = max_epochs
    self.model             = model
    self.feature_extractor = feature_extractor
    self.cores             = cores
    self.fp16              = fp16
    self.eval_metric       = eval_metric
    self.ids2labels        = self.model.config.id2label
    self.labels2ids        = self.model.config.label2id
    self.classification_report_digits = classification_report_digits

    print(self.ids2labels)
    print(self.labels2ids)

    # Processing device (CPU / GPU)
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    # Get the classifier collator
    self.collator = ImageClassificationCollator(self.feature_extractor)

    # Get the model output path
    self.output_path = self.__getOutputPath()
    self.logs_path   = self.output_path
    
    # Open the logs file
    self.__openLogs()

    """
    🏗️ Build the trainer
    """
    self.training_args = TrainingArguments(
        output_dir                  = self.output_path,
        save_total_limit            = 2,
        weight_decay                = 0.01,
        save_steps                  = 10000,
        learning_rate               = self.lr,
        per_device_train_batch_size = self.batch_size,
        per_device_eval_batch_size  = self.batch_size,
        num_train_epochs            = self.max_epochs,
        metric_for_best_model       = self.eval_metric,
        logging_dir                 = self.logs_path,
        evaluation_strategy         = "epoch",
        load_best_model_at_end      = False,
        overwrite_output_dir        = True,
        fp16=self.fp16,
    )
    
    self.trainer = Trainer(
      self.model,
      self.training_args,
      train_dataset = self.train,
      eval_dataset  = self.test,
      data_collator = self.collator,
    )
    print("Trainer builded!")

    """
    ⚙️ Train the given model on the dataset
    """
    print("Start Training!")
    self.trainer.train()
    self.trainer.save_model(self.output_path + "/trainer/")
    self.model.save_pretrained(self.output_path + "/model/")
    self.feature_extractor.save_pretrained(self.output_path + "/feature_extractor/")
    print("Model saved at: \033[93m" + self.output_path + "\033[0m")

    # Close the logs file
    self.logs_file.close()

  """
  📜 Open the logs file
  """
  def __openLogs(self):    

    # Open the logs file
    self.logs_file = open(self.logs_path + "/logs.txt", "a")

  """
  📍 Get the path of the output model
  """
  def __getOutputPath(self):

    path = os.path.join(
      self.output_dir,
      self.model_name.upper() + "/" + str(self.max_epochs) + "_" + datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    )

    # Create the full path if doesn't exist yet
    if not os.path.isdir(path):
        os.makedirs(path)

    return path

  """
  🧪 Evaluate the performances of the system of the test sub-dataset given a f1-score
  """
  def evaluate_f1_score(self):

    # Get the hypothesis and predictions
    all_target, all_preds = self.evaluate()

    cr = metrics.classification_report(
      all_target,
      all_preds,
      labels = [int(a) for a in list(self.ids2labels.keys())],
      target_names = list(self.labels2ids.keys()),
      zero_division = 0,
      digits=self.classification_report_digits,
    )
    print(cr)

    # Write logs
    self.__openLogs()
    self.logs_file.write(cr + "\n")
    self.logs_file.close()

    print("Logs saved at: \033[93m" + self.logs_path + "\033[0m")

    return all_target, all_preds

  """
  🧪 Evaluate the performances of the system of the test sub-dataset
  """
  def evaluate(self):
        
    all_preds  = []
    all_target = []

    # For each image
    for image, label in tqdm(self.test):

        # Compute
        inputs  = self.feature_extractor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)

        # Get predictions from the softmax layer
        preds = outputs.logits.softmax(1).argmax(1).tolist()
        all_preds.extend(preds)

        # Get hypothesis
        all_target.append(label)

    return all_target, all_preds

  """
  🧪 Test on a single image
  """
  def testing(self, img,expected):
    image_array = Image.open(img)
    inputs      = self.feature_extractor(images=image_array, return_tensors="pt").to(self.device)
    outputs     = self.model(**inputs)
    preds       = outputs.logits.softmax(1).argmax(1).tolist()[0]
    print(
      "Predicted class: ",
      self.ids2labels[str(preds)],
      "(", str(preds), " - ", self.ids2labels[str(expected)], ") ",
      str(preds == expected)
    )
    return preds