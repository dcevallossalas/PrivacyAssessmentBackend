# ---------------------------------------------------------------------------------------------
# Module for determining criteria of non-compliances
# ---------------------------------------------------------------------------------------------

# OpenAI library
from openai import OpenAI

# Determines the criteria of noncompliances
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
# previous_id: Identifier of the previous response for CoT reasoning
# putTex: Flag to determine if the text of the normative and law is requiered
def queryNoncompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n, previous_id, putText):
    client = OpenAI(api_key = apiKey)
    example1 = "Suppose that this is a fragment of another privacy legal framework."
    output1 = "Category 0: (Here you explain your reasons and key points in a maximum of two paragraphs)\nCategory 1: (Here you explain your reasons and key points in a maximum of two paragraphs)\nCategory 2: None."
    example2 = "Suppose that this is a fragment of another privacy legal framework."
    output2 = "Category 0: (Here you explain your reasons and key points in a maximum of two paragraphs)\nCategory 1: None. \nCategory 2: (Here you explain your reasons and key points in a maximum of two paragraphs)"
    
    input_system = "Considering your previous answer, you must now analyze the privacy legal framework " + name_law + " and the categories of subclauses of the standard " \
    + name_normative + " in order to determine for each category the privacy gaps, points, aspects, factors, or arguments that are not covered by the privacy legal " \
    + "framework. In your explanation, you will have to refer to the items analyzed. " \
    + "An item of the privacy legal framework can be an article, that you will represent through its number in parentheses, " \
    + "e.g. (8) means article 8, a subarticle of the privacy legal framework that belongs to an article or another subarticle, that you will represent through its " \
    + "numbers in parentheses, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3 subarticle 2; and a literal which can belong to an " \
    + "article or subarticle,  that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article " \
    + "46 subarticle 5 literal c. If all subarticles of an article cover a category, then you just specify the article (not each of the subarticles). " \
    + "Given the text of the privacy legal framework, you must determine for each one of " \
    + "the " + str(n) + " categories of subclauses defined by the standard (in a maximum of two paragraphs) the reasons why the privacy legal framework does not fulfill" \
    + "or is not aligned in some way with each subclause.\n" \
    + "Here, there are two examples of expected output structures from you when analyzing a fragment of another privacy legal framework:" \
    + "Example:\n" \
    + "Text: " + example1 + "\n" \
    + "Expected ouput structure:" + output1 + "\n" \
    + "Example 2:\n" \
    + "Text: " + example2 + "\n" \
    + "Expected ouput structure:" + output2

    input_user = "Perform the task using the text of the privacy legal framework previously provided."
   
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
        previous_response_id = previous_id,
        temperature=0,
        top_p=1
    )

    return response.output_text