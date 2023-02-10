import json
import streamlit as st
import pandas as pd
#from samp import freight
import time
import os
from datetime import datetime
from dateutil.tz import gettz

if 'form_sample' not in st.session_state:
    st.session_state['form_sample'] = list()



class freight:
    def __init__(self) -> None:
        self.data = list()
        self.temp_ = dict()

    def entry(self,field_name,
                data_type,character_to_be_removed,
                split,hierarchy,
                hierarchy_threshold) -> None:

        temp_ = dict()
        temp_["field_name"] = field_name
        temp_["character_to_be_removed"] = character_to_be_removed
        temp_["split"] =  split
        temp_["hierarchy"] = hierarchy
        temp_["hierarchy_threshold"] = hierarchy_threshold
        temp_["data_type"] = data_type
        self.temp_ = temp_
   
    def next(self):
        self.data.append(self.temp_)
        self.temp_ = dict()
        return self.data

    def export(self,data) -> dict:
        return {"postprocessing":data}


def freight_instance():
    data_instance = freight()
    return data_instance

# def conv(freight_detail):
#     jsonStr = json.dumps(freight_detail.dict)
#     print(jsonStr)
#     return jsonStr

name = 'freight.csv'

df = pd.read_csv(name, error_bad_lines=False)

def download1(data):
    res = [{'Freight Details':data}]
    df.loc[len(df.index)] = list(res[0].values())
    df.to_csv(name, index=False)
    return "Done"



with st.form("my_form", clear_on_submit=True):
    st.write("Inside the form")
    field_name = st.selectbox('Field_name', ('Invoice_number','consignee_zip','payment_type'))
    character_to_be_removed = st.text_input('Enter the list of characters to be removed with comma seperation')
    #character_to_be_removed = list(character_to_be_removed.split(','))
    split = st.text_input('Enter the character to be split and the portion (Eg. [/,1] -> / - to be split and return the 1 part)')
    #split = list(split.split(','))
    hierarchy = st.selectbox('Select Hierarchy',("Layout","Table","duckling"))
    hierarchy_threshold = st.text_input('Enter Threshold')
    #hierarchy_threshold = list(hierarchy_threshold.split(','))
    data_type = st.radio('Select Datatype', ('string','Bool', 'Int', 'float', 'Regex'))
    col1, col2, col3,col4, col5 = st.columns(5)
    with col1:
        next_button_state = st.form_submit_button(label='Next')
    with col5:
        export_button_state = st.form_submit_button(label='Done')


global data_instance
if next_button_state or export_button_state:
    data_instance = freight_instance()
    if not character_to_be_removed:
        st.error("Select Character to be removed is required")
    elif not split:
        st.error("Enter split is required")
    elif not hierarchy_threshold:
        st.error("Enter Threshold is required")
    elif next_button_state and not export_button_state:
        character_to_be_removed = list(character_to_be_removed.split(','))
        split = list(split.split(','))
        hierarchy_threshold = list(hierarchy_threshold.split(','))
        data_instance.entry(field_name,character_to_be_removed,split,hierarchy,hierarchy_threshold,data_type)
        content = data_instance.next()
        st.session_state['form_sample'].append(content)
        next_button_state = False
    elif export_button_state:
        character_to_be_removed = list(character_to_be_removed.split(','))
        split = list(split.split(','))
        hierarchy_threshold = list(hierarchy_threshold.split(','))
        data_instance.entry(field_name,character_to_be_removed,split,hierarchy,hierarchy_threshold,data_type)
        content = data_instance.next()
        st.session_state['form_sample'].append(content)
        data = data_instance.export(st.session_state["form_sample"])
        print("sess:",st.session_state["form_sample"])
        st.json(data)
        res = download1(data)
        next_button_state = False
        export_button_state = False
        st.session_state['form_sample'] = list()