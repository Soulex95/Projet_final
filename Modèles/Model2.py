# Importer les bibliothèques necessaires
import psycopg2
import pickle as pkl
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# Se connecter à la base de données
HOST = "localhost"
USER = "postgres"
PASSWORD = "balde95"
DATABASE = "Concree_data"

# Ouvrir la connection
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))

# Ouvrir le curseur pour envoyer des requettes sql
cur = conn.cursor()
# lancer la commande sql
interest = "SELECT * FROM interest"
cur.execute(interest)
#cur.execute(post_like)
# recuperation des données
df1 = pd.DataFrame(cur.fetchall(), columns=['id','user_id','interest_id'])
# fermer la connexion
conn.close()

with open('df1.pickle', 'wb') as f:
    pkl.dump(df1, f)

# importer les données supplementaires
df = pd.read_csv(r"C:\Users\DELL\Desktop\Projets\Recommandation\Codes\public.posts.csv")
df_likes = pd.read_csv(r"C:\Users\DELL\Desktop\Projets\Recommandation\Codes\public.post_likes.csv")

# ajouter une colonne valeur comme mesure
df1 = df1.assign(value=1)

#créer la matrice
user_interest_matrix = df1.pivot_table(index='user_id', columns='interest_id', values='value')
#affecter tous les NAN à 0
user_interest_matrix = user_interest_matrix.fillna(0)
user_interest_matrix = pd.DataFrame(user_interest_matrix)
#print(user_interest_matrix)

# Calculer les similarités entre les utilisateurs
user_similarity = cosine_similarity(user_interest_matrix)
user_similarity = pd.DataFrame(user_similarity)
#print(user_similarity)
# enregistrer le modèle et la matrice
with open('model2.pickle', 'wb') as f:
    pkl.dump(user_similarity, f)

with open('matrix2.pickle', 'wb') as f:
    pkl.dump(user_interest_matrix, f)

