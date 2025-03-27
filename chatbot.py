import joblib
import tkinter as tk

# Définition de la classe ChatBotApp
class ChatBotApp:
    def __init__(self):
        self.rf_description1 = joblib.load('chatbot_models/model_chatbot_temp_1.joblib')
        self.rf_recommended1 = joblib.load('chatbot_models/model_chatbot_temp_2.joblib')
        self.encoder1_1 = joblib.load('chatbot_models/temp_chatbot_encoder1.joblib')
        self.encoder1_2 = joblib.load('chatbot_models/temp_chatbot_encoder2.joblib')

        self.rf_description2 = joblib.load('chatbot_models/model_chatbot_mono_1.joblib')
        self.rf_recommended2 = joblib.load('chatbot_models/model_chatbot_mono_2.joblib')
        self.encoder2_1 = joblib.load('chatbot_models/mono_chatbot_encoder1.joblib')
        self.encoder2_2 = joblib.load('chatbot_models/mono_chatbot_encoder2.joblib')

        self.rf_description3 = joblib.load('chatbot_models/model_chatbot_puiss_1.joblib')
        self.rf_recommended3 = joblib.load('chatbot_models/model_chatbot_puiss_2.joblib')
        self.encoder3_1 = joblib.load('chatbot_models/puiss_chatbot_encoder1.joblib')
        self.encoder3_2 = joblib.load('chatbot_models/puiss_chatbot_encoder2.joblib')
    def respond(self):
        # Récupération de l'entrée utilisateur
        user_input = self.entry.get().lower()
        
        # Vérifier si user_input est vide
        if not user_input:
            return

        self.display_message("Vous: " + user_input)

        # Vérifier si l'utilisateur a salué
        if user_input in self.greetings:
            bot_response = "Bonjour ! " + self.help_messages[0]
        elif user_input in self.help_messages:
            bot_response = "Je suis là pour vous aider. Veuillez décrire votre problème."
        else:
            bot_response = self.predict_cause_and_solution(user_input)

        # Afficher la réponse du ChatBot
        self.display_message("ChatBot: " + bot_response)

        # Effacer le champ d'entrée
        self.entry.delete(0,tk.END)


    # Méthode predict_cause_and_solution faisant partie de la classe ChatBotApp
    def predict_cause_and_solution(self, user_input):
        if not user_input:
            return "Entrez un message."
        if user_input.startswith('['):
            problem = list(map(int, user_input.strip('[]').split(',')))

            # Choisir le modèle en fonction de la longueur de l'entrée
            if len(problem) == 2:
                description = "C'est un système de température."
                rf_description = self.rf_description1
                rf_recommended = self.rf_recommended1
                encoder1 = self.encoder1_1
                encoder2 = self.encoder1_2
            elif len(problem) == 3:
                description = "C'est un système monophasé."
                rf_description = self.rf_description2
                rf_recommended = self.rf_recommended2
                encoder1 = self.encoder2_1
                encoder2 = self.encoder2_2
            elif len(problem) == 6:
                description = "C'est un système de puissance."
                rf_description = self.rf_description3
                rf_recommended = self.rf_recommended3
                encoder1 = self.encoder3_1
                encoder2 = self.encoder3_2
            else:
                return "Entrez un problème au format [a, b], [a, b, c] ou [a, b, c, d, e, f]."

            # Prédiction et encodage inverse
            predicted_decodage = encoder1.inverse_transform(rf_description.predict([problem]))[0]
            self.predicted_recommendation = encoder2.inverse_transform(rf_recommended.predict([problem]))[0]

            return f"{description}\n{predicted_decodage}\nVoulez-vous une recommandation pour ce problème?"
        # Vérification de la réponse pour la recommandation
        elif user_input.lower() == "oui" and self.predicted_recommendation:
            recommendation_response = self.predicted_recommendation
            self.predicted_recommendation = None
            return recommendation_response

        elif user_input.lower() == "non":
            return "Merci !"

        return "Entrez un problème au format [a, b], [a, b, c] ou [a, b, c, d, e, f]."

