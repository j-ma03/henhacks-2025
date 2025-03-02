from google import genai

client = genai.Client(api_key="AIzaSyBCGrr4M1xkbFjRuNFW3lR0y4NSAxnTy1A")
prompt = input("Enter your prompt: ")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"openstreetmap uses key-value pairs to describe objects. given a natural prompt, generate suggestions for key-value pairs that could be used to describe the object and related objects in openstreetmap. it's okay to generate key-value pairs that don't exactly match the prompt, as long as it's related. return a response in this format: key1=value1, key2=value2, key3=value3, ... . for example, if the prompt is 'a park', the response could be 'name=central park, type=park, city=new york'. do not include anything in the response that is not a key-value pair. do not include the prompt in the response. this is your prommpt: {prompt}."
)
result = response.text
result = result.replace(", ", "\n")
print(result)