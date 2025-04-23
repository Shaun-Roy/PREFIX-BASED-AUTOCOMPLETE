
# PREFIX MATCHING BASED AUTOCOMPLETE

Here we are creating a simple autocomplete system using a flask api and sql for storage, redis for a cache system and MISTRAL LLM as a fallback mechanism.

## LOGIC
The heart of our project is the flask API. When the user types something in our UI, the input goes to the API. The API first cheks our redis cache for prefix matches. if it cannot find a match, it moves on to SQL. Finally if SQL cannot find a prefix match too, we use LLM to generate autocomplete suggestions.

## FLOW

![ DIAGRAM ](https://github.com/Shaun-Roy/PREFIX-BASED-AUTOCOMPLETE/blob/main/screenshots%20for%20readme/Screenshot%202025-04-23%20141327.png)


## STEPS INVOLVED


1 Chose a .txt file

2 Cleaned the data (made it lowercase, removed special characters,etc)

3 Created n-grams and stored them in a csv file

4 Stored the csv data into SQLite Database with this schema:

```sql
CREATE TABLE ngrams (
    ngrams TEXT ,
    count INTEGER DEFAULT 0
)
```
5 Created FLASK API and routed it to simple index.html page

6 Used PREFIX MATCHING to get next word suggestions on input data

```sql"
SELECT ngrams FROM ngrams WHERE ngrams LIKE ? ORDER BY count DESC LIMIT 5"
```
7 Created a cache in redis (code in flask api itself)

8 Used LLM (MISTRAL) as a fallback mechanism to deal with unseen data

**PROMPT :**
```
f"generate up to {needed} possible completions for the prefix '{user_input}'. MAKE SURE THE COMPLETIONS ARE GRAMMATICALLY CORRECT AND LOGICAL. "
"Respond ONLY with a JSON array of strings like this: "
'["completion 1", "completion 2", ..., "completion n"]\n'
"THE OUTPUTS SHOULD INCLUDE ONLY THE PART OF THE COMPLETION THAT COMES AFTER THE PREFIX. IF THE INPUT IS 'WA' AND THE COMPLETIONS ARE 'was not' OR 'water', "
"THE OUTPUT SHOULD BE 's not' AND 'ter' (WITHOUT INCLUDING 'WA')."
"IF THE COMPLETION IS A CONTINUATION OF THE SAME WORD, DO NOT ADD A SPACE. IF IT IS A NEW WORD, ADD A LEADING SPACE."
"DO NOT include any explanation, formatting, markdown, or extra text. Just return the JSON array."
```
9 Cached LLM outputs too to reduce number of calls to LLM.





## Tech Stack

**FRONT END :** 

HTML, CSS, VANILLA JS

**BACK END :**

FLASK, SQLITE, REDIS (IN DOCKER), MISTRAL LLM

**DEVELOPMENT & ENVIORNMENT :**

GOOGLE COLAB, VS CODE, DOCKER (FOR REDIS)



