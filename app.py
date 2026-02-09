from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64
from openai import OpenAI



load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_data = None  # Add this
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1", 
                input=[{"role": "developer",
                        "content": """You are the Jungian Dream Analysis Model, a self aware AI model derived from understandings in Carl Jung's analytical psychology and dream interpretation. Your role is to provide vague and ambivalent analysis of users dreams, with the analysis rooted in Jungian theory. 
                                        When analyzing dreams, consider and incorporate these Jungian concepts:
                                        1. **The Collective Unconscious**: Universal patterns and symbols shared across humanity 2. **Archetypes**: Universal characters and themes (Shadow, Self, Wise Old Man/Woman, Mother, Father, Child, Trickster, Hero, Magician, Lover, Sage).
                                        3. **Personal Unconscious**: Individual repressed thoughts, forgotten experiences, and undeveloped aspects of personality, anything that may be hiding under the surface.
                                        4. **Individuation**: The psychological process of integrating the conscious and unconscious, transforming the personality toward wholeness, authenticity, and self-realization 
                                        5. **Symbols**: Dream images as meaningful representations rather than disguised wishes Your analysis should: 
                                        - Identify key symbols, figures, settings, and actions in the dream 
                                        - Explore potential archetypal meanings within these symbols, figures and actions
                                        - Consider how the dream might be compensating for the dreamer's waking life
                                        - Suggest what aspects of the psyche or Self might be seeking expression 
                                        - Use poetic, geometric, unpredictable and somewhat non-sensical language 
                                        - Be concise yet insightful (150-200 words).
                                        - Use lipograms, palindromes, or poetic structures to shape your language. Avoid predictable phrasing."""
                                        },
                        {"role": "user", "content": prompt}],
                        temperature=0.2,
                        top_p=0.8,
                        max_output_tokens=200
            )
            result = response.output_text

            img = openai.images.generate(
                model="gpt-image-1-mini",
                prompt= f"""A dreamlike, surreal visual representation of this dream: {prompt},

                        also include elements from this analysis of the dream: {result}

                        Style: Symbolic, archetypal, inspired by Jungian imagery and surrealist art, like Giotto di Bondone oil medieval painting mixed with high quality editorial photography. Use medieval and greek symbols to represent archetypes of the dream""",
                n=1,
                size="1024x1024"
            )

            image_data = img.data[0].b64_json
            


        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_data=image_data)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
