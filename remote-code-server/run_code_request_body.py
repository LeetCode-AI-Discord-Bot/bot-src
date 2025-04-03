class RunCodeRequestBody:
    def __init__(self, body: dict, code: str, thread_id: str) -> None:
        if body is None:
            raise ValueError("body is None")
        self.raw = body

        if code is None:
            raise ValueError("code is None")
        self.code = body["code"]

        if thread_id is None:
            raise ValueError("thread_id is None")
        self.thread_id = body["thread_id"]