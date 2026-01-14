from openai import OpenAI

def queryCompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n, previous_id, putText):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output1 = "Category 0: (1),(2)(a),(3)(2)\nCategory 1: (1)(a),(5)(b) I made this match because (here your reasons)\nCategory 2: None I decided this because (here your reasons)"
    example2 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output2 = "Category 0: (1)(f),(3)(5),(4)(3)(c) I made this match because (here your reasons)\nCategory 1: None\nCategory 2: (3) I made this match because (here your reasons)"
    instructions ="Considering your previous answer, you must now found the items of the privacy legal framework " + name_law + " that are aligned or covers each category of the standard " + name_normative + "." \
        "An item of the privacy legal framework can be an article, that you will represent through its number in parenthesis, e.g. (8) means article 8,\n" \
        "a subarticle of the privacy legal framework that belongs to an article or another subarticle, that you will represent through its numbers in parenthesis, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3, subarticle 2; " \
        "and a literal which can belong to an article or subarticle,  that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article 46 subarticle 5, literal c" \
        "Of course, if all subarticles of an article covers a category, then you just specify the article (not each of the subarticles). Try not to be redundant and resume the results as much as you can so that they are easy to read and interpret." \
        "Given the text of the privacy legal framework you must determine for each one of the " + str(n) + "categories of subclauses defined by the standard all those items of the privacy legal framework that are aligned or covers in some way each category. Of course each item of the privacy legal framework could be part or be aligned with various categories." \
        "The categories are coded with numbers from 0 to " + str(n-1) + "In case of a category with no items of the privacy legal framework determined, answer None for that category." \
        "Complement your answer explaining in one short paragraph the reasons why you made the match for each category.\n" 

    if putText:
        intructions = instructions + "The categories of subclauses defined by the standard and their definitions are the following:\n"+ textNormative + "\n" \

    intructions = instructions + "Here there are two examples of expected responses from you when analyzing the privacy legal framework:\n" \
        "Example:\n" \
        "Text of privacy legal framework: " + example1 + "\n" \
        "Expected ouput structure:" + output1 + "\n" \
        "Example 2:\n" \
        "Text of privacy legal framework: " + example2 + "\n" \
        "Expected ouput structure:" + output2

    inputgpt = ""
    if putText:
        inputgpt = inputgpt + "The following is the text of the privacy legal framework that you previously analyzed:\n" + textLaw

    response = client.responses.create(
        model="gpt-5.2",
        previous_response_id = previous_id,
        instructions = instructions,
        input= inputgpt,
        temperature=0,
        top_p=1
    )

    resultGpt = response.output_text
    return resultGpt