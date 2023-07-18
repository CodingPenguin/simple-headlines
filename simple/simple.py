"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import json
import os, openai
import time
from typing import List
from pcconfig import config
import pynecone as pc
import pandas as pd
import simple.styles.global_styles as gs

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def chat_with_chatgpt(messages: list, model: str = "gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']
    
    
class State(pc.State):
    """The app state."""
    
    form_data: dict = {}
    website_headline: str = ""
    homepage_excerpt: str = ""
    subtitle: str = ""
    seo_headline: str = ""
    seo_excerpt: str = ""
    newsletter_intro: str = ""
    twitter_share: str = ""
    
    csv_path: str = "./web/public/"
    examples: pd.DataFrame
    
    async def handle_upload(self, files: List[pc.UploadFile]):
        file = files[0]
        upload_data = await file.read()
        outfile = f".web/public/{file.filename}"

        # Save the file.
        with open(outfile, "wb") as file_object:
            file_object.write(upload_data)

        self.csv_path = outfile
        examples = pd.read_csv(self.csv_path, escapechar='\\', quoting=0)
        self.examples = examples
        print(self.examples)
        
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        # clear current data
        self.website_headline = ""
        self.homepage_excerpt = ""
        self.subtitle = ""
        self.seo_headline = ""
        self.seo_excerpt = ""
        self.newsletter_intro = ""
        self.twitter_share = ""
    
        print('hello')
        self.website_headline = self.generate_website_headline()
        yield
        self.homepage_excerpt = self.generate_homepage_excerpt()
        yield
        self.subtitle = self.generate_subtitle()
        yield
        self.seo_headline = self.generate_seo_headline()
        yield
        self.seo_excerpt = self.generate_seo_excerpt()
        yield
        self.newsletter_intro = self.generate_newsletter_intro()
        yield
        self.twitter_share = self.generate_twitter_share()
        yield
        time.sleep(1)
        print("DONE!")
    
        
    def generate_website_headline(self):
        # make the messages such that it generates them as CSVs, not as readable lists and such. Consider using special character as delimiter.
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["headline_examples"]} headlines that summarize the content given and mimics the voice of the user using the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be in JSON format. Here is the expected format: {{"headlines: ["headline 1", "headline 2", "...", "headline {self.form_data["headline_examples"]}"]}}'},
            {'role': 'system', 'content': f'Limit your response to {self.form_data["headline_char_limit"]} characters.'},
            {'role': 'user', 'content': f'Please generate {self.form_data["headline_examples"]} headlines. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        if self.form_data["liked_headlines"].strip() != "":
            messages.insert(1, {'role': 'system', 'content': f'Here are some headlines that you should mimic, separated by a \\n character: {self.form_data["liked_headlines"]}'})
            
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = eval(output)['headlines']
        # print(f"headlines: {parsed_output}", end='\n\n\n\n\n\n\n\n')
        # return parsed_output
    
    def generate_homepage_excerpt(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["homepage_excerpt_examples"]} homepage excerpts that describe the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be a JSON object. Here is the expected JSON format: {{"homepage_excerpts": ["homepage_excerpt 1", "homepage_excerpt 2", "...", "homepage_excerpt {self.form_data["homepage_excerpt_examples"]}"]}}'},
            {'role': 'user', 'content': f'Please generate {self.form_data["homepage_excerpt_examples"]}, {self.form_data["homepage_excerpt_char_limit"]}-character homepage excerpts. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        if self.form_data["liked_homepage_excerpts"].strip() != "":
            messages.insert(1, {'role': 'system', 'content': f'Here are some homepage excerpts that you should mimic, separated by a \\n character: BEGIN EXAMPLES {self.form_data["liked_homepage_excerpts"]} END EXAMPLES'},)
            
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = eval(output)['homepage_excerpts']
        # print(f"homepage excerpts: {parsed_output}", end='\n\n\n\n\n\n\n\n')
        # return parsed_output
        
    def generate_subtitle(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["subtitle_examples"]} {self.form_data["subtitle_char_limit"]}-character subtitles that describe the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be in JSON format. Here is the expected format: {{"subtitles": ["subtitle 1", "subtitle 2", "...", "subtitle {self.form_data["subtitle_examples"]}"]}}'},
            {'role': 'user', 'content': f'Please generate {self.form_data["subtitle_examples"]}, {self.form_data["subtitle_char_limit"]}-character subtitles. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        if self.form_data["liked_subtitles"].strip() != "":
            messages.insert(1, {'role': 'system', 'content': f'Here are some subtitles that you should mimic, separated by a \\n character: BEGIN SUBTITLE EXAMPLES {self.form_data["liked_subtitles"]} END SUBTITLE EXAMPLES'})
            
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = eval(output)["subtitles"]
        # print(parsed_output, end='\n\n\n\n\n\n\n\n')
        # return parsed_output
    
    def generate_seo_headline(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["seo_headline_examples"]} {self.form_data["seo_headline_char_limit"]}-character SEO headlines that summarize the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be in JSON format. Here is the expected JSON format: {{"seo_headlines": ["seo_headline 1", "seo_headline 2", "...", "seo_headline {self.form_data["seo_headline_examples"]}"]}}'},
            # {'role': 'system', 'content': f'Here are some SEO headlines that you should mimic, separated by a \\n character: BEGIN EXAMPLES {self.form_data["liked_seo_headlines"]} END EXAMPLES'},
            {'role': 'user', 'content': f'Please generate {self.form_data["seo_headline_examples"]}, {self.form_data["seo_headline_char_limit"]}-character SEO headline. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = json.loads(output)
        # print(parsed_output)
        # print('\n\n\n\n\n\n\n\n\n\n\n\n')
        # return parsed_output['seo_headlines']
    
    def generate_seo_excerpt(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["seo_excerpt_examples"]} {self.form_data["seo_excerpt_char_limit"]}-character SEO excerpts that describe the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be a JSON object. Here is the expected JSON format: {{"seo_excerpts": ["seo_excerpt 1", "seo_excerpt 2", "...", "seo_excerpt {self.form_data["seo_excerpt_examples"]}"]}}'},
            # {'role': 'system', 'content': f'Here are some SEO excerpts that you should mimic, separated by a \\n character: BEGIN EXAMPLES {self.form_data["liked_seo_excerpts"]} END EXAMPLES'},
            {'role': 'user', 'content': f'Please generate {self.form_data["seo_excerpt_examples"]}, {self.form_data["seo_excerpt_char_limit"]}-character SEO excerpt. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
       
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = json.loads(output)
        # print(parsed_output)
        # print('\n\n\n\n\n\n\n\n\n\n\n\n')
        # return parsed_output['seo_excerpts']
    
    def generate_newsletter_intro(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["newsletter_intro_examples"]} {self.form_data["newsletter_intro_char_limit"]}-character newsletter intros that describe the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be in JSON format. Here is the expected JSON format: {{"newsletter_intros": ["newsletter_intro 1", "newsletter_intro 2", "...", "newsletter_intro {self.form_data["newsletter_intro_examples"]}"]}}'},
            # {'role': 'system', 'content': f'Here are some newsletter intros that you should mimic, separated by a \\n character: BEGIN EXAMPLES {self.form_data["liked_newsletter_intros"]} END EXAMPLES'},
            {'role': 'user', 'content': f'Please generate {self.form_data["newsletter_intro_examples"]}, {self.form_data["newsletter_intro_char_limit"]}-character newsletter intro. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = json.loads(output)
        # print(parsed_output)
        # print('\n\n\n\n\n\n\n\n\n\n\n\n')
        # return parsed_output['newsletter_intros']
    
    def generate_twitter_share(self):
        messages = [
            {'role': 'system', 'content': f'You will generate {self.form_data["twitter_share_examples"]} {self.form_data["twitter_share_char_limit"]}-character Twitter share messages that describe the content given, while mimicking the voice of the content by the same vernacular, formality, and tone.'},
            # {'role': 'system', 'content': f'Your response should be in JSON format. Here is the expected JSON format: {{"twitter_shares": ["twitter_share 1", "twitter_share 2", "...", "twitter_share {self.form_data["twitter_share_examples"]}"]}}'},
            # {'role': 'system', 'content': f'Here are some Twitter share messages that you should mimic, separated by a \\n character: BEGIN EXAMPLES {self.form_data["liked_twitter_shares"]} END EXAMPLES'},
            {'role': 'user', 'content': f'Please generate {self.form_data["twitter_share_examples"]}, {self.form_data["twitter_share_char_limit"]}-character Twitter share messages. BEGIN CONTENT {self.form_data["content"]} END CONTENT'}, 
        ]
        
        output = chat_with_chatgpt(messages)
        print(output, end='\n\n\n\n\n\n\n\n')
        return output
        # parsed_output = json.loads(output)
        # print(parsed_output)
        # print('\n\n\n\n\n\n\n\n\n\n\n\n')
        # return parsed_output['twitter_shares']
    
def index() -> pc.Component:
    return pc.vstack(
        pc.hstack(
            pc.upload(
                pc.button(
                    "Select File",
                    bg="white",
                    border="1px solid black",
                ),
                padding='20px',
                accept={'text/csv': ['.csv']},
                multiple=False,
                max_files=1
            ),
            pc.button(
                "Upload",
                on_click=lambda: State.handle_upload(
                    pc.upload_files(),
                ),
            ),
        ),
        pc.form(
            pc.vstack(
                pc.heading("Your Input Content"),
                pc.text_area(placeholder="Your content", id="content"),
                pc.hstack(
                    pc.vstack(
                        pc.heading("Website Headline"),
                        pc.hstack(
                            pc.input(default_value="80", placeholder="Character Limit", id="headline_char_limit"),
                            pc.input(default_value="20", placeholder="# of Examples", id="headline_examples"),
                        ),
                        pc.text_area(placeholder="Type the headlines you like. Separate them by pressing enter!", id="liked_headlines"),
                    ),    
                    pc.vstack(
                        pc.heading("Homepage Excerpt"),
                        pc.hstack(
                            pc.input(default_value="300", placeholder="Character Limit", id="homepage_excerpt_char_limit"),
                            pc.input(default_value="4", placeholder="# of Examples", id="homepage_excerpt_examples"),
                        ),
                        pc.text_area(placeholder="Type the excerpts you like. Separate them by pressing enter!", id="liked_homepage_excerpts"),
                    ),    
                    pc.vstack(
                        pc.heading("Website Subtitle"),
                        pc.hstack(
                            pc.input(default_value="150", placeholder="Character Limit", id="subtitle_char_limit"),
                            pc.input(default_value="4", placeholder="# of Examples", id="subtitle_examples"),
                        ),
                        pc.text_area(placeholder="Type the subtitles you like. Separate them by pressing enter!", id="liked_subtitles"),
                    ),    
                ),
                pc.hstack(
                    pc.vstack(
                        pc.heading("SEO Headline"),
                        pc.hstack(
                            pc.input(default_value="50", placeholder="Character Limit", id="seo_headline_char_limit"),
                            pc.input(default_value="4", placeholder="# of Examples", id="seo_headline_examples"),
                        )
                    ),
                    pc.vstack(
                        pc.heading("SEO Excerpt"),
                        pc.hstack(
                            pc.input(default_value="155", placeholder="Character Limit", id="seo_excerpt_char_limit"),
                            pc.input(default_value="4", placeholder="# of Examples", id="seo_excerpt_examples"),
                        ),
                    ),
                    pc.vstack(    
                        pc.heading("Newsletter Intro"),
                        pc.hstack(
                            pc.input(default_value="150", placeholder="Character Limit", id="newsletter_intro_char_limit"),
                            pc.input(default_value="3", placeholder="# of Examples", id="newsletter_intro_examples"),
                        ),
                    ),
                    pc.vstack(
                        pc.heading("Twitter Share"),
                        pc.hstack(
                            pc.input(default_value="280", placeholder="Character Limit", id="twitter_share_char_limit"),
                            pc.input(default_value="3", placeholder="# of Examples", id="twitter_share_examples"),
                        ),
                    )
                ),
                pc.button("Submit", type_="submit"),
            ),
            on_submit=State.handle_submit,
            
        ),
        pc.divider(),
        pc.heading("Results"),
        pc.text("Headlines"),
        pc.text(State.website_headline),
        # pc.responsive_grid(
        #     pc.foreach(State.website_headline, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.divider(),
        pc.text("Homepage Excerpts"),
        pc.text(State.homepage_excerpt),
        # pc.responsive_grid(
        #     pc.foreach(State.homepage_excerpt, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.divider(),
        pc.text("Subtitles"),
        pc.text(State.subtitle),
        # pc.responsive_grid(
        #     pc.foreach(State.subtitle, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.divider(),
        pc.text("SEO Headlines"),
        pc.text(State.seo_headline),
        # pc.responsive_grid(
        #     pc.foreach(State.seo_headline, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.divider(),
        pc.text("SEO Excerpts"),
        pc.text(State.seo_excerpt),
        # pc.responsive_grid(
        #     pc.foreach(State.seo_excerpt, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.divider(),
        pc.text("Newsletter Intros"),
        pc.text(State.newsletter_intro),
        # pc.responsive_grid(
        #     pc.foreach(State.newsletter_intro, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        pc.text("Twitter Share Messages"),
        pc.text(State.twitter_share),
        # pc.responsive_grid(
        #     pc.foreach(State.twitter_share, X_display),
        #     columns=[1,2],
        #     padding="15px"
        # ),
        margin="0",
        padding="0px"
    )
    
# def X_display(X: str):
#     # print(headline)
#     return pc.text(
#         X,
#         padding="15px"
#     )

# Add state and page to the app.
app = pc.App(state=State, style=gs.global_style)
app.add_page(index)
app.compile()

