from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import re,os,json
from rouge import Rouge 
from tqdm import tqdm
import nltk
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import argparse

def bleu_score(reference,candidate):

    reference = reference.split()
    candidate = candidate.split()

    score = sentence_bleu([reference], candidate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=SmoothingFunction().method1)

    return score

def extract_picture_numbers(text):
    pattern = r'\[Picture (\d+)\]'

    numbers = re.findall(pattern, text)

    if not numbers:
        pattern = r'\[Picture(\d+)\]'
        numbers = re.findall(pattern, text)
        if not numbers:
            return [0]
        return [int(number) for number in numbers]

    return [int(number) for number in numbers]


def show_score(inpath):
    rouge = Rouge()
    with open(inpath,'r',encoding='utf-8') as inp:
        rl,pic_count,bleu = 0,0,0
        lines = inp.readlines()
        for line in lines:
            data = json.loads(line)

            response = data['response']
            pic_chose = extract_picture_numbers(response)
            truth_fig_idx = data['truth_fig_idx']
            answer = data['answer']

            if len(pic_chose) == 1 and pic_chose[0] == (int(truth_fig_idx) + 1):
                pic_count += 1

            try:
                scores = rouge.get_scores(response, answer)
                rl += scores[0]['rouge-l']['f']
                bleu += bleu_score(answer,response)
            except:
                pass

        print('ROUGE-L:',rl/len(lines))
        print('BLEU:',bleu/len(lines))
        print('Picture acc:',pic_count/len(lines))




def main(args):
    
    # TODO Load model 
    # model = load_your_model()
    model_path = args.model_path
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True).eval()

    with open(args.test_file_path,'r',encoding = 'utf-8') as infile,open(args.output_path,'a',encoding = 'utf-8') as outfile:
        lines = infile.readlines()
        eval_num = len(lines)

        # TODO Set propmt 
        # prompt_head = 
        prompt_head = "Based on the following known information, answer the user's questions concisely and professionally. If the answer is derived from an image, please indicate in the answer by referencing [Picture *], where * represents the image number. If the answer cannot be obtained from it, ignore the content of the text and respond to the user's question in Chinese. Known content: "
        
        for line in tqdm(lines):
            data = json.loads(line)

            context = data['context']
            question = data['question']
            query = prompt_head + context +  '\nQuestion:' + question

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


