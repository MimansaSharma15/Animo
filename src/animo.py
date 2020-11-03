import streamlit as st

st.title("Animo")
st.write("A Guide To Mental Heath")

html_temp1 = """
<div style="background-color:#000000  ;padding:10px; background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">“Anything that’s human is mentionable, and anything that is mentionable can be more manageable. When we can talk about our feelings, they become less overwhelming, less upsetting, and less scary.” Fred Rogers</h2>
</div>"""
st.markdown(html_temp1, unsafe_allow_html=True)
st.write("")
html_temp2 = """


st.markdown(page_bg_img, unsafe_allow_html=True)


html_temp3 = """
<div style="background-color:#000000  ;padding:10px; background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5) ">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">Let's Talk</h2>
</div>"""
st.markdown(html_temp3, unsafe_allow_html=True)
st.write("")
st.write("Ask as many questions as you want and without the fear of judgement. We are hear for you clear any doubts you have about your health.")

st.write("Note: Enter your question in brief!!")
st.write("")
question = st.text_input("Question")

html_temp4 = """
<div style="background-color:#000000  ;padding:10px;  background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">From our conversation we would like to recommend for you whats best for your health. We also provide a service which recommends trained mental health experts,counsellors and psychiatrists in your area.")   
</h2>
</div>"""
st.markdown(html_temp4, unsafe_allow_html=True)

html_temp5 = """
<div style="background-color:#000000  ;padding:5px;  background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">Please enter your pincode in the box below!!</h2>
</div>"""
st.markdown(html_temp5, unsafe_allow_html=True)
st.write("")
pin = st.text_input("Pin")

st.write("""Mental Health : is a loaded term. It can trigger a dizzying array of reactions when we hear it. In a country like India where 
Mental health is probably the next pandemic but the awareness is still very low. Our main objective is to educate the population still oblivious to the issues regarding mental health.""")

