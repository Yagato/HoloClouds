import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import regex
import seaborn as sns
from sklearn.preprocessing import MaxAbsScaler
from sklearn.neighbors import NearestNeighbors

anime = pd.read_csv(r'C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Anime Recommender\anime.csv')
print(anime.head())

anime.loc[(anime["genre"]=="Hentai") & (anime["episodes"]=="Unknown"),"episodes"] = "1"
anime.loc[(anime["type"]=="OVA") & (anime["episodes"]=="Unknown"),"episodes"] = "1"
anime.loc[(anime["type"] == "Movie") & (anime["episodes"] == "Unknown")] = "1"

known_animes = {"Naruto Shippuuden":500,
                "One Piece":784,
                "Detective Conan":854,
                "Dragon Ball Super":86,
                "Crayon Shin chan":942,
                "Yu Gi Oh Arc V":148,
                "Shingeki no Kyojin Season 2":25,
                "Boku no Hero Academia 2nd Season":25,
                "Little Witch Academia TV":25}

for k,v in known_animes.items():
    anime.loc[anime["name"]==k,"episodes"] = v

anime["anime_id"] = anime["anime_id"].astype(int)

anime["episodes"] = anime["episodes"].map(lambda x:np.nan if x=="Unknown" else x)
anime["episodes"].fillna(anime["episodes"].median(), inplace=True)

anime["rating"] = anime["rating"].astype(float)
anime["rating"].fillna(anime["rating"].median(), inplace=True)

print(pd.get_dummies(anime[["type"]]).head())

anime["members"] = anime["members"].astype(float)

anime_features = pd.concat([anime["genre"].str.get_dummies(sep=","),
                            pd.get_dummies(anime[["type"]]),
                            anime[["rating"]],
                            anime[["members"]],
                            anime["episodes"]], axis=1)

anime["name"] = anime["name"].map(lambda name:regex.sub('[^A-Za-z0-9][+-=/:;]+', " ", name))

print(anime_features.head())
print(anime_features.columns)

max_abs_scaler = MaxAbsScaler()
anime_features = max_abs_scaler.fit_transform(anime_features)

nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)
distances, indices = nbrs.kneighbors(anime_features)


def get_index_from_name(name):
    return anime[anime["name"] == name].index.tolist()[0]


print(get_index_from_name("Kemono Friends"))
print(distances[11018])
print(indices[11018])

all_anime_names = list(anime.name.values)

def get_id_from_partial_name(partial):
    for name in all_anime_names:
        if partial in name:
            print(name, all_anime_names.index(name))

def print_similar_anime(query=None,id=None):
    if id:
        for id in indices[id][1:]:
            print(anime.iloc[id]["name"])
    if query:
        found_id = get_index_from_name(query)
        for id in indices[found_id][1:]:
            print(anime.iloc[id]["name"])

print("----- Kemono Friends -----")
print_similar_anime(query="Kemono Friends")
print("----- Tengen Toppa Gurren Lagann -----")
print_similar_anime(query="Tengen Toppa Gurren Lagann")
print("----- Steins;Gate -----")
print_similar_anime(query="Steins;Gate")
print("----- Houseki no Kuni -----")
print_similar_anime(query="Houseki no Kuni")
print("----- Pokemon (obtener ids) -----")
get_id_from_partial_name("Pokemon")
print("----- Hidamari Sketch (usando id) -----")
print_similar_anime(id=1528)
print("----- Koe no Katachi -----")
print_similar_anime("Koe no Katachi")
