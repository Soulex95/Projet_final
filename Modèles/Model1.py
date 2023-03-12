import pandas as pd
import pickle as pkl
from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv(r"C:\Users\DELL\Desktop\Projets\Recommandation\Codes\public.posts.csv")
df_likes = pd.read_csv(r"C:\Users\DELL\Desktop\Projets\Recommandation\Codes\public.post_likes.csv")

with open('df.pickle', 'wb') as f:
    pkl.dump(df, f)

with open('df_likes.pickle', 'wb') as f:
    pkl.dump(df_likes, f)
# ajouter une colonne valeur comme mesure
df_likes = df_likes.assign(values = 1)

#créer la matrice
user_likes_matrix = df_likes.pivot_table(index='user_id', columns='post_id', values='values')

#affecter tous les NAN à 0
user_likes_matrix = user_likes_matrix.fillna(0)
#user_likes_matrix = pd.DataFrame(user_likes_matrix)
#print(user_likes_matrix)

# Calculer les similarités entre les utilisateurs
# Calculate similarity scores
user_similarity = cosine_similarity(user_likes_matrix)
user_similarity = pd.DataFrame(user_similarity)
#print(user_similarity)

with open('model1.pickle', 'wb') as f:
    pkl.dump(user_similarity, f)

with open('matrix.pickle', 'wb') as f:
    pkl.dump(user_likes_matrix, f)


