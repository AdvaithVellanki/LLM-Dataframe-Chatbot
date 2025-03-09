This project creates a chatbot to read an interact with a dataframe using Streamlit. 
It requires a local LLM, which can be downloaded using OLLAMA (https://ollama.com/download)

Once OLLAMA is downloaded, you need to pull an LLM you want to use along with selecting the number of parameters depending on device memory.
After the LLM has been downloaded, install the requirements from requirements.txt and then run "streamlit run src/main.py" in the terminal

The LLM being used in this script is the Deepseek-r1:8b model. This can be changed to any other LLM by changing the name of the LLM in line 58 in main.py
