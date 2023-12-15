from src_IR_prediction.tool_selection import SelectTools
from src_IR_prediction.data_loader import JLoader
import time


class Model:
    def __init__(self):
        return

    def data_preparation(self):
        jld = JLoader("test_project.json")
        dataset = jld.load_dataset()
        cve_ld = JLoader("CVE_dict.json")
        cve_dataset = cve_ld.load_dataset()
        l_query = list()
        for data_item in dataset:
            # query_res = stool.query(self.concatenate_pattern(data_item))
            query_item = self.concatenate_pattern(data_item, cve_dataset)
            l_query.append(query_item)
        return l_query

    def data_query(self, stool, query_list):
        prompt_base = "Is the following issue report matches the CVE?\n"
        count_pos = 0
        res_list = list()
        for i, query_item in enumerate(query_list):
            query_data, query_res = stool.query(prompt_base + query_item)
            count_pos += query_data
            print("Total Accurate Prediction {}/{}".format(count_pos, i + 1))
            res_list.append(query_res)
            time.sleep(10)
        return res_list

    def concatenate_pattern(self, data_item, cve_dataset):
        content = "Issue Title ({});\nIssue Body ({});\nMatched CVE ({})"\
            .format(data_item["Issue_Title"], data_item["Issue_Body"],
                   data_item["CVE_ID"])
        if data_item["CVE_ID"] != '':
            content += "({})".format(cve_dataset[data_item["CVE_ID"]]["CVE_Description"])
        return content


if __name__ == "__main__":
    model = Model()
    query_list = model.data_preparation()
    stool = SelectTools()
    model.data_query(stool, query_list)