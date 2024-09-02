import time
import streamlit as st
import boto3
import requests
import streamlit.components.v1 as components
# from streamlit_navigation_bar import st_navbar
from util import Constant

mycode = "<script>alert('Your session has timed out! Click OK to restart your session')</script>"

# import subprocess
s3 =  boto3.client("s3")
cimplify = "https://z4af6u028e.execute-api.us-east-1.amazonaws.com/v1"
# cimplify =  "http://127.0.0.1:5000"

# st.set_option('server.runOnSave', False)
# Function to set cookies in requests
def set_cookies(cookies):
    session = requests.Session()
    session.cookies.set("session", cookies)
    return session

# Function to get cookies from response
def get_cookies(response):
    cookies = {}
    for cookie in response.cookies:
        cookies[cookie.name] = cookie.value
    return cookies

# def iterateMessage():
    # for message in st.session_state.messages:
    #     if message["role"] == "user":
    #        messages.chat_message("user").write(message["content"])
    #     elif message["role"] == "assistant":
    #         messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write(message["content"])

# send a file and prompt
def v1(prompt):
    data = {'message': prompt }
    url = f"{cimplify}/ai-demo/qAndA"
    headers = {"Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{st.session_state.get('session_id')}" }
    
    # session = st.session_state.cookies
    res = st.session_state["api"].post(url,
                    json=data, headers=headers).json()
    return res["message"]
 
def exitingFile(path):
    data = {'s3Path': path }
    url = f"{cimplify}/ai-demo/exiting-file-loaded"
    headers = {"Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{st.session_state.get('session_id')}" }
    
    # session = st.session_state.cookies
    res = st.session_state["api"].post(url,
                    json=data, headers=headers)
    return res

def fileUpload(file):
    url = f"{cimplify}/ai-demo/qAndA-file-upload"
    headers = {"Content-Type": "application/pdf",
            "Authorization": f"{st.session_state.get('session_id')}" }
    res = st.session_state["api"].post(url,
                    data=file, headers=headers)
    return res
def get_session_id():
    st.session_state["api"] =  requests.Session()
    response = st.session_state["api"].get(f"{cimplify}/ai-demo/get-session-id")
    # print("+========================",response)
    return response.json().get('session_id')

def chips(type, option): 
    options = ["chipsBut1", "chipsBut2", "chipsBut3"]
    if type == "Indian food":
        st.session_state["chipsValues"] = Constant.chipsQuestion[type][option]
    elif type == "Predict Customer Purchase Behavior":
        st.session_state["chipsValues"] = Constant.chipsQuestion[type][option]
    else:
        st.session_state["chipsValues"] = Constant.chipsQuestion[type][option]
    st.session_state[options[option]] = True
    st.session_state["chipsBoolean"] = True
    


# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state["uptoTime"] = time.time() + 300 #seconds 300s
    st.session_state["session_id"] = get_session_id()
    st.session_state["option"] = True
    st.session_state["fileUploaded"]=True
    st.session_state["temp"] = ""
    st.session_state["data"] = ""
    st.session_state["chipsValues"] = ""
    st.session_state["chipsBoolean"] = False
    st.session_state["chipsBut1"] = False
    st.session_state["chipsBut2"] = False
    st.session_state["chipsBut3"] = False
    # st.session_state["api"] =  requests.Session()

# Store cookies in session state
if 'cookies' not in st.session_state:
    st.session_state.cookies = set_cookies(st.session_state["session_id"])

print(st.session_state.get("session_id"))

# Define your custom CSS
custom_css = """
<style>
    .container {
        background-color: #2A2F3A;  /* Secondary background color */
        padding: 20px;
        border-radius: 10px;
    }

    @media (max-width: 50.5rem) {
    .st-emotion-cache-1eo1tir {
        max-width: fit-content;
    }
}
}
</style>
"""

# Inject the CSS into the Streamlit app
# st.markdown(css, unsafe_allow_html=True)
# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image(image="./Cimplify.AI Logo Header.svg")

with col3:
    st.write(' ')

def exitingFileSelect(option):
    st.session_state.fileUploaded = False
    if time.time() < st.session_state["uptoTime"]:
        for i in option:
            print(st.session_state["temp"] , i)
            if i != st.session_state["temp"]:
                st.session_state["temp"] = i
                st.session_state["data"] = exitingFile(pathDict[i])
                st.session_state["chipsBut1"] = False
                st.session_state["chipsBut2"] = False
                st.session_state["chipsBut3"] = False
                st.session_state.messages = []
        if st.session_state["data"] :
            messages = st.container(height=300)
            if len(option) != 0:
                messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write_stream( ["I am Cimba. I'm ready to answer questions about " + option[0] +".  a *"+fieldName[option[0]]+"* to get started"])
            
            chipCol1, chipCol2, chipCol3 = st.columns(3)

            with chipCol1:
                if  st.session_state["chipsBut1"] == False:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][0],on_click=lambda: chips(st.session_state["temp"],0))
                else:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][0],on_click=lambda: chips(st.session_state["temp"],0), disabled=True)
            with chipCol2:
                if  st.session_state["chipsBut2"] == False:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][1],on_click=lambda: chips(st.session_state["temp"],1))
                else:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][1],on_click=lambda: chips(st.session_state["temp"],1), disabled=True)
            with chipCol3:
                if  st.session_state["chipsBut3"] == False:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][2],on_click=lambda: chips(st.session_state["temp"],2))
                else:
                    st.button(Constant.chipsQuestion[st.session_state["temp"]][2],on_click=lambda: chips(st.session_state["temp"],2), disabled=True)
        
                # Create a chat input field
            prompt = st.chat_input("Message Cimba")
            if prompt or st.session_state["chipsBoolean"]:
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        messages.chat_message("user").write(message["content"])
                    elif message["role"] == "assistant":
                        messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write(message["content"])
                if st.session_state["chipsBoolean"] == True:
                    st.session_state["chipsBoolean"] = False
                    prompt = st.session_state["chipsValues"]
                messages.chat_message("user").write(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                res = v1(prompt)
                # obj = s3.get_object(Bucket="ai-demo-projects", Key="audio/f1af57d8-90d1-4088-a437-dde94095fa3b/07e4edd9-06ca-49f5-afca-763536b0de11.mp3")
            
                # st.audio(, format="audio/ogg")
                # b64 = base64.b64encode(obj['Body'].read()).decode()
                # md = f"""
                #             <audio controls autoplay="true">
                #             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                #             </audio>
                #             """
                # st.markdown(
                #     md,
                #     unsafe_allow_html=True,
                # )
                messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write_stream([res])
                # messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").audio(st.markdown(
                #     md,
                #     unsafe_allow_html=True,
                # ))
                # While processing
                st.session_state.messages.append({"role" : "assistant", "content" :res })
    else:
        st.session_state.clear()
        components.html(mycode, height=0, width=0)
        st.rerun()


def userFileUpload(fileUploaded):
    st.session_state.option = False
    if time.time() < st.session_state["uptoTime"]:
        if (fileUploaded):
            st.session_state["data"] = fileUpload(fileUploaded.read())
            st.session_state.messages = []
            print(st.session_state["data"])
            if st.session_state["data"] :
                messages = st.container(height=300)
                messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write_stream( ["I am Cimba. I'm ready to answer questions about to get started"])
                # Create a chat input field
                prompt = st.chat_input("Message Cimba")
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        messages.chat_message("user").write(message["content"])
                    elif message["role"] == "assistant":
                        messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write(message["content"])
                if prompt:
                    iterateMessage()
                    messages.chat_message("user").write(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    res = v1(prompt)
                    messages.chat_message("assistant", avatar="./Cimplify Cube Logo.png").write_stream([res])
                
                    st.session_state.messages.append({"role" : "assistant", "content" :res })
    else:
        st.session_state.clear()
        components.html(mycode, height=0, width=0)
        st.rerun()

# Using object notation
section  = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("home","v1", "v2"),
    index=list(Constant.sections.values()).index("home")
)
selected_slug = Constant.sections[section]

# Update the URL with the selected section
if st.session_state.get("section") != selected_slug:
    st.session_state.section = selected_slug
    st.query_params.section=selected_slug

if st.session_state.section == "home":
    print(st.session_state.option)
    pathDict = {
        "Indian food" : "files/indian_food.csv",
        "Predict Customer Purchase Behavior" : "files/customer_purchase_data.csv",
        "Genral Election":"files/GE_2024_Results.csv"
    }
    fieldName = {
        "Indian food" : "idly, puri",
        "Predict Customer Purchase Behavior" : "Age, Gender, Annual Income, Number of Purchases, Product Category",
        "Genral Election": "state, candidate, result, party"
    }
   
    if st.session_state.option:
        st.title("Engage in a Q&A with a Dataset")
        st.text("Existing Dataset")

        option = st.multiselect("Select an option", ["Indian food", "Predict Customer Purchase Behavior", "Genral Election"], max_selections=1)
        if option:
            exitingFileSelect(option)

    if st.session_state.fileUploaded:
        st.text("with your Dataset")
        with st.spinner('Wait for it...'):
            fileUploaded = st.file_uploader(
            "Choose a file", type="pdf")
            if fileUploaded:
                userFileUpload(fileUploaded)

elif st.session_state.section == "v1":
    st.title('Q & A with a Dataset')
        

    pathDict = {
        "Indian food" : "files/indian_food.csv",
        "Predict Customer Purchase Behavior" : "files/customer_purchase_data.csv",
        "Genral Election":"files/GE_2024_Results.csv"
    }
    fieldName = {
        "Indian food" : "idly, puri",
        "Predict Customer Purchase Behavior" : "Age, Gender, Annual Income, Number of Purchases, Product Category",
        "Genral Election": "state, candidate, result, party"
    }

    with st.spinner('Wait for it...'):
        option = st.multiselect("Select an option", ["Indian food", "Predict Customer Purchase Behavior", "Genral Election"], max_selections=1)
        exitingFileSelect(option)
elif  st.session_state.section == "v2":
    st.title('Q and A with your dataset')    
    st.caption("powered by cimplify")
    with st.spinner('Wait for it...'):
        fileUploaded= st.file_uploader(
    "Choose a file", type="pdf")
       