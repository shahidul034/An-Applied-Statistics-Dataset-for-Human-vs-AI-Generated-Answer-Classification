
# An Applied Statistics Dataset for Human vs AI-Generated Answer Classification

We have developed a dataset of 4231 question-and-answer pairs for Applied Statistics, which includes 116 questions selected by domain experts and answers provided by 100 students and 50 AI-generated responses using ChatGPT. Our dataset can be used to develop AI detectors for the Applied Statistics domain and to evaluate existing ones. Additionally, our data collection framework can be applied to other domains.

## Installation

```bash
  conda create -n asd python=3.10
  conda activate asd
  pip install flask -q
  pip install datasets -q
```
    
## Flow diagram

![alt text](https://github.com/shahidul034/An-Applied-Statistics-Dataset-for-Human-vs-AI-Generated-Answer-Classification/blob/main/flowchartV4.png)
## Acknowledgements
```
@article{SALIM2024110240,
title = {An Applied Statistics dataset for human vs AI-generated answer classification},
journal = {Data in Brief},
pages = {110240},
year = {2024},
issn = {2352-3409},
doi = {https://doi.org/10.1016/j.dib.2024.110240},
url = {https://www.sciencedirect.com/science/article/pii/S2352340924002117},
author = {Md. Shahidul Salim and Sk Imran Hossain},
keywords = {LLM, Assignment, Transformer, AI},
abstract = {Due to the increasing popularity of Large Language Models (LLMs) like ChatGPT, students from various fields now commonly rely on AI-powered text generation tools to complete their assignments. This poses a challenge for course instructors who struggle to identify the authenticity of submitted work. Several AI detection tools for differentiating human-generated text from AI-generated text exist for domains like medical and coding, and available generic tools do not perform well on domain-specific tasks. Those AI detection tools depend on LLM, and to train the LLM, an instruction dataset is needed that helps the LLM to learn the differences between patterns of human-generated text and AI-generated text. To help with the creation of a tool for Applied Statistics, we have created a dataset containing 4231 question-and-answer combinations. To create the dataset, first, we collected 116 questions covering a wide range of topics from Applied Statistics selected by domain experts. Second, we created a framework to randomly distribute and collect answers to the questions from students. Third, we collected answers to fifty assigned questions from each of the 100 students participating in the work. Fourth, we generated an equal number of AI-generated answers using ChatGPT. The prepared dataset will be useful for creating AI-detector tools for the Applied Statistics domain as well as benchmarking AI-detector tools, and the proposed data preparation framework will be useful for collecting data for other domains.}
}
```