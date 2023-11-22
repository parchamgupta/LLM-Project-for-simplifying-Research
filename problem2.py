from openai import OpenAI
import json

client = OpenAI(api_key = "")

def answer_question_with_citations(question, contexts):
    # Construct the chat history
    chat_history = [        
        {
            "role": "system",
            "content": "You are a smart assistant with information source only containing the given contexts by the user. Please provide a concise answer to the question citing relevant sources from the context. Answer should only contain points from the given context. All the relevant authors from the contexts must be cited alongside the answer in the format (Author et al) for each line. For example, Answer: 'text1 (Author1's last name et al). text2 (Author2's last name et al)'. Always mention 'et al' after the author's last name). The answer should be sort and to the point.",
        }
    ]

    # Add the provided contexts
    for context in contexts:
        chat_history.append({
            "role": "user",
            "content": f"Context: {context['text']} (Author: {context['author']})",
        })

    chat_history.append(
        {
            "role": "user",
            "content": f"Question: {question}",
        }
    )

    # Send the chat history to the Chat Completion API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Extract the answer and citations
    answer_text = response.choices[0].message.content

    return answer_text

# Example usage
question = "What is the difference between GPT and BERT models?"
contexts = [
    {
        "author": "Trinita Roy",
        "text": "BERT is an encoder transformer model which is trained on two tasks - masked LM and next sentence prediction.",
    },
    {
        "author": "Asheesh Kumar",
        "text": "GPT is a decoder model that works best on sequence generation tasks.",
    },
    {
        "author": "Siddhant Jain",
        "text": "LSTMs have been very popular for sequence-to-sequence tasks but have limitations in processing long texts.",
    },
]

answer_with_citations = answer_question_with_citations(question, contexts)
print(answer_with_citations)