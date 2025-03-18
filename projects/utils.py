from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from projects.models import Project

nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')

def preprocess_text(text):
    """Clean and preprocess text for better similarity comparison."""
    text = text.lower()
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def calculate_cosine_similarity(new_project_description, existing_projects):
    """
    Compares the new project description against existing projects.
    Args:
        new_project_description (str): The description of the new project.
        existing_projects (QuerySet): A queryset of existing projects to compare against.
    Returns:
        tuple: (highest similarity percentage, most similar project name)
    """
    if not new_project_description:
        raise ValueError("New project description cannot be empty.")

    # Convert QuerySet to a list for consistency
    existing_projects = Project.objects.all()

    if not existing_projects:
        return 0, None  # No projects to compare

    # Preprocess descriptions
    descriptions = [preprocess_text(project.description) for project in existing_projects]
    descriptions.append(preprocess_text(new_project_description))  # Add the new project description

    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    if similarity_scores.size == 0:
        return 0, None  # No similarities found

    max_score = max(similarity_scores)
    most_similar_index = similarity_scores.argmax()

    # Return results
    if most_similar_index >= 0:
        most_similar_project = existing_projects[int(most_similar_index)]
        return max_score * 100, most_similar_project.name  # Scale to percentage
