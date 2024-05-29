from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import re,os,json
from rouge import Rouge 
from tqdm import tqdm
import nltk
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import argparse


def extract_picture_numbers(text):
    numbers = re.findall(r'Picture (\d+)', text)
    numbers = [int(num) for num in numbers]
    return numbers

def show_score(path):
    with open (path,'r',encoding='utf-8') as file:
        lines = file.readlines()
        corr_num = 0
        for line in lines:
            data =json.loads(line)
            answer = data['answer']
            response = data['response']

            flag = 1
            gt_pic = extract_picture_numbers(answer)
            response_pic = extract_picture_numbers(response)
            for i in range(len(gt_pic)):
                try:
                    if not gt_pic[i] == response_pic[i]:
                        flag =0
                except:
                    flag = 0      

            if flag:
                corr_num += 1
        print(corr_num/(len(lines)))


def main(args):
    
    # TODO Load  model 
    # model = load_your_model()
    model_path = args.model_path
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True).eval()

    with open(args.test_file_path,'r',encoding = 'utf-8') as infile,open(args.output_path,'a',encoding = 'utf-8') as outfile:
        lines = infile.readlines()
        eval_num = len(lines)

        # TODO Set propmt 
        # prompt_head = 
        prompt_head = "Please determine the correspondence between the pictures and segments based on the content provided in 'pictures' and 'segments'. Please use [Picture *] to respond, where * represents the index of the picture."
        
        for line in tqdm(lines):
            data = json.loads(line)

            context = data['context']
            query = prompt_head + context

            # TODO Use model
            # image_paths = data['image_paths']
            # response = model.generate(query)
            response, history = model.chat(tokenizer, query=query, history=None)

            outdata = data
            outdata['response'] = response
            json.dump(outdata,outfile,ensure_ascii=False)
            outfile.write('\n')

    show_score(args.output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_file_path", type=str, required=True)
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="./results_final.json")
    args = parser.parse_args()
    print(args)
    main(args)


