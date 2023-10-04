from metaphor_python import Metaphor
import openai
from datetime import date
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

openai.api_key = "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"
metaphor = Metaphor("e20637d1-1473-4095-8e0e-389e77d244f6")

query = "Here is the latest news in the world of cars:"

SYSTEM_MESSAGE = "You are a helpful assistant that summarizes the content of a webpage. Summarize the users input."


@app.route('/')
def index():
    print(date.today())
    response = metaphor.search(
        query,
        num_results = 9,
        start_published_date = str(date.today())
    )
    print(response.results)
    #summaries = []
    
    # for res in contents_result.contents:
    #     completion = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": SYSTEM_MESSAGE},
    #             {"role": "user", "content": contents_result.contents[0].extract}
    #         ]
    #     )
    #     summaries.append(completion.choices[0].message.content)
    
    # print(summaries)
    
    results = []
    photos = []
    
    for res in response.results:
        results.append(res)
        response = requests.get(res.url)

        
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to retreive the webpage. Status code: {response.status_code}")

        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        
        largest_image_url = None
        largest_image_size = 0
        
        for img in img_tags:
            img_url = img.get('src')
            img_width = img.get('width')
            img_height = img.get('height')
            img_size = 0
            
            if img_url and img_width and img_height:
                img_size = int(img_width) * int(img_height)

            if img_size > largest_image_size:
                largest_image_size = img_size
                largest_image_url = img_url
            
        if largest_image_url == None:
            first_img = img_tags[0]
            img_url = first_img.get('src') 
            photos.append(img_url)
        else:
            photos.append(largest_image_url)
        
    print(photos)
    return render_template('index.html', results=zip(results, photos))

if __name__ == '__main__':
    app.run()

