from openai import OpenAI

def queryGpt(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the law to analyze."
    output1 = "0,1,2"
    example2 = "Suposse that this is a very long text with the law to analyze."
    output2 = "3,4"
    message = [{
        "role": "system",
        "content": "You are an expert in privacy and must determine how well aligned is the law " + name_law + "with the normative " + name_normative + "." +
        "Given the text of the law you must determine whether it suggests and/or compels the compliance of each one of the " + str(n) + "categories of goals defined by the normative." +
        "The categories are coded with numbers from 0 to " + str(n-1) + ". Just return the codes without a reason or extra text. In case of no categories selected, answer None." +

        "The categories of goals defined by the law and their definitions are the following:\n"+ textNormative + "\n"

        "Here there are two examples of expected responses from you when analyzing the law:\n" \
        "Example 1:\n" \
        "Text of law: " + example1 + "\n" \
        "Expected ouput:" + output1 + "\n" \
        "Example 2:\n" \
        "Text of law: " + example2 + "\n" \
        "Expected ouput:" + output2 \
    },
    {
        "role": "user",
        "content": "The following is the text of the law that you must analyze:\n" + textLaw
    }]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages= message,
        temperature=0,
        top_p=1,
        seed=1234,
        logprobs=True
    )

    resultGpt = response.choices[0].message.content
    results = list()
    if resultGpt == "" or resultGpt.strip().lower() == "none":
        result = dict()
        result["category"] = "None"
        result["log_prob"] = 0
        results.append(result)
    else:
        for logprob in response.choices[0].logprobs.content:
            if str(logprob.token) != "," and str(logprob.token) != " " and str(logprob.token) != ", " and str(logprob.token) != " ,":
                result = dict()
                result["category"] = int(logprob.token)
                result["log_prob"] = float(logprob.logprob)
                results.append(result)

    resultFinal = dict()
    resultFinal["id_normative"] = id_normative
    resultFinal["name_normative"] = name_normative
    resultFinal["alias_normative"] = name_normative
    resultFinal["id_law"] = id_law
    resultFinal["name_law"] = name_law
    resultFinal["alias_law"] = name_law
    resultFinal["categories"] = results
    return resultFinal