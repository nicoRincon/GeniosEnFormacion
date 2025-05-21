from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import random
import unicodedata

class FeedAIDataSpanish:
    def __init__(self):
        self.letters = []
        self.activities = []
        self.knn = KNeighborsClassifier(n_neighbors=1)

    def get_activity(self):
        for letter in range(65, 91):
            self.letters.append([letter])
            self.activities.append(f"Palabras con {chr(letter)}")

        self.letters = np.array(self.letters)

        self.knn.fit(self.letters, self.activities)

        new_letter = np.array([[random.randint(65, 91)]])
        return self.knn.predict(new_letter)

    def receive_and_process_activity(self):
        words_to_validate = np.array(["Árbol", "Barco", "Casa", "Dado", 'Saco'])
        words_to_validate = np.array([self.normalize_letter(word) for word in words_to_validate])
        first_letters = np.array([word[0] for word in words_to_validate])
        letters_to_ascii = np.array([ord(letter) for letter in first_letters])
        if letters_to_ascii.size > 0:
            ascii_codes_2d = letters_to_ascii.reshape(-1, 1)
            result_suggested_activity = self.knn.predict(ascii_codes_2d)
            for rsa in result_suggested_activity:
                print(f"La palabra ingresada pertenece a la actividad: {rsa}")
        else:
            print("La letra ingresada no está en los datos de la IA.")

    def normalize_letter(self, letter: str):
        # Quita acentos y convierte a mayúscula
        return unicodedata.normalize('NFKD', letter).encode('ASCII', 'ignore').decode('ASCII').upper()