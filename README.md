# LLM-Projects
Problem 1: Research Assistant

In this problem, you are expected to build a GPT Assistant that reads PDF and does below
actions. You have to use the new assistants API released by Open AI:
https://platform.openai.com/docs/assistants/overview
You have to follow below steps:
1. Create an assistant using the API that reads research papers
2. Upload a research paper pdf file to your assistant
3. Ask Assistant to get the abstract of the paper
4. Print the Assistant’s response in the console
5. Ask assistant to paraphrase the abstract based on below user input:
a. Tone (Academic / Creative / Aggressive)
b. Output length (1x i.e. same length / 2x i.e. twice the length / 3x i.e. thrice the
length)
c. Please ask user input for above fields of tone and output length
6. Print the final paraphrased output in console
The output should not be a text paragraph. It needs to be a list of sentences in JSON format
that should be easily processed by using below code.
import json
json.loads(gpt_output)

Problem 2: Answer with citation

Researchers like answers that also give citations or original sources with them. It makes it
easier to trust and verify the answer using the cited source. We want ChatGPT to do the same
for our use case. Use the chat completion API:
https://platform.openai.com/docs/api-reference/chat/create
In the research use-case, the citations are research papers which are usually represented in the
format of Author, et al. For a given question we will be giving context from multiple research
papers. ChatGPT should answer the question using only those contexts and give citations
based on the context used in the answer for every line.
As input, give ChatGPT the question as well as the contexts.
Bonus marks if you submit a zero-shot prompt.
You can use the below example to test your prompt. Your prompt should work for any question
and context.
Example scenario:
Question: What is the difference between GPT and BERT models?
Context 1 author: Trinita Roy
Context 1 text: BERT is an encoder transformer model which is trained on two tasks - masked
LM and next sentence prediction.
Context 2 author: Asheesh Kumar
Context 2 text: GPT is a decoder model that works best on sequence generation tasks.
Context 3 author: Siddhant Jain
Context 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have
limitations in processing long texts.
Sample Answer: While GPT is a decoder model (Kumar et al.), BERT is an encoder transformer
model (Roy et al.). Based on their training tasks, GPT is more suitable for sequence generation
(Roy et al). BERT is more suited for next-sentence prediction (Kumar et al.).
