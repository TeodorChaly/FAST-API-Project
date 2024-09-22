# News Generator Application


## Introduction
This project, "News Generator," leverages the OpenAI GPT models to automate the creation of news content across various categories. It is designed for content creators, marketers, and news agencies looking to streamline their content generation process. The system integrates with existing JSON-based data infrastructures and provides a seamless workflow for producing high-quality, tailored news articles.


### Key Features

-   **Automated News Generation**: Utilizes GPT models to generate news content that is coherent, contextually relevant, and up-to-date.
-   **Multi-Language Support**: Offers the capability to generate news in multiple languages, enhancing global reach.
-   **SEO Optimization**: Automatically generates SEO-friendly titles and descriptions to boost search engine visibility.
-   **Custom Category Creation**: Users can define and modify news categories according to their needs.


### Installation

1.  Clone the repository:
    
    `git clone https://github.com/yourgithub/news-generator.git` 
    
2.  Install the required packages:
 
    `pip install -r requirements.txt` 
    
3.  Set up environment variables:
    -   `MY_OPENAI_API_KEY`: Your OpenAI API key.
    -   `LANGUAGE_API_KEY`: Your password key for language changing
    -   `LANGUAGE_API_NAME`: Your name for language changing
### Usage

Start the application by running the following command:

`uvicorn main:app --reload --port 8000` 

Access the application through `localhost:8000` in your web browser.
