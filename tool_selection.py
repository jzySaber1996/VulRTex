import re
import httpx
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src_IR_prediction import Config as cf
from src_IR_prediction.chat_bot import ChatBot
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"

class SelectTools:
    def __init__(self):
        self.prompt = cf.prompt.strip()
        self.action_re = re.compile('^Action: (\w+): (.*)$')
        self.known_actions = {
            "wikipedia": self.wikipedia,
            "compare": self.compare_res,
            "issue_search": self.issue_search,
            "comment_search": self.comment_search
        }
        return

    def query(self, question, max_turns=5):
        i = 0
        bot = ChatBot(self.prompt)
        next_prompt = question
        while i < max_turns:
            i += 1
            '''
            Predict the thought and actions with LLM. The format is as follows:
            @ Thought: I will use the {action name} action to analyze the issue report and CVE.
            @ Action: {action name}, content of questions.
            '''
            result = bot(next_prompt)
            print(result)
            # if "Action" not in result:
            #     result = result.replace("Answer", "Action")
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                # There is an action to run
                action, action_input = actions[0].groups()
                if action not in self.known_actions:
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                print(" -- running {} {}".format(action, action_input))
                '''
                Output the observation, and check whether the issue report matches the CVE. 
                '''
                observation = self.known_actions[action](action_input)
                print("Observation:", observation)
                sent_pos = self.sentiment_analysis(observation)
                if sent_pos:
                    return 1, observation
                else:
                    '''
                    Cannot match the issue report and CVE directly, so select the next tool. 
                    '''
                    next_prompt = "Observation: {}".format(observation)
                    next_prompt = bot(next_prompt)
                    next_prompt = "Question: {}".format(next_prompt.replace("Answer", ""))
                    # question += observation
                    # next_prompt = question
            else:
                return 0, ""

    def compare_res(self, q):
        bot_compare = ChatBot()
        res_compare = bot_compare(q)
        return res_compare

    def sentiment_analysis(self, q):
        sid = SentimentIntensityAnalyzer()
        sent_res = sid.polarity_scores(q.split(',')[0])
        if sent_res['pos'] > sent_res['neg']:
            return True
        else:
            sent_res_ful = sid.polarity_scores(q)
            if sent_res_ful['pos'] > sent_res_ful['neg']:
                return True
            else:
                return False

    def issue_search(self, q):
        print("issue_search")
        return

    def comment_search(self, q):
        print("comment_search")
        return

    def wikipedia(self, q):
        return httpx.get("https://en.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        }).json()["query"]["search"][0]["snippet"]

    def search_screenshot(self, q):
        try:
            cred = credential.Credential("SecretId", "SecretKey")
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "", clientProfile)

            req = models.GeneralBasicOCRRequest()
            params = {
                "ImageUrl": q
            }
            req.from_json_string(json.dumps(params))
            resp = client.GeneralBasicOCR(req)
            print(resp.to_json_string())
            return resp.to_json_string()
        except TencentCloudSDKException as err:
            print(err)