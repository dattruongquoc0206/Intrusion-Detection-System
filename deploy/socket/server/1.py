import gradio as gr
import pickle
import joblib
import numpy as np

def make_prediction(string_input):
    loaded_model = joblib.load('dt_model.sav')
    string_input=string_input.split(",")
    string_input=np.array(string_input)
    y_pred = loaded_model.predict(string_input.reshape(1, -1))
    print(y_pred)
    print(type(string_input))
    print(type(string_input[1]))
    return y_pred

string_input = gr.Textbox(label = "Enter String")
# We create the output
output = gr.Textbox()

app = gr.Interface(fn = make_prediction, inputs=[string_input], outputs=output)
app.launch()