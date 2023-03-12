import pandas as pd
df_likes = pd.read_csv(r"C:\Users\DELL\Desktop\Projets\Recommandation\Codes\public.post_likes.csv")
#print(df_likes)
counter = df_likes.value_counts
print(counter)