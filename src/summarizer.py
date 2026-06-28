from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(text):

    if len(text) < 100:
        return "Text is too short to summarize."

    result = summarizer(
        text[:1000],
        max_length=80,
        min_length=20,
        do_sample=False
    )

    return result[0]["summary_text"]