# ---------------------------------------------------------------------------------------------
# Module for determining the categories of a law according to a normative with GPT
# ---------------------------------------------------------------------------------------------

# OpenAI library
from openai import OpenAI

# Determine with GPT the identified categories in a law based on the definitions of a normative
# apiKey: OpenAi's api key.
# id_normative: Identifier of the normative
# name_normative: Name of the normative
# alias_normative: Alias of the normative
# id_law: Identifier of the law
# name_law: Name of the law
# alias_law: Alias of the law
# textNormative: Text with the categories of the normative
# textLaw: Text of the law to be analyzed
# n: Total number of categories
def queryGpt(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n):
    client = OpenAI(api_key = apiKey)
    example1 = "Suppose that this is a fragment of another privacy legal framework."
    output1 = "0,1,15,17,21"
    example2 = "Suppose that this is a fragment of another privacy legal framework to analyze."
    output2 = "1,5,7,16"

    input_system = "You are an expert in privacy and must determine how well aligned is the privacy legal framework " + name_law + " with the standard " + name_normative + ". " \
    "Given the text of the privacy legal framework, you must determine whether it suggests and/or compels the compliance of each one of the " + str(n) \
    " categories of subclauses defined by the standard. The categories are coded with numbers from 0 to " + str(n-1) + ". " \
    "Just return the codes without a reason or extra text. In case of no categories selected, answer None. " \
    "The categories of subclauses and their definitions are the following:\n" + textNormative + "\n" \
    "Here, there are two examples of expected output structures from you when analyzing a fragment of another privacy legal framework:\n"
    "Example 1:\n" \
    "Text: " + example1 + "\n" \
    "Expected output structure:" + output1 + "\n" \
    "Example 2:\n" \
    "Text: " + example2 + "\n" \
    "Expected output structure:" + output2
        
    input_user =  "The following is the text of the privacy legal framework that you must analyze:\n" + textLaw

    response = client.responses.create(
        input= [
            {
                "role": "system",
                "content": input_system
            },
            {
                "role": "user",
                "content": input_user
            }
        ],
        model="gpt-5.2",
        temperature=0,
        top_p=1,
        include=["message.output_text.logprobs"]
    )

    resultGpt = response.output_text
    results = list()
    if resultGpt == "" or resultGpt.strip().lower() == "none":
        result = dict()
        result["category"] = "None"
        result["log_prob"] = 0
        results.append(result)
    else:
        for logprob in response.output[0].content[0].logprobs:
            if str(logprob.token) != "," and str(logprob.token) != " " and str(logprob.token) != ", " and str(logprob.token) != " ,":
                result = dict()
                result["category"] = int(logprob.token)
                result["log_prob"] = float(logprob.logprob)
                results.append(result)

    resultFinal = dict()
    resultFinal["id"] = response.id
    resultFinal["id_normative"] = id_normative
    resultFinal["name_normative"] = name_normative
    resultFinal["alias_normative"] = alias_normative
    resultFinal["id_law"] = id_law
    resultFinal["name_law"] = name_law
    resultFinal["alias_law"] = alias_law
    resultFinal["categories"] = results
    return resultFinal