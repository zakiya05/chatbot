import ollama 
import config


def get_response(conversation_history):
    messages = [{"role":"system", "content": config.SystemPrompt}] + conversation_history
    response = ollama.chat(model = config.Model, messages = messages)
    return response["message"]["content"]



def main():
    print(f"The model config is:{config.Model}")
    conversation_history = []
    while True:
        user_input = input("You:").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Great chatting with you! See you")
            break
        if not user_input:
            continue
        conversation_history.append({"role": "user", "content": user_input})
        try:
            reply = get_response(conversation_history)
        except Exception as e:
            print(f"Error calling local model: {e}")
            print("Check if Ollama is running? Try 'ollama serve' in another terminal.")
            conversation_history.pop()  
            continue
 
        conversation_history.append({"role": "assistant", "content": reply})
 
        print(f"Llama: {reply}\n")



if __name__ == "__main__":
     main()