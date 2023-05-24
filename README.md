# AI-File-Assistant

For a long time, I've found the local file search results on my laptop to be less than satisfactory, especially when I want to search for an image or a PDF. I often remember only a few keywords from the file, but I forget the file name.

In recent months, I've witnessed the power of ChatGPT4 and the rapid development of the AI community. Seizing this opportunity, I decided to use ChatGPT4 along with free open-source models and libraries to implement an AI file assistant from scratch in my spare time to improve the search quality of PDFs and images. This was a project that I didn't dare to think about before, because it involves knowledge from many different fields, and learning and using them all on my own would take a lot of time. Fortunately, now I have a "reliable" assistant, ChatGPT4, and I will use it to embark on this experiment.

I envision the AI file assistant having three main functions:

1. Users can specify the folders they want to track, and the AI file assistant can index the PDFs and images inside them. Of course, users can also cancel tracking of a folder.
2. Users can ask questions about a PDF file, and the AI file assistant can return the closest answer along with its source.
3. Users can enter several keywords for an image, and the AI file assistant can return the closest image source.

Of course, the front-end interface and the database are also indispensable. Here is the overall architecture of the AI file assistant system:
![Overall architecture](./overall_architecture.png)

Undeniably, utilizing OpenAI's APIs could greatly streamline the development process and significantly enhance the user experience. However, in consideration of budget constraints, I chose not to integrate them into this project to avoid additional costs. Despite this, the project was completed within a timeframe of just four days, and it was really remarkable.

Here was my experience while playing with the AI file assistant. The speed of image indexing was acceptable, although there were instances of inaccuracies in the text extraction. PDF indexing was tested using academic papers, with each paper taking between 30 and 60 seconds to index. A performance analysis revealed that the majority of the time was consumed by the embedding model, underscoring the benefits of having a GPU or a smaller embedding model.

For future enhancements, there are several improvements I am keen to implement:
1. The integration of a large language model for fine-tuning query outputs, which could substantially improve the readability and accuracy of results.
2. Developing functionality to index existing files in newly registered directories, increasing the system's convenience and efficiency.
3. Interaction with AI models hosted in the cloud, improving the performance of the system.

I have included all the conversations I had with ChatGPT4 in the /gpt_chats folder, encompassing two sessions titled "File Assistant with AI" and "File Assistant with AI 2".


## Environment Setup
```
conda create -n AiFileAssistant python=3.8.16
conda activate AiFileAssistant

# Install Python dependencies
cd [parent_directory_of_project]/AI-File-Assistant
pip install -r requirements.txt

# Start AI-File-Assistant
sudo python main.py

# To interact with the assistant, input the following URL into your web browser: http://localhost:8000/
```

## Acknowledgements
This project utilizes a variety of open-source models and libraries, and I am immensely grateful for their contributions. Here are some of the key components that have played a crucial role:

[watchdog](https://pypi.org/project/watchdog/): for file change detection;

[FastAPI](https://fastapi.tiangolo.com/lo/): for web framework;

[PyPDF2](https://pypi.org/project/PyPDF2/): for PDF text extraction;

[easyocr](https://pypi.org/project/easyocr/): for image text extraction;

[chromadb](https://docs.trychroma.com/): for vector embedding database;

[langchain](https://python.langchain.com/en/latest/index.html): for large language model application framework;

[Hugging Face](https://huggingface.co/): for open-source AI models;