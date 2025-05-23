import streamlit as st
import os
import subprocess
import time
# from fragments import sidebarFrag

# Page Config
this_dir = os.path.dirname(__file__)
favicon = os.path.join(this_dir, "assets", "favicon.ico")
logo = os.path.join(this_dir, "assets", "logo.png")
logo_sm = os.path.join(this_dir, "assets", "logo_sm.png")
logo_md = os.path.join(this_dir, "assets", "logo_md.png")
logo_lg = os.path.join(this_dir, "assets", "logo_lg.png")
st.set_page_config(
    page_title="Shakey - Text Inference",
    page_icon=favicon,
    # layout="wide",
)

# state
if "ngrams" not in st.session_state:
    st.session_state.ngrams = 4
if "num_prediction_words" not in st.session_state:
    st.session_state.num_prediction_words = 50
if "context" not in st.session_state:
    st.session_state.context = ""
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "inference_time" not in st.session_state:
    st.session_state.inference_time = ""

def run_inference_model():
    st.session_state.context = st.session_state.context.strip() # ensure it counts words and not whitespace
    # print('context:', st.session_state.context.split(), "length:", len(st.session_state.context.split()))
    # print('ngrams:', st.session_state.ngrams, "length:", len(str(st.session_state.ngrams)))
    if not st.session_state.context:
        st.warning("Please enter some text in the context box.")
    elif len(st.session_state.context.split()) < st.session_state.ngrams - 1:
        st.warning(f"Please enter a context of at least {st.session_state.ngrams - 1} characters.")
    else:
        st.session_state.context = st.session_state.context
        st.session_state.ngrams = st.session_state.ngrams
        st.session_state.num_prediction_words = st.session_state.num_prediction_words

            
        # f'## Context: `{st.session_state.context}`'
        # f'## N-Grams: `{st.session_state.ngrams}`'
        # f'## Prediction Words: `{st.session_state.num_prediction_words}`'

        ### Run the model
        # path: ../add_new_corpus.sh
        # run the model
        # fix: relative path
        script_path = os.path.join(this_dir, "../scripts/query.sh")
        command = [
            "bash",
            script_path,
            str(st.session_state.ngrams),
            str(st.session_state.num_prediction_words),
            st.session_state.context
        ]
        with st.spinner("Generating...", show_time=True):
            try:
                # Run the shell command and capture the output
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                output = result.stdout.strip("")  # Get the standard output
                # get the time (the first line of the output)
                time_taken = output.split("\n")[0]
                output = output.split("\n")[1:]  # Get the rest of the output
                output = "\n".join(output)  # Join the rest of the output
                st.text_area(
                    "generated_text",
                    value = st.write_stream(stream_data(time_taken, output)),
                    height=300,
                    on_change=None,
                    args=None,
                )
                st.session_state.generated_text = output
                st.session_state.inference_time = time_taken
                st.rerun()
                # st.write_stream(stream_data(time_taken, output))
                # st.markdown(f"### Time taken: {time_taken}")
                # st.markdown(f"### Generated Text:\n{output}")
            except subprocess.CalledProcessError as e:
                st.error(f"Error running the query script: {e.stderr}")

def on_text_change():
    pass

def stream_data(time_taken, output):
    for letter in time_taken:
        yield letter
        time.sleep(0.02)
    yield "\n"
    time.sleep(0.03)
    for word in output.split(" "):
        yield word + " "
        time.sleep(0.02)

def ngrams_segmented_control():
    ngrams = {
            2: "bigram",
            3: "3-gram",
            4: "4-gram",
            5: "5-gram",
            6: "6-gram",
            7: "7-gram",
        }
    
    st.session_state.ngrams = st.segmented_control(
            "ngrams",
            options=ngrams.keys(),
            format_func=lambda x: ngrams[x],
            default=4,
            selection_mode="single",
            label_visibility="hidden",
        )

# sidebar
def sidebar():
    with st.sidebar:
        st.logo(logo_lg, size="large", icon_image=logo, link=None)

        "# Text Inference Settings ⛭"
        st.divider()

        "## N-Grams"

        ngrams_segmented_control()

        "## Prediction Words"

        st.session_state.num_prediction_words = st.slider(
            "num_prediction_words",
            1,
            100,
            50,
            label_visibility="hidden",
        )
        st.divider()
        st.page_link("evalMetrics.py", label="Evaluation Metrics", icon="📊")


sidebar()

# main
"# Shakespearean Text Inference"
f"N-gram: `{st.session_state.ngrams}-gram`"
f"num prediction words: `{st.session_state.num_prediction_words}`"


st.session_state.context = st.text_area(
    "context",
    height=300,
    on_change=on_text_change(),
    args=None,
    placeholder="Enter text...",
    label_visibility="hidden",
    value = st.session_state.generated_text,
)

left, middle, right = st.columns(3)


if middle.button("Generate", use_container_width=True):
    run_inference_model()

if st.session_state.inference_time:
    right.markdown(
        f"`Inference Time: {st.session_state.inference_time}s`",
    )