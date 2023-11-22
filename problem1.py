import base64
import sys
import json
from openai import OpenAI, AsyncOpenAI
import asyncio

client = AsyncOpenAI(api_key = "")

async def create_file(paper):
    file = await client.files.create(
        file=open(paper, "rb"),
        purpose="assistants"
    )
    print("File created and uploaded, id: ", file.id)
    return file

async def create_assistant(file):
    assistant = await client.beta.assistants.create(
        name="Research Assistant 1",
        instructions="You are a machine learning researcher. Answer questions based on the research paper. Only focus on the details and information mentioned in the paper and don not consider any information outside the context of the research paper.",
        model="gpt-3.5-turbo-1106",
        tools=[{"type": "retrieval"}],
        file_ids=[file.id]
    )
    print("Assistant created, id: ", assistant.id)
    return assistant

async def create_thread():
    thread = await client.beta.threads.create()
    print("Thread created, id: ", thread.id)
    return thread

async def create_message(thread, content):
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )
    print("User message sent!")

async def run_assistant(thread, assistant):
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    print("Assistant Running, id: ", run.id)
    return run

async def extract_run(thread, run):
    while run.status != "completed":
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print("Extracting run, status: ", run.status)
    print("Extracted run, status: ", run.status)

async def extract_result(thread):
    messages = await client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return messages

if __name__ == "__main__":
    async def main():
        paper = sys.argv[1]
        file = await create_file(paper)
        assistant = await create_assistant(file)
        thread = await create_thread()
        content1 = "Please provide the abstract of the research paper. The abstract should be concise and to the point. Only consider the context of the research paper and do not consider any information not present in it."
        message1 = await create_message(thread, content1)
        run1 = await run_assistant(thread, assistant)
        run2 = await extract_run(thread, run1)
        messages1 = await extract_result(thread)
        # print("ROLE:", messages1.data[0].role)

        for message in list(messages1.data):
            # if message['object'] == 'thread.message':
            # print(message)
            # print("ROLE:", message.role)
            if message.role == "assistant":
                print("Abstract : " + message.content[0].text.value)
                abstract = message.content[0].text.value
                break    
            else:
                continue

        tone = input("Please enter the desired tone (Academic, Creative, or Aggressive): ")
        output_length = input("Please enter the desired output length (1x, 2x, or 3x): ")
        if output_length == "1x":
            output = "SAME IN LENGTH AS"
        elif output_length == "2x":
            output = "TWO TIMES THE LENGTH OF"
        elif output_length == "3x":
            output = "THREE TIMES THE LENGTH OF"

        # content2 = f"Considr the below given abostarct of a research paper. \nAbstract: {abstract}. \nPlease paraphrase the above abstract of the research paper in a {tone} tone. The output should be generated in a more detailed and expansive manner. The output should have EXACTLY {output} the length as the original abstract present above. Maintain the same context and information but provide additional elaboration and details. The output should be concise and to the point. Only consider the context of the research paper and do not consider any information not present in it."
        content2 = f"Text: {abstract}. \nGenerate a paraphrased version of the provided textin the {tone} tone. Expand on each key point and provide additional details where possible. Aim for a final output that is approximately {output} the original text. Ensure that the paraphrased version retains the core information and meaning while offering a more detailed and comprehensive explanation."
        message2 = await create_message(thread, content2)
        run3 = await run_assistant(thread, assistant)
        run4 = await extract_run(thread, run3)
        messages2 = await extract_result(thread)
        for message in messages2.data:
            # if message['object'] == 'thread.message':
            if message.role == "assistant":
                print("Paraphrased abstract : " + message.content[0].text.value)
                paraphrased_text = message.content[0].text.value
                break 
            else:
                continue   

        # Convert paraphrased text to JSON format
        paraphrased_sentences = paraphrased_text.split(". ")
        paraphrased_json = json.dumps(paraphrased_sentences)
        print("Paraphrased JSON:", paraphrased_json)
    asyncio.run(main())