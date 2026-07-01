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
    
    def execute (self, code_string):
        stdout_capture = io.StringIO()


        try:
            with contextlib.redirect_stdout(stdout_capture):
                exec (code_string, self.global_state)
            
            output = stdout_capture.getvalue()

            if not output:
                output = "[REPL] Code executed successfully. No output."
            return output
        
        except Exception as e:
            error_trace = traceback.format_exc()
            return f"[REPL] Error during execution:\n{error_trace}"
        



if __name__ == "__main__":
    repl = ReplManager()

    fake_long_prompt = "This is a very long prompt that exceeds the token limit of the model. " * 100000

    repl.load_huge_content(fake_long_prompt, "INPUT_DATA")


    llm_output_1 = """
    I am checking the length of the input: 
    ```python
    data_length = len(INPUT_DATA)
    print(f"Length of INPUT_DATA: {data_length}")
    ```
    """

    code_1 = repl.extract_code(llm_output_1)

    result_1 = repl.execute(code_1)
    print ("[REPL] Execution Result 1:")
    print (result_1)

    llm_output_2 = """
    ```python
    #Divide the length by 2
    chunk_size = data_length // 2
    chunk_1 = INPUT_DATA[:chunk_size]
    chunk_2 = INPUT_DATA[chunk_size:]
    print(f"Chunk 1 length: {len(chunk_1)}")
    print(f"Chunk 2 length: {len(chunk_2)}")
    ```
    """


    code_2 = repl.extract_code(llm_output_2)
    result_2 = repl.execute (code_2)
    print ("[REPL] Execution Result 2:")
    print (result_2)



