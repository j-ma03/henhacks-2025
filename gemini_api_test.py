from google import genai

class GeminiAPI:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate_suggestions(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=(
            "openstreetmap uses key-value pairs to describe objects. "
            "given a natural prompt, generate suggestions for key-value pairs "
            "that could be used to describe the object and related objects in openstreetmap. "
            "it's okay to generate key-value pairs that don't exactly match the prompt, "
            "as long as it's related. the key-values should be specific, so don't generate anything "
            "that needs to be filled in, such as 'name=Park Name', since 'Park Name' is only a filler "
            "for a specific name of a park. don't suggest any key-values pertaining to a specific location, "
            "such as 'city=New York' or 'operator=city of seattle', since the location is not specified in the prompt. "
            "return a response in this format: key1=value1, key2=value2, "
            "key3=value3, ... . for example, if the prompt is 'a park', the response could be 'name=central park, "
            "type=park, city=new york'. do not include anything in the response that is not a key-value pair. "
            f"do not include the prompt in the response. this is your prompt: {prompt}."
            )
        )
        result = response.text
        result = result.replace(", ", "\n")
        return result

if __name__ == "__main__":
    api_key = "AIzaSyBCGrr4M1xkbFjRuNFW3lR0y4NSAxnTy1A"
    gemini_api_test = GeminiAPI(api_key)
    prompt = input("Enter your prompt: ")
    result = gemini_api_test.generate_suggestions(prompt)
    print(result)