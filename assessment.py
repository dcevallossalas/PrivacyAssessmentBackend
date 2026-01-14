from openai import OpenAI

def queryGpt(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output1 = "0,1,2,17"
    example2 = "Suposse that this is a very long text with the privacy legal framework to analyze."
    output2 = "3,21"
    instructions = "You are an expert in privacy and must determine how well aligned is the privacy legal framework " + name_law + "with the standard " + name_normative + "." \
        "Given the text of the privacy legal framework you must determine whether it suggests and/or compels the compliance of each one of the " + str(n) + "subclauses defined by the standard." \
        "The categories are coded with numbers from 0 to " + str(n-1) + ". Just return the codes without a reason or extra text. In case of no categories selected, answer None." \
        "The categories of subclauses defined by the standard and their definitions are the following:\n"+ textNormative + "\n" \
        "Here there are two examples of expected responses from you when analyzing the privacy legal framework:\n" \
        "Example 1:\n" \
        "Text of privacy legal framework: " + example1 + "\n" \
        "Expected ouput:" + output1 + "\n" \
        "Example 2:\n" \
        "Text of privacy legal framework: " + example2 + "\n" \
        "Expected ouput:" + output2 \
        
    inputgpt =  "The following is the text of the privacy legal framework that you must analyze:\n" + textLaw

    response = client.responses.create(
        model="gpt-5.2",
        instructions = instruction,
        input= inputgpt,
        temperature=0,
        top_p=1,
        seed=1234,
        logprobs=True
    )

    resultGpt = response.output_text
    results = list()
    if resultGpt == "" or resultGpt.strip().lower() == "none":
        result = dict()
        result["category"] = "None"
        result["log_prob"] = 0
        results.append(result)
    else:
        for logprob in response.output_text.logprobs:
            if str(logprob.token) != "," and str(logprob.token) != " " and str(logprob.token) != ", " and str(logprob.token) != " ,":
                result = dict()
                result["category"] = int(logprob.token)
                result["log_prob"] = float(logprob.logprob)
                results.append(result)

    resultFinal = dict()
    resultFinal["id"] = response.id
    resultFinal["id_normative"] = id_normative
    resultFinal["name_normative"] = name_normative
    resultFinal["alias_normative"] = name_normative
    resultFinal["id_law"] = id_law
    resultFinal["name_law"] = name_law
    resultFinal["alias_law"] = name_law
    resultFinal["categories"] = results
    return resultFinal