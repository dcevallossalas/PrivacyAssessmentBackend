from openai import OpenAI

def queryNoncompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n, previous_id, putText):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output1 = "Category 0: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 1: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 2: None"
    example2 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output2 = "Category 0: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 1: None\nCategory 2: [Here you explain your reasons and key points in maximum two paragraphs]"
    instructions = "Considering your previous answer, you must now analyze the privacy legal framework " + name_law + " and the categories of subclauses of the standard " + name_normative + " in order to determine for each category" +
        "the main points, aspects, factor or arguments that are not convered by the privacy legal framework. In your explanation you will have to refer to the items analyzed. " +
        "An item of the privacy legal framework can be an article, that you will represent through its number in parenthesis, e.g. (8) means article 8,\n"+
        "a subarticle of the privacy legal framework that belongs to an article or another subarticle, that you will represent through its numbers in parenthesis, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3, subarticle 2; "+
        "and a literal which can belong to an article or subarticle, that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article 46 subarticle 5, literal c" +
        "Of course, if all subarticles of an article covers a category, then you just specify the article (not each of the subarticles). Try not to be redundant and resume the results as much as you can so that they are easy to read and interpret."
        "Given the text of the privacy legal framework you must determine for each one of the " + str(n) + "categories of subclauses defined by the standard in maximum two paragraphs the arguments why the privacy legal framework does not fulfill with the standard." +
        "The categories are coded with numbers from 0 to " + str(n-1) + "In case the category is not covered by the privacy legal framework completely, answer None for that category.\n" 

    if putText:
        instructions = instructions + "The categories of subclauses defined by the standard and their definitions are the following:\n"+ textNormative + "\n"

    instructions = instruction + "Here there are two examples of expected responses from you when analyzing the privacy legal framework:\n" \
        "Example:\n" \
        "Text of privacy legal framework: " + example1 + "\n" \
        "Expected ouput structure:" + output1 + "\n" \
        "Example 2:\n" \
        "Text of privacy legal framework: " + example2 + "\n" \
        "Expected ouput structure:" + output2 \

    inputgpt = ""
    if putText:
        inputgpt = inputgpt + "The following is the text of the privacy legal framework that you previously analyzed::\n" + textLaw

    response = client.chat.completions.create(
        model="gpt-5.2",
        previous_response_id = previous_id,
        instructions = instructions,
        input= inputgpt,
        temperature=0,
        top_p=1
    )

    resultGpt = response.choices[0].message.content
    return resultGpt