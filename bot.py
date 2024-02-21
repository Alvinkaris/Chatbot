import json
import re


def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


response_data = load_json("response.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        
        if required_score == len(required_words):
            
            for word in split_message:
                
                if word in response["user_input"]:
                    response_score += 1

        
        score_list.append(response_score)

    
    best_response = max(score_list)

    
    if input_string == "":
        return "Please type something so we can chat :("

    #
    if best_response == 0:
        print("Bot: I don't know the answer. what do you suppose the answer might be? i would really like to learn")
        new_response = input("You: ")

        
        response_data.append({"user_input": split_message, "bot_response": new_response, "required_words": []})
        with open("response.json", "w") as json_file:
            json.dump(response_data, json_file, indent=2)
        
        return f"Bot: Thank you. I learned a new response: "

   
    response_index = score_list.index(best_response)
    return response_data[response_index]["bot_response"]

while True:
    user_input = input("You: ")
    bot_response = get_response(user_input)
    print("Bot:", bot_response)
