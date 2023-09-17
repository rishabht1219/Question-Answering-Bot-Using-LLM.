import logging
import asyncio
import concurrent.futures
from config import options
from async_timeout import timeout
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from google.cloud import dialogflow
from Models import Item , ResponseModel
from google.api_core.exceptions import InvalidArgument
from utils import get_source,extract_firstlink,google_search_firstlink,final_search,summarize_model,selection_algorithm_with_similarity

app = FastAPI()

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(options["log_path"], maxBytes=200000,backupCount=5)
logger.addHandler(handler)

DIALOGFLOW_PROJECT_ID = 'newagent-hyjn'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

async def some_other_function(text:str):
    loop = asyncio.get_event_loop()
    logger.info("response.query_result.action == input.unknown")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fs = await loop.run_in_executor(executor, final_search, text)
    #fs = final_search(text)  # sends three concurrent requests: wikipedia,google snippet, google knowledge graph, google first link content
    logger.info(f"Final search result: {fs}")
    sa = selection_algorithm_with_similarity(text,fs) # select best text results from final search
    logger.info(f"Selection algorithm result : {sa}")
    if len(sa.get('content','').split(' ')) < 100:
        logger.info(f"Content less than 100 words in selection algorithm: {sa}")
        summary = sa # summarise the selection algorithm text
        logger.info(f"Summary not created: {summary}")
        try:
            search_result = {'text':text,'summary':summary['content'],'url':summary['url'],'first_link':google_search_firstlink(text)}
        except KeyError:
            search_result = {'text':text,'summary':summary,'url':sa.get('url',""),'first_link':google_search_firstlink(text)}
        logger.info(f"Response returned: {search_result}")
    else:
        summary = summarize_model(sa)
        logger.info(f"Summary  created: {summary}")
        search_result = {'text':text,'summary':summary['summary'],'url':summary['url'],'first_link':google_search_firstlink(text)}
        logger.info(f"Response returned: {search_result}")
    return search_result

async def rishabh(query_input,text):
    response = session_client.detect_intent(session=session, query_input=query_input)
    task1 = asyncio.create_task(some_other_function(text))
    if response.query_result.action == "input.unknown":
        result = await asyncio.wait_for(task1, timeout=20)
        return result
    else:
        return_result =  {'text':"",'summary':response.query_result.fulfillment_text,'url':"",'first_link':""}
        logger.info("Response sent from dialog flow {return_result}")
        return return_result
 
@app.post("/search")
async def any(item: Item)->ResponseModel:
    item = dict(item)
    text = item["text"]
    logger.info("*************************************")
    logger.info(f"Request received for query : {text}")

    text_input = dialogflow.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        task = asyncio.create_task(rishabh(query_input,text))
        result = await asyncio.wait_for(task, timeout=20)
        return result
    except asyncio.TimeoutError:
        print("The long operation timed out, but we've handled it.")
        return {"error":"Timeout please rephrase the question! "}
    except Exception as err:
        print(err)
   
    