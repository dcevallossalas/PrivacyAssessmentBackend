# ---------------------------------------------------------------------------------------------
# Module for determining criteria of compliances
# ---------------------------------------------------------------------------------------------

# OpenAI library
from openai import OpenAI

# Determines the criteria of compliances
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
def queryCompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n, previous_id, putText):
    client = OpenAI(api_key = apiKey)
    example1 = "Suppose that this is a text of another privacy legal framework."
    output1 = "Category 0: (1),(2)(a),(3)(2) I made this match because (here reasons). \nCategory 1: (1)(a),(5)(b) I made this match because (here reasons)\nCategory 2: None I decided this because (here reasons)"
    example2 = "Suppose that this is a text of another privacy legal framework."
    output2 = "Category 0: (1)(f),(3)(5),(4)(3)(c) I made this match because (here reasons)\nCategory 1: None. I decided this because (here reasons)\nCategory 2: (3) I made this match because (here reasons)"
    
    input_system = "Considering your previous answer, you must now find the items of the privacy legal framework " + name_law + " that are aligned or cover each category " \
    "of the standard " + name_normative + ". An item of the privacy legal framework can be an article, that you will represent through its number in parentheses, " \
    "e.g. (8) means article 8, a subarticle of the privacy legal framework that belongs to an article or another subarticle, that you will represent through its " \
    "numbers in parentheses, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3 subarticle 2; and a literal which can belong to an " \
    "article or subarticle,  that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article " \
    "46 subarticle 5 literal c. If all subarticles of an article cover a category, then you just specify the article (not each of the subarticles). Try not to be " \
    "redundant and summarize the results as much as you can, so that they are easy to read and interpret. Of course, each item of the privacy legal framework could " \
    "be part or be aligned with various categories. Complement your answer by explaining in one short paragraph the reasons why you made the match for each category. " \
    "Answer in English.\n" \
    "Here, there are two examples of expected output structures from you when analyzing a fragment of another privacy legal framework:\n" \
    "Example:\n" \
    "Text: " + example1 + "\n" \
    "Expected ouput structure:" + output1 + "\n" \
    "Example 2:\n" \
    "Text: " + example2 + "\n" \
    "Expected ouput structure:" + output2

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