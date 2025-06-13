import gradio as gr
import pandas as pd
import requests
import io

# Connect to your FastAPI backend
def run_inference(file):
    try:
        with open(file.name, "rb") as f:
            files = {'file': (file.name, f, 'text/csv')}
            response = requests.post("http://127.0.0.1:8000/inference/run", files=files)

        data = response.json()
        print("API returned data:", data)  # 👈 Debug print

        if response.status_code != 200:
            return "❌ Error: " + data.get("error", "Unknown error"), None

        rows = data.get("rows_received", [])
        
        # If the backend returns a string instead of list
        if isinstance(rows, str):
            try:
                rows = json.loads(rows)
            except Exception:
                return "❌ Cannot parse backend output.", None

        if not isinstance(rows, list):
            return "❌ Invalid data format received from backend.", None

        df = pd.DataFrame(rows)
        return "✅ Inference successful!", df

    except Exception as e:
        return f"❌ Exception occurred: {str(e)}", None

def download_result(df):
    return df.to_csv(index=False)

with gr.Blocks(title="📊 Inference System") as demo:
    gr.Markdown("## 🔍 Upload a CSV File for Inference")
    
    file_input = gr.File(label="📁 Upload CSV", file_types=[".csv"])
    run_button = gr.Button("🚀 Run Inference")
    message = gr.Textbox(label="Status", interactive=False)
    result_table = gr.Dataframe(label="📋 Result Table", visible=False)
    download_button = gr.Button("⬇️ Download CSV", visible=False)
    csv_output = gr.File(label="📥 Download File", visible=False)

    def inference_pipeline(file):
        msg, df = run_inference(file)
        if isinstance(df, pd.DataFrame):
            return msg, gr.update(value=df, visible=True), gr.update(visible=True), gr.update(value=io.StringIO(df.to_csv(index=False)), visible=True)
        else:
            return msg, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    run_button.click(inference_pipeline, inputs=[file_input], outputs=[message, result_table, download_button, csv_output])

demo.launch()
