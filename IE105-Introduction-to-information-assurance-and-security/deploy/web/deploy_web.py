import gradio as gr
import joblib
import numpy as np

def make_prediction(string_input):
    loaded_model = joblib.load('DT_UNSW_NB15.joblib')
    string_input=string_input.split(",")
    string_input=np.array(string_input)
    y_pred = loaded_model.predict(string_input.reshape(1, -1))
    print(y_pred)
    print(type(string_input))
    print(type(string_input[1]))
    return "IP: 59.166.0.6 Port: 8569 " + "Warning!!!!! Attacked: " + str(y_pred[0])

string_input = gr.Textbox(label = "Enter Data String to Detect")
# We create the output
output = gr.Textbox()

app = gr.Interface(fn = make_prediction, inputs=[string_input], outputs=output).launch()