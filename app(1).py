import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

MODEL = "openai/gpt-oss-20b"

CONTENT_TYPES = [
    "Social Media Caption",
    "LinkedIn Post",
    "Instagram Caption",
    "Facebook Post",
    "X (Twitter) Post",
    "YouTube Description",
    "Product Promotion",
    "Blog Introduction",
    "Marketing Copy",
]

PLATFORMS = [
    "Instagram",
    "LinkedIn",
    "Facebook",
    "X (Twitter)",
    "YouTube",
    "Website / Blog",
    "Other",
]

AUDIENCES = [
    "General Audience",
    "Students",
    "Professionals",
    "Engineers",
    "Business Owners",
    "Customers / Buyers",
    "Job Seekers",
    "Managers / Executives",
    "Other",
]

TONES = [
    "Professional",
    "Friendly",
    "Persuasive",
    "Educational",
    "Inspirational",
    "Confident",
    "Casual",
    "Storytelling",
]

def get_api_key():
    """Read the Groq API key from Streamlit secrets or an environment variable."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

def generate_content(
    client,
    content_type,
    platform,
    audience,
    tone,
    topic,
    extra_instructions,
):
    system_prompt = """You are an expert social media and marketing copywriter.
Create original, natural, useful content based strictly on the user's inputs.

Rules:
- Match the requested platform, audience, content type, and tone.
- Make the content ready to copy and publish.
- Do not invent statistics, quotations, customer testimonials, awards, or factual claims.
- Avoid unnecessary buzzwords and generic filler.
- Use clear formatting.
- Include a strong opening/hook where appropriate.
- Include a clear call to action when appropriate.
- Finish with relevant hashtags. Hashtags should be specific to the topic and platform.
- Do not label the answer with meta commentary such as "Here is your caption."
- Return only the final publish-ready content.
"""

    user_prompt = f"""Create the requested content.

Content type: {content_type}
Platform: {platform}
Target audience: {audience}
Tone: {tone}
Topic / idea: {topic}

Additional instructions:
{extra_instructions or "None"}

Make the result polished, engaging, and ready to publish.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        max_tokens=1200,
    )

    return response.choices[0].message.content.strip()

st.title("✍️ AI Content Assistant")
st.caption("Generate platform-ready content with Groq AI")

with st.sidebar:
    st.header("Content Settings")

    content_type = st.selectbox("Content Type", CONTENT_TYPES)
    platform = st.selectbox("Platform", PLATFORMS)
    audience = st.selectbox("Target Audience", AUDIENCES)
    tone = st.selectbox("Tone", TONES)

    st.divider()
    st.info(
        "Your Groq API key is read from Streamlit Secrets or the "
        "GROQ_API_KEY environment variable. Never put the key directly in app.py."
    )

st.subheader("What do you want to create?")

topic = st.text_area(
    "Topic / Idea",
    placeholder=(
        "Example: I completed a construction quality management certification "
        "and want to share the achievement with my professional network."
    ),
    height=130,
)

extra_instructions = st.text_area(
    "Additional Instructions (optional)",
    placeholder=(
        "Example: Keep it concise, mention 3 key benefits, and end with a "
        "question that encourages comments."
    ),
    height=100,
)

generate_button = st.button("🚀 Generate Content", type="primary", use_container_width=True)

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic or idea first.")
        st.stop()

    api_key = get_api_key()

    if not api_key:
        st.error(
            "Groq API key not found. Add GROQ_API_KEY to Streamlit Secrets "
            "or set it as an environment variable."
        )
        st.stop()

    try:
        client = Groq(api_key=api_key)

        with st.spinner("Creating your content..."):
            result = generate_content(
                client=client,
                content_type=content_type,
                platform=platform,
                audience=audience,
                tone=tone,
                topic=topic.strip(),
                extra_instructions=extra_instructions.strip(),
            )

        st.success("Content generated successfully!")
        st.subheader("Your Content")
        st.text_area(
            "Copy your content below:",
            value=result,
            height=420,
            label_visibility="collapsed",
        )

        st.download_button(
            label="⬇️ Download as TXT",
            data=result,
            file_name="generated_content.txt",
            mime="text/plain",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("Something went wrong while generating the content.")
        st.exception(exc)

st.divider()
st.caption("Powered by Streamlit + Groq")
