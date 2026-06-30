import io
import sys
import contextlib
import traceback
import re

class ReplManager:
    def __init__ (self):

        self.global_state = {}
    

    def load_huge_content (self, text_data, variable_name = "LONG_CONTEXT"):
        self.global_state[variable_name] = text_data

        print (f"[REPL] Data loaded into {variable_name}. Length: {len(text_data)} characters. ")
    

    def extract_code (self, llm_response):
        pattern = r"```python\n(.*?)\n```"
        match = re.search(pattern, llm_response, re.DOTALL)


        if match:
            return match.group(1).strip()
        
        return llm_response.strip()
    
    def execute (self, llm_response):
        stdout_capture = io.StringIO()


        try:
            with contextlib.redirect_stdout(stdout_capture):
                exec (code_string, self.global_state)