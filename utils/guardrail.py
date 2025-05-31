from openai import OpenAI

client = OpenAI()

def moderate_text(text):
    """Check if the text violates OpenAI's moderation policy."""
    response = client.moderations.create(input=text)
    flagged = response.results[0].flagged
    categories = response.results[0].categories
    return flagged, categories

def check_quality(text, min_length=200, max_length=1000):
    """Ensure content is within acceptable length bounds."""
    if not text or len(text.strip()) < min_length:
        return False, "Too short"
    if len(text.strip()) > max_length:
        return False, "Too long"
    return True, ""
