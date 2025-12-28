def queryNoncompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the law to analyze."
    output1 = "Category 0: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 1: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 2: None"
    example2 = "Suposse that this is a very long text with the law to analyze."
    output2 = "Category 0: [Here you explain your reasons and key points in maximum two paragraphs]\nCategory 1: None\nCategory 2: [Here you explain your reasons and key points in maximum two paragraphs]"
    message = [{
        "role": "system",
        "content": "You are an expert in privacy and must analyze the law " + name_law + " and the categories of the normative " + name_normative + " in order to determine for each category" +
        "the main points, aspects, factor or arguments that are not convered by the law. In your explanation you will have to refer to the items analyzed. " +
        "An item of the law can be an article, that you will represent through its number in parenthesis, e.g. (8) means article 8,\n"+
        "a subarticle of the law that belongs to an article or another subarticle, that you will represent through its numbers in parenthesis, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3, subarticle 2; "+
        "and a literal which can belong to an article or subarticle,  that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article 46 subarticle 5, literal c" +
        "Of course, if all subarticles of an article covers a category, then you just specify the article (not each of the subarticles). Try not to be redundant and resume the results as much as you can so that they are easy to read and interpret."
        "Given the text of the law you must determine for each one of the " + str(n) + "categories of goals defined by the normative in maximum two paragraphs the arguments why the law does not fulfill with the normative." +
        "The categories are coded with numbers from 0 to " + str(n-1) + "In case the category is covered by the law completely, answer None for that category." +

        "The categories of goals defined by the law and their definitions are the following:\n"+ textNormative + "\n"

        "Here there are two examples of expected responses from you when analyzing the law:\n" \
        "Example:\n" \
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
        logprobs=False
    )

    resultGpt = response.choices[0].message.content
    return resultGpt