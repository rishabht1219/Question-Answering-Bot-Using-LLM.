import bs4
import spacy
import requests
import wikipedia
import concurrent.futures
from config import options
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained('t5-base')
model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

nlp = spacy.load("en_core_web_lg")

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def google_search_firstlink(text:str):
    try:
        url = f"https://www.google.com/search?q={text}"
        response = requests.get(url, headers=options['headers'],timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all('a')
        first_result = None
        for link in search_results:
            url = link.get('href')
            if "/url?q=" in url:
                first_result = url.split("/url?q=")[1].split("&")[0]
                break
        return first_result 
    except Exception as err:
        return err

def extract_firstlink(url:str):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all('p')
        all_paragraphs= []
        for p in paragraphs:
            all_paragraphs.append(p.text)
        content = "".join(all_paragraphs)
        result = {"url":url,"content":content}
        return result
    except:
        return  {}

def wikipedia_search(text:str):
    try :
        page = wikipedia.page(text)
        content = page.content
        url = page.url
        result = {"url":url,"content":content}
        return result
    except wikipedia.exceptions.WikipediaException:
        return {"url":'',"content":''}

def google_snippet(text:str):
    try:
        url = "https://google.com/search?q=" + text
        request_result = requests.get( url)
        soup = bs4.BeautifulSoup( request_result.text , "html.parser" )
        content = soup.find( "div" , class_='BNeawe' ).div.div.text
        result = {"url":google_search_firstlink(text),"content":content }
        return result
    except:
        return {"url":'',"content":''}
         
def extract_content_from_firstlink(text:str):
    firsturl = google_search_firstlink(text)
    first_link_result = extract_firstlink(firsturl)
    return first_link_result
    
# def final_search(search_query:str):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#         wikipedia_result = executor.submit(wikipedia_search, search_query)
#         google_snippet_result= executor.submit(google_snippet,search_query )
#         first_link_result = executor.submit(extract_content_from_firstlink,search_query )
#         concurrent.futures.wait([wikipedia_result,google_snippet_result,first_link_result])
#         final_result = {"wikipedia_result":wikipedia_result.result(),"google_snippet_result":google_snippet_result.result()
#                     ,"first_link_result":first_link_result.result()}
#         return final_result


  
def final_search(search_query:str):
    wikipedia_result = wikipedia_search(search_query)
    google_snippet_result= google_snippet(search_query)
    first_link_result = extract_content_from_firstlink(search_query)
    final_result = {"wikipedia_result":wikipedia_result,"google_snippet_result":google_snippet_result
                ,"first_link_result":first_link_result}
    return final_result

def selection_algorithm_with_similarity(question:str,final_result:dict) -> dict:
    try:
        scores = []
        s = ['wikipedia_result','google_snippet_result','first_link_result']
        for source,result in final_result.items():
            if source == "google_snippet_result":
                content = final_result[source].get('content',"")
                if len(content) > 1:
                    return final_result[source]
            doc1 = nlp(question)
            answer = result.get('content',"")
            if answer != "":
                doc2 = nlp(answer)
                score  = doc1.similarity(doc2)
            else:
                score = 0
            scores.append(score)
        max_value = max(scores)
        index = scores.index(max_value)
        return final_result[s[index]]
    except Exception as e:
        return {"url":'',"content":"Sorry,cannot find results for your query!"}

def summarize_model(text:dict):
    inputs = tokenizer.encode("summarize: " + text['content'],
                          return_tensors='pt',
                          max_length=512,
                          truncation=True)
    summary_ids = model.generate(inputs,max_length=250, min_length=100,length_penalty=1, num_beams=2)
    summary = tokenizer.decode(summary_ids[0],skip_special_tokens=True)
    summary_ids[0]
    return {'url':text['url'],'summary':summary}




