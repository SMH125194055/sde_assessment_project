import time
import random
from typing import Dict

def mock_model_predict(input_data: str) -> Dict[str, str]:

    print(f"Simulating prediction for input: {input_data}")
    #  Simulate processing delay between 10 to 17 seconds 
    time.sleep(random.randint(10, 17))
    #  Generate a random result 
    result = str(random.randint(1000, 20000))
    output = {"input": input_data, "result": result}
    print(f"Prediction result: {output}")
    return output