import streamlit as st
from help import health_analysis
from load_chatmodel import load
from data import main_data
from get_medical import get_links
import torch 
from tensorflow.keras.preprocessing.sequence import pad_sequences

encoder_net, decoder_net = load()
data = main_data()
max, vocab_enc, vocab_dec = data.len_all()
tok_enc = data.tok_enc
tok_dec = data.tok_dec

st.title("Animo")
st.write("A Guide To Mental Heath")

html_temp1 = """
<div style="background-color:#000000  ;padding:10px; background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">“Anything that’s human is mentionable, and anything that is mentionable can be more manageable. When we can talk about our feelings, they become less overwhelming, less upsetting, and less scary.” Fred Rogers</h2>
</div>"""
st.markdown(html_temp1, unsafe_allow_html=True)
st.write("")
html_temp2 = """
<div style="background-color:#000000  ;padding:10px; background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
<h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">Animo is the latin translation of mind and noticing the sync where mental health is the well being of one's mind .We bring you a one stop guide to answer all your questions regarding mental health. We aim to provide and connect every individual with the vast expanse of mental health .Enter your queries in the space provided below and we'll be there at your service!!</h2>
</div>"""
st.markdown(html_temp2, unsafe_allow_html=True)


page_bg_img = '''
<style>
body {
background-image: url("https://www.homemaidsimple.com/wp-content/uploads/2018/04/Mental-health-stigma-1.jpg");
background-size: cover;
height: 100vh;
background-position: center;
}
</style>
'''

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

if question:
    question = tok_enc.texts_to_sequences(question)

    seq = torch.tensor(pad_sequences(question, padding='pre',maxlen=100), dtype=torch.long)

    with torch.no_grad():
        hidden, cell = encoder_net(seq)

    outputs = [1]

    for _ in range(100):
        previous_word = torch.LongTensor([outputs[-1]]).to("cpu")

        with torch.no_grad():
            output, hidden, cell = decoder_net(previous_word, hidden, cell)
            best_guess = output.argmax(1).item()

        outputs.append(best_guess)

        # Model predicts it's the end of the sentence
        if output.argmax(1).item() == 2: 
            break

if question:
    question = question.lower()
    sent = [question]
    health_model = health_analysis(sent)
    
    if health_model.recommend():
        html_temp4 = """
        <div style="background-color:#000000  ;padding:10px;  background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
        <h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">From our conversation we would like to recommend for you whats best for your health. We also provide a service which recommends trained mental health experts,counsellors and psychiatrists in your area.")   
        </h2>
        </div>"""
        st.markdown(html_temp4, unsafe_allow_html=True)
        html_temp5 = """
        <div style="background-color:#000000  ;padding:10px;  background:rgba(255,255,255,0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.5)">
        <h2 style="color:black;text-align:center;font-family: "Lucida Console", Courier, monospace;">Please enter your pincode in the box below!!</h2>
        </div>"""
        st.markdown(html_temp5, unsafe_allow_html=True)
        pin = st.text_input("Pin")

        st.write("""Mental Health : is a loaded term. It can trigger a dizzying array of reactions when we hear it. In a country like India where 
        Mental health is probably the next pandemic but the awareness is still very low. Our main objective is to educate the population still oblivious to the issues regarding mental health.""")
        if pin:
            for i in get_links(pin):
                st.write(i)


