import requests
import re
from markdownify import markdownify as html_to_md

def extract_problem_name(url: str) -> str:
    match = re.search(r'leetcode\.com/problems/([^/]+)/', url)
    if not match:
        return None
    
    return match.group(1)

# TODO: Add redis caching here to save on url calls, if i feel like it
class LeetCodeProblem():
    def __init__(self, leetcode_url: str):
        self.__base_url = "https://alfa-leetcode-api.onrender.com/"
        self.leetcode_url = leetcode_url
        self.problem_url_tile = self.__extract_problem_name(self.leetcode_url)    
        self.__getData()

    def __extract_problem_name(self, url: str) -> str:
        problem_name = extract_problem_name(url)
        if not problem_name:
            raise Exception(f"Invalid LeetCode URL: {self.leetcode_url}")
        return problem_name
    
    def __getData(self) -> None:
        try:
            self.raw_data = requests.get(self.__base_url+"select?titleSlug="+self.problem_url_tile).json()
            self.title = self.raw_data["questionTitle"]
            self.hints = [html_to_md(x) for x in self.raw_data["hints"]]
            self.question = html_to_md(self.raw_data["question"])
        except Exception as exc:
            raise Exception(f"Failed to get data from LeetCode API: {str(exc)}") from exc


if __name__ == "__main__":
    problem = LeetCodeProblem("https://leetcode.com/problems/")
    print(problem.question)
    print(problem.title)
    print(problem.hints)
