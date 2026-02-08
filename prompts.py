import json
import re


def make_direct_output_prompt(s):
    code, test = s
    return f"""You are given a Python function ,an input to the function and an assertion containing this input. 
    Complete the assertion with a literal (no unsimplified expressions, no function calls) containing the output when 
    executing the provided code on the given input, even if the function is incorrect or incomplete. 
    Do NOT output any extra information. 
    Provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts

text = "This is a sample text. This text contains sample words."
assert f(text)['this'] == ?? 

[/PYTHON]
[ANSWER]
assert f(text)['this'] == 2 
[/ANSWER]

[PYTHON]
import pandas as pd 
import regex as re 
import seaborn as sns 

COLUMN_NAMES = ["Name", "Email", "Age", "Country"] 

def f(text):
    pattern = r"Name: (.*?), Email: (.*?), Age: (.*?), Country: (.*?)($|\n)" 
    matches = re.findall(pattern, text) 
    data = [] 
    for match in matches: 
        data.append(match[:-1]) 
    df = pd.DataFrame(data, columns=COLUMN_NAMES) 
    df["Age"] = df["Age"].astype(int)  
    return df.loc[0, 'Name']

text = "Name: John Doe, Email: john.doe@example.com, Age: 30, Country: USA\nName: Jane Doe, Email: jane.doe@example.com, Age: 25, Country: UK"
assert f(text) == ??
[/PYTHON]
[ANSWER]
assert f(text) == "John Doe"
[/ANSWER]

[PYTHON]
{code}
{test}
[/PYTHON]
[ANSWER]
"""


def make_RAG_details_output_prompt(s, data):
    id, code, test = s

    for item in data:
        if item.get("ID") == id:
            matches = item.get("matches", [])
            texts = []
            for match in matches:
                query = match.get("query", "")
                for result in match.get("results", []):
                    api_path = result.get("api_path", "")
                    api_description = result.get("api_description", "")
                    api_signature = result.get("api_signature", "")
                    api_parameters = result.get("api_parameters", "")
                    api_returns = result.get("api_returns", "")
                    api_examples = result.get("api_examples", "")
                    
                    text = f"""\
Query: {query}
API Path: {api_path}
Description: {api_description}
Signature: {api_signature}
Parameters: {api_parameters}
Returns: {api_returns}
Examples: {api_examples}
"""
                    texts.append(text)
            rag_text =  "\n\n".join(texts)

    return f"""You are given a Python function ,an input to the function and an assertion containing this input. Complete the assertion with a literal (no unsimplified expressions, no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. Do NOT output any extra information. Provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts

text = "This is a sample text. This text contains sample words."
assert f(text)['this'] == ?? 

[/PYTHON]
[ANSWER]
assert f(text)['this'] == 2 
[/ANSWER]

[PYTHON]
import pandas as pd 
import regex as re 
import seaborn as sns 

COLUMN_NAMES = ["Name", "Email", "Age", "Country"] 

def f(text):
    pattern = r"Name: (.*?), Email: (.*?), Age: (.*?), Country: (.*?)($|\n)" 
    matches = re.findall(pattern, text) 
    data = [] 
    for match in matches: 
        data.append(match[:-1]) 
    df = pd.DataFrame(data, columns=COLUMN_NAMES) 
    df["Age"] = df["Age"].astype(int)  
    return df.loc[0, 'Name']

text = "Name: John Doe, Email: john.doe@example.com, Age: 30, Country: USA\nName: Jane Doe, Email: jane.doe@example.com, Age: 25, Country: UK"
assert f(text) == ??
[/PYTHON]
[ANSWER]
assert f(text) == "John Doe"
[/ANSWER]

What's more, here is some information about the APIs which are similar to the APIs in the given Python function, you can understand them to help you complete the assertion.
{rag_text}

[PYTHON]
{code}
{test}
[/PYTHON]
[ANSWER]
"""



def make_RAG_no_details_output_prompt(s, data):
    id, code, test = s

    for item in data:
        if item.get("ID") == id:
            matches = item.get("matches", [])
            texts = []
            for match in matches:
                query = match.get("query", "")
                for result in match.get("results", []):

                        api_path = result.get("api_path", "")
                        api_doc_full = result.get("api_doc", "")
                        api_name = result.get("api_name", "")
                        api_signature = result.get("api_signature", "")
                        if isinstance(api_doc_full, str) and api_doc_full.strip():
                            text_clean = api_doc_full.replace("\n", " ").replace("\r", " ")
                            sentences = re.split(r'(?<=[。！？.!?])\s*', text_clean)
                            sentences = [s.strip() for s in sentences if s.strip()]
                            api_doc = " ".join(sentences[:4])
                        else:
                            api_doc = ""

                        text = f"""\ 
    [API INFORMATION]
    API Path: {api_path}
    API Doc: {api_doc_full}
    [/API INFORMATION]
    """
                        texts.append(text)
            rag_text =  "\n\n".join(texts)


    return f"""
Here is some API information which can help you to solve the following task , each API information is between [API INFORMATION] and [/API INFORMATION] tags. No API information is possible.
{rag_text}
Here is your task. You are given a Python function ,an input to the function and an assertion containing this input. Complete the assertion with a literal (no unsimplified expressions, 
no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. Do NOT output any extra information. 
Provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts

text = "This is a sample text. This text contains sample words."
assert f(text)['this'] == ?? 

[/PYTHON]
[ANSWER]
assert f(text)['this'] == 2 
[/ANSWER]

[PYTHON]
import pandas as pd 
import regex as re 
import seaborn as sns 

COLUMN_NAMES = ["Name", "Email", "Age", "Country"] 

def f(text):
    pattern = r"Name: (.*?), Email: (.*?), Age: (.*?), Country: (.*?)($|\n)" 
    matches = re.findall(pattern, text) 
    data = [] 
    for match in matches: 
        data.append(match[:-1]) 
    df = pd.DataFrame(data, columns=COLUMN_NAMES) 
    df["Age"] = df["Age"].astype(int)  
    return df.loc[0, 'Name']

text = "Name: John Doe, Email: john.doe@example.com, Age: 30, Country: USA\nName: Jane Doe, Email: jane.doe@example.com, Age: 25, Country: UK"
assert f(text) == ??
[/PYTHON]
[ANSWER]
assert f(text) == "John Doe"
[/ANSWER]

[PYTHON]
{code}
{test}
[/PYTHON]
[ANSWER]
"""


def make_cot_output_prompt(s):
    code, test = s
    return f"""You are given a Python function and an assertion containing an input to the function. Complete the assertion with a literal (no unsimplified expressions, 
    no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. 
    Do NOT output any extra information. Execute the program step by step before arriving at an answer, and provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts

text = "This is a sample text. This text contains sample words."
assert f(text)['this'] == ?? 
[/PYTHON]
[THOUGHT]
Let's execute the code step by step:

1. A list named STOPWORDS is defined, containing common English stopwords:["a", "an", "the", "in", "is", "are"].
2. A function f is defined that takes a single argument text:"This is a sample text. This text contains sample words.".
3. Inside the function, text.lower() is executed -> "this is a sample text. this text contains sample words."
4. The regular expression r"\b\w+\b" is applied using re.findall, which matches all word tokens.The result is:['this', 'is', 'a', 'sample', 'text', 'this', 'text', 'contains', 'sample', 'words']
5. The list is filtered to remove any words in STOPWORDS.Filtered words:['this', 'sample', 'text', 'this', 'text', 'contains', 'sample', 'words']
6. A pandas.Series is created from the filtered word list, and value_counts() is called to count word frequency.
7. f(text)['this'] is 2, because the word "this" appears twice after stopword filtering.
[/THOUGHT]
[ANSWER]
assert f(text)['this'] == 2 
[/ANSWER]

[PYTHON]
{code}
{test}
[/PYTHON]
[THOUGHT]
"""


def make_cot_direct_output_prompt(s):
    code, test = s
    return f"""You are given a Python function and an assertion containing an input to the function. Complete the assertion with a literal (no unsimplified expressions, 
    no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. 
    Do NOT output any extra information. Execute the program step by step before arriving at an answer, and provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts

text = "This is a sample text. This text contains sample words."
assert f(text)['this'] == ?? 
[/PYTHON]

Let's execute the code step by step.

[ANSWER]
assert f(text)['this'] == 2 
[/ANSWER]

[PYTHON]
{code}
{test}
[/PYTHON]
Let's execute the code step by step, provide the assertion with the correct output in [ANSWER] and [/ANSWER] tags.
[ANSWER]
"""



def make_RAG_MonkBeatEval_PanNumEval_output_prompt(s, data):
    id, code, test = s
    rag_text =  "\n\n"

    for item in data:
        if item.get("ID") == id:
            matches = item.get("matches", [])
            texts = []
            for match in matches:
                query = match.get("query", "")
                for result in match.get("results", []):
                
                        api_path = result.get("api_path", "")
                        api_description = result.get("api_description", "")
                        #api_name = result.get("API_name", "")
                        api_signature = result.get("api_signature", "")
                        api_examples = result.get("api_examples", "")
                        api_source = result.get("api_source", [])  

                        # 非空检查
                        if isinstance(api_description, str) and api_description.strip():
                            api_description = api_description
                        else:
                            api_description = ""
                        # if isinstance(api_examples, str) and api_examples.strip():
                        #     api_examples = api_examples
                        # else:
                        #     api_examples = ""
                        if not isinstance(api_source, list):
                            api_source = []

                        api_source_str = "".join(api_source[:50])  # 最多保留 50 行


                        text = f"""\ 
    [API INFORMATION]
    API Path: {api_path}
    API Description: {api_description}
    API Examples: {api_examples}
    [/API INFORMATION]
    """
                        texts.append(text)
            rag_text =  "\n\n".join(texts)


    return f"""
    Here is some API information which can help you to solve the following task , each API information is between [API INFORMATION] and [/API INFORMATION] tags.
    {rag_text}
    
    Here is your task. You are given a Python function ,an input to the function and an assertion containing this input. Complete the assertion with a literal (no unsimplified expressions, no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. Do NOT output any extra information. Provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

*****example start*****
[PYTHON]
import pandas as pd 
import regex as re 

STOPWORDS = ["a", "an", "the", "in", "is", "are"] 

def f(text):
    words = re.findall(r"\b\w+\b", text.lower()) 
    words = [word for word in words if word not in STOPWORDS] 
    word_counts = pd.Series(words).value_counts().rename(None) 
    return word_counts['this']

text = "This is a sample text. This text contains sample words."
assert f(text).['this'] == <ground_truth> 

[/PYTHON]
[ANSWER]
assert f(text).['this'] == 2 
[/ANSWER]

*****example end*****

Now you need to execute the following code and complete the [ANSWER] tags, only the assert line can have "==".
[PYTHON]
{code}
{test}
[/PYTHON]
"""
