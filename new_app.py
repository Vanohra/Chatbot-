from tkinter import *
from tkinter import simpledialog
from tkinter import font 
import time 
import random 
import requests 
import json 
import re 


FONT = 'Helvetica 14'
FONT_BOLD = 'Helvetica 13 bold' 
TEXT_COLOR = '#1E1E1E'
BG_GRAY  = 'lavenderblush1'
BG_COLOR =  '#C1CDC1'
BG_STRIP = "#FFE6EE"

class ChatApplication(): 
    def __init__(self): 
        self.window = Tk()
        self._setup_main_window()

    def run(self): 
        self.window.mainloop()

    def _setup_main_window(self): 
        self.window.title("Vanohra's Chatbot <3")
        self.window.resizable(width= False, height= False)
        self.window.configure(width=1000, height= 550, bg = BG_COLOR)

        # Creating head label 
        head_label = Label(self.window, bg = BG_COLOR, fg = TEXT_COLOR, text= 'Welcome to the Chatbot', 
        font = FONT_BOLD, pady = 10)
        head_label.place(relwidth= 1)

        line = Label(self.window, width = 450, bg = BG_GRAY)
        line.place(relwidth=1,rely = 0.07, relheight=0.012)

        # Text widget
        self.text_widget = Text(self.window, width = 20, height = 2, bg = BG_COLOR, fg = TEXT_COLOR, font = FONT, padx = 5, pady = 8)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.175, relx=-0.0001)
        self.text_widget.configure(cursor='arrow', state= DISABLED)
        
        search_label = Label(self.window, bg=BG_STRIP, fg=TEXT_COLOR, text="Type SEARCH: [Query] to look something up!", font=('Cascadia Mono', 10), pady=5)
        search_label.place(x=500, rely=.11, anchor="center", relwidth=1, relheight=0.03,)

        # Bottom label 
        bottom_label = Label(self.window, bg = BG_GRAY, height = 80)
        bottom_label.place(relwidth=1, rely = 0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg= 'lavenderblush1', fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        msg2 = f"{'Chatty'}: {conversation(msg)}\n\n" 
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)


def conversation(request): 
    greetings = [ "Hi!", "Hi", "hi", "Sup", "sup", "Hello", "hello" "Hello there", "Howdy", 
                 "hey", "yo"]
    greet_backs = ["Hello !", "Hi!", "Hey!"]
    day_asks =  [ "How are you", " how have you been", "Hru?", "what's up", "How's your day going"]
    day_responses = ["Doing great, thank you", " I'm well, thank you"]
    goodbyes = ["Bye!", "Peace out","Take care", "see you"]
    gratitudes = ["Thank you so much", "Thank you!", "Thx", "ty", "tysm"]
    youre_welcome = ["Of course", "My pleasure !", "You're welcome", "You're very welcome", "Any time"]

    request = request.capitalize()
    request_list = request.split(" ")
    for x in request_list:
        x.capitalize()
        
    if request_list[0].capitalize() in greetings:
        pick = random.randint(0, len(greet_backs) - 1)
        return greet_backs[pick]

    elif request in day_asks:
        for x in day_asks:
            if (x in request_list[0]) and (x=="Hru"):
                pick = random.randint(0, len(day_responses) - 1)
                return day_responses[pick]
            
            elif (x in request):
                pick = random.randint(0, len(day_responses) - 1)
                return day_responses[pick]
            
    elif "your day" in request:
                pick = random.randint(0, len(day_responses) - 1)
                return day_responses[pick]
      
    elif request_list[0].capitalize() in goodbyes:
        pick = random.randint(0, len(goodbyes) - 1)
        return goodbyes[pick]
    
    elif request_list[0].capitalize() in gratitudes:
        pick = random.randint(0, len(youre_welcome) - 1)
        return youre_welcome[pick]

    elif request_list[0].capitalize() == "RATE":
        if 1 <= int(request_list[1]) <= 5:
            mood_dict = {
            1: " I'm sorry about that.",
            2: "Hm, your day could have been better. ",
            3: f"Seems that your day was okay! Could have been worse. ",
            4: "Yay, you had a good day! ",
            5: f"Wow, your day was awesome! "}

            return mood_dict[int(request_list[1])]
        else:
            return "Invalid rating. Please provide a rating from 1 to 5."
        
    elif request_list[0].upper() == "SEARCH:": 
        del request_list[0]
        new_request = " ".join(request_list)

        language_code = 'en'
        search_query = new_request 
        number_of_results = 1
        headers = {
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'User-Agent': 'YOUR_APP_NAME (APaskulin_(WMF))'
            }

        base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
        endpoint = '/search/page'
        url = base_url + language_code + endpoint
        parameters = {'q': search_query, 'limit': number_of_results}
        response = requests.get(url, headers=headers, params=parameters)

        response = json.loads(response.text)
        output = []

        for page in response['pages']:
            display_title = page['title']
            article_url = 'https://' + language_code + '.wikipedia.org/wiki/' + page['key']
            try:
                article_description = page['description']
            except:
                article_description = 'a Wikipedia article'
            try:
                thumbnail_url = 'https:' + page['thumbnail']['url']
            except:
                thumbnail_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png'  
            excerpt_text = page["excerpt"]
    
            excerpt_text_no_tags = re.sub('<span.*?>|&.*;|</span>', '', excerpt_text)
            description_text = page['description']
            return f"""\nHm... 
            \nExcerpt: {excerpt_text_no_tags}
            \nDescription: {description_text}
            \nArticle URL: {article_url}"""
        
    else: 
        dont_know = [f"...I've got nothing.", "I'm not sure what you mean.", "Erm...? ", "I'm not sure what you're asking.", "I don't get it"]
        pick = random.randint(0, len(dont_know) - 1)
        return dont_know[pick]
        
 

app = ChatApplication()
app.run()



