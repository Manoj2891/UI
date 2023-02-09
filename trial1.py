import json
import streamlit as st

class freight:
    field_name = 'Invoice_Number'
    data_type = 'string'
    character_to_be_removed = '-'
    split =  "-"
    hierarchy = "Layout"
    hierarchy_thresholf = 'threshold'
	
freight_detail = freight()

def conv(freight_detail):
    jsonStr = json.dumps(freight_detail.__dict__)
    print(jsonStr)
    return jsonStr


def main():
    #form = st.form("my_form",  clear_on_submit=True)
    # Now add a submit button to the form:
    st.title("JSON_Config")
    freight_detail.field_name = st.text_input('Field_name', 'Enter Detail')
    freight_detail.data_type = st.selectbox('Select Datatype', ('string','Bool', 'Int', 'float', 'Regex'))
    freight_detail.character_to_be_removed = st.multiselect('Select Character to be removed', ["-","/","Invoice No", ""])
    freight_detail.split = st.multiselect('Select split', ["-",1])
    freight_detail.hierarchy = st.selectbox('Select Hierarchy',("Layout","Table","duckling"))
    freight_detail.hierarchy_thresholf = st.number_input('Enter Threshold')
    #form_check = check(freight_detail)
    if [] not in (freight_detail.field_name, freight_detail.character_to_be_removed, freight_detail.data_type, freight_detail.hierarchy,freight_detail.hierarchy_thresholf, freight_detail.split):
        if st.button(label='Next'):
        # if submitted == "Next":
            print(freight_detail.hierarchy_thresholf) 
            json_output = conv(freight_detail)
            st.success('The output is {}'.format(json_output))
    else:
        st.info('Enter all the fields', icon="ℹ️")

if __name__=='__main__':
    main()
