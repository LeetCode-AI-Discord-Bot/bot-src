import requests
import re
from markdownify import markdownify as html_to_md

# TODO: Add redis caching here to save on url calls, if i feel like it
class LeetCodeProblem():
    def __init__(self, leetcode_url: str):
        self.__base_url = "https://alfa-leetcode-api.onrender.com/"
        self.leetcode_url = leetcode_url
        self.problem_url_tile = self.__extract_problem_name(self.leetcode_url)    
        self.__getData()

    def __extract_problem_name(self, url: str) -> str:
        match = re.search(r'leetcode\.com/problems/([^/]+)/', url)
        if not match:
            raise Exception("Invalid LeetCode URL")

        return match.group(1)
    
    def __getData(self) -> None:
        try:
            self.raw_data = requests.get(self.__base_url+"select?titleSlug="+self.problem_url_tile).json()
            self.title = self.raw_data["questionTitle"]
            self.hints = [html_to_md(x) for x in self.raw_data["hints"]]
            self.question = html_to_md(self.raw_data["question"])
        except Exception as exc:
            raise Exception("Failed to get data from LeetCode API") from exc


if __name__ == "__main__":
    problem = LeetCodeProblem("https://leetcode.com/problems/")
    print(problem.question)
    print(problem.title)
    print(problem.hints)
