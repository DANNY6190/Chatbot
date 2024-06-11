from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
import random
import json

from chat.models import Chat
from compte.models import Client
from django.utils import timezone

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat

# with open('chat\data\intents.json', 'r') as json_data:
#     intents = json.load(json_data)


import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipedia
# from deep_translator import GoogleTranslator
import spacy
from langdetect import detect
# from lefff import LefffLemmatizer

# Téléchargement des ressources NLTK
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

with open('chat\data\intents_final.json', 'r', encoding='utf-8') as json_data:
    reponses = json.load(json_data)

# Charger les modèles spacy
nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')

def preprocess_text(text):
    # Détecter la langue du texte
    language = detect(text)
    
    # Tokenization
    tokens = word_tokenize(text.lower())

    if language == 'fr':
        # Suppression des stopwords en français
        filtered_tokens = [word for word in tokens if word not in stopwords.words('french')]
        # Lemmatization en français
        doc = nlp_fr(' '.join(filtered_tokens))
    else:
        # Suppression des stopwords en anglais (par défaut)
        filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]
        # Lemmatization en anglais
        doc = nlp_en(' '.join(filtered_tokens))

    lemmatized_tokens = [token.lemma_ for token in doc]
    return ' '.join(lemmatized_tokens)


# Prétraitement des questions et réponses
preprocessed_questions = [preprocess_text(q) for q in reponses.keys()]

# Vectorisation des questions
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(preprocessed_questions)

# Fonction pour trouver la réponse à une question
def repondre_question(question):
    # Prétraitement de la question
    preprocessed_question = preprocess_text(question)
    # Calcul des similarités de cosinus entre la question donnée et les questions prédéfinies
    question_vector = vectorizer.transform([preprocessed_question])
    similarities = cosine_similarity(question_vector, question_vectors)
    # Trouver l'indice de la question la plus similaire
    max_similarity_index = similarities.argmax()
    max_similarity = similarities[0][max_similarity_index]
    # Déterminer si la similarité est suffisante pour considérer la question comme correspondante
    if max_similarity > 0.5:  # Vous pouvez ajuster ce seuil selon vos besoins
        return list(reponses.values())[max_similarity_index]
    else:
        return "Désolé, je ne comprends pas bien votre préoccupation. Veuillez reformuler ou reposer le problème s'il vous plaît..."


def chat(request):
    current_page = request.path
    
    # Récupérer tous les chats
    chats = Chat.objects.all()

    if request.method == 'POST':
        message = request.POST.get('message')
        print (f'Client = {message}')
        response = repondre_question(message)
        print("Agent :", response)

        # Enregistrer le message dans la base de données
        chat = Chat(message=message, response=response, created_at=timezone.now())
        chat.save()
        
        return JsonResponse({'message': message, 'response': response})
    
    context = {
        'current_page': current_page,
        'chats': chats,
    }
    return render(request, 'chat/chat.html', context)




# Create your views here.
# @login_required
# def chat(request):
#     current_page = request.path
#     user = request.user
    
#     # Assurez-vous que l'utilisateur est bien une instance de Client
#     if not isinstance(user, Client):
#         # Gérer cette situation selon vos besoins, par exemple, renvoyer une erreur HTTP 403
#         return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette ressource.")
    
#     chats = Chat.objects.filter(user=request.user)


#     if request.method == 'POST':
#         message = request.POST.get('message')
#         response = ask_openai(message)

#         chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now)
#         chat.save()
#         return JsonResponse({'message': message, 'response': response})
#     context = {
#         'current_page': current_page,
#         'chats': chats,
#     }
#     return render(request, 'chat/chat.html', context)


# Fonction de prétraitement du texte
# def preprocess_text(text):
#     # Tokenization
#     tokens = word_tokenize(text.lower())
#     # Suppression des stopwords
#     filtered_tokens = [word for word in tokens if word not in stopwords.words('french')]
#     # Lemmatization
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
#     return ' '.join(lemmatized_tokens)