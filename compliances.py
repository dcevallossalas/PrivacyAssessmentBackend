def queryCompliances(apiKey, id_normative, name_normative, alias_normative, id_law, name_law, alias_law, textNormative, textLaw, n):
    client = OpenAI(api_key = apiKey)
    example1 = "Suposse that this is a very long text with the law to analyze."
    output1 = "Category 0: (1),(2)(a),(3)(2)\nCategory 1: (1)(a),(5)(b) I made this math because (here your reasons)\nCategory 2: None I made this math because (here your reasons)"
    example2 = "Suposse that this is a very long text with the law to analyze."
    output2 = "Category 0: (1)(f),(3)(5),(4)(3)(c) I made this math because (here your reasons)\nCategory 1: None\nCategory 2: (3) I made this math because (here your reasons)"
    message = [{
        "role": "system",
        "content": "You are an expert in privacy and must found the items of the law " + name_law + " that are aligned or covers each category of the normative " + name_normative + "." +
        "An item of the law can be an article, that you will represent through its number in parenthesis, e.g. (8) means article 8,\n"+
        "a subarticle of the law that belongs to an article or another subarticle, that you will represent through its numbers in parenthesis, e.g. (8)(2) means article 8 subarticle 2; (5)(3)(2) means article 5 subarticle 3, subarticle 2; "+
        "and a literal which can belong to an article or subarticle,  that you will represent through its numbers and literal in parenthesis, e.g. (4)(a) means article 4 literal a; (46)(5)(c) means article 46 subarticle 5, literal c" +
        "Of course, if all subarticles of an article covers a category, then you just specify the article (not each of the subarticles). Try not to be redundant and resume the results as much as you can so that they are easy to read and interpret."
        "Given the text of the law you must determine for each one of the " + str(n) + "categories of goals defined by the normative all those items of the law that are aligned or covers in some way each category. Of course each item of the law could be part or be aligned with various categories." +
        "The categories are coded with numbers from 0 to " + str(n-1) + "In case of a category with no items of the law determined, answer None for that category." +
        "Complement your answer explaining in one short paragraph the reasons why you made this match for each category."

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