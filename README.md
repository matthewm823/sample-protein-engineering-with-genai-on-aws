# protein-engineering-with-genai-on-aws

These notebooks demonstrate how to deploy and run generative AI models to scale protein engineering on AWS. We will demonstrate how to generate novel protein sequences using models such as Progen2, and then validate the functional and structural properties of the generated sequences using models like Amplify and ESMFold. You will learn several practical approaches to AI model deployment and explore their advantages.

## Prerequisites

- Amazon SageMaker Studio Code Editor environment. 

## Setup Instructions

1. These notebooks were designed to run with Amazon SageMaker Studio. To use Studio, you will need to setup a SageMaker Domain. For instructions on how to onboard to a Sagemaker domain, refer to this [link](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-onboard.html).
2. Make sure your SageMaker execution role has the following managed policies:

```
- arn:aws:iam::aws:policy/AWSBatchFullAccess
- arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
- arn:aws:iam::aws:policy/AmazonOmicsFullAccess
```

3. The SageMaker execution role will also need read and write access to the S3 buckets where data will be stored.

## Usage Instructions

1. On SageMaker Studio, open the Code Editor environment.
2. Clone this repository or manually import all files from this project into your workspace.
3. The notebooks files need to be executed in the following sequence given some dependencies betweeb labs: [lab1-progen-on-batch-deployment](lab1-progen-on-batch-deployment.ipynb), [lab1-progen-on-batch-inference](lab1-progen-on-batch-inference.ipynb), [lab2-amplify-on-sagemaker-deployment](lab2-amplify-on-sagemaker-deployment.ipynb), [lab2-amplify-on-sagemaker-inference](lab2-amplify-on-sagemaker-inference.ipynb), [lab3-esmfold-on-healthomics-inference](lab3-esmfold-on-healthomics-inference.ipynb).
4. Follow the instructions on each notebook to run the cells. Some of the notebooks will have a Setup section in the beginning with additional installation instructions.