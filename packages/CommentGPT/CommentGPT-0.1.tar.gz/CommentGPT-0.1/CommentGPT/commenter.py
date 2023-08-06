from CommentGPT import chatgpt_interface_wrapper
from tqdm import tqdm

testing_mode = False

# convert a section of code to a question for ChatGPT
def snippet_to_question(snippet):
    # the question being asked to API
    prompt = "Give me this code but with comments written in. "
    # narrows down the question to avoid  "undesirable" components in the response
    # things like "This is the code: " or "This is code with comments in it."
    narrower = "Don't say something before or after the code. Don't add any backticks. Don't modify the code. Only add comments.:\n\n"
    prompt += narrower
    question = prompt + snippet
    return question


# take the whole snippet of code & divide it into an array of sections of that code
# each section is 'section_size' lines long. they are divided on that basis
def divide_into_sections(snippet, section_size):
    lines = snippet.splitlines() # split the code into a list of strings, each one line of the code
    snippet_sections = []
    # create a list of 'snippet_size' line sections of the file
    while len(lines) > 0:
        # TODO: figure out a way to split along lines without splitting along '\n' segments within the lines
        snippet_section = '\n'.join(lines[:section_size])
        lines = lines[section_size:]
        snippet_sections.append(snippet_section)
    return snippet_sections


# comment the string of code "snippet", the "section_size" configures how big each section of code sent to ChatGPT is
# returns a string of the input code, but commented
def comment_code(snippet, section_size=50):
    # get a ChatGPT interface & initialize it
    curr_gpt_tool = chatgpt_interface_wrapper.chatgpt_wrapper_interface()
    curr_gpt_tool.init()

    # break the input 'snippet' of text into a list of strings. i.e. "snippet_sections"
    snippet_sections = divide_into_sections(snippet, section_size)

    # send each section of the input text to chatGPT, requesting to comment each section
    print("Commenting the code with ChatGPT: ")
    combined_response = ""
    for snippet_section in tqdm(snippet_sections):
        # format each the section of the text into a question, requesting comments
        question = snippet_to_question(snippet_section)
        # send the question
        response = curr_gpt_tool.ask(question)
        # combine each individual commented section into a combined, commented file
        combined_response = response if combined_response == "" else combined_response + '\n' + response

    return combined_response


# verify if ChatGPT is working by asking a very simple question
def verify_connection():
    # get a ChatGPT interface & initialize it
    curr_gpt_tool = chatgpt_interface_wrapper.chatgpt_wrapper_interface()
    curr_gpt_tool.init()

    # verify if the tool is working
    is_working = curr_gpt_tool.is_working()
    if is_working:
        print("ChatGPT is working.")
    else:
        print("ChatGPT is NOT working.")
    exit()  # exit after finishing the test
