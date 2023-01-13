from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
anime_details = pickle.load(open('anime_details.pkl', 'rb'))
animes_cbrs = pickle.load(open('animes_cbrs.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def mainpage():
    return render_template('main.html',
    anime_name = list(popular_df['title'].values),
    synopsis = list(popular_df['synopsis'].values),
    genre = list(popular_df['genre'].values),
    release_date = list(popular_df['release_date'].values),
    episodes = list(popular_df['episodes'].values),
    rating = list(popular_df['score'].values),
    image = list(popular_df['img_url'].values)
    )

@app.route('/recommend', methods = ["POST", "GET"])
def recommend_ui():
    if request.method == 'GET':
        anime_name_search = list(anime_details['title'].values)
        return render_template('recommend.html', anime_name_search = anime_name_search)
    
@app.route('/recommend_anime', methods = ["POST", "GET"])
def recommend():
    if request.method == 'POST':
        anime_name_search = list(anime_details['title'].values)
    
    user_input = request.form.get('user_input')
    
    if(anime_details[anime_details['title'] == user_input].empty):
        return render_template('notavailable.html')
    else:
        index = animes_cbrs[animes_cbrs['title'] == user_input].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x: x[1])
        
        data = []
        for i in distances[1:11]:
            item = []

            temp_df = animes_cbrs[animes_cbrs['title'] == animes_cbrs.iloc[i[0]].title]
            item.extend(list(temp_df['title'].values))
            
            item.extend(list(anime_details[anime_details['title'].isin(temp_df['title'])]['synopsis'].values))
            
            item.extend(list(temp_df['genre'].values))
            item.extend(list(temp_df['release_date'].values))
            item.extend(list(temp_df['episodes'].values))
            item.extend(list(temp_df['score'].values))
            item.extend(list(temp_df['img_url'].values))
            
            data.append(item)
            
        new_df = anime_details[anime_details['title'] == user_input]
        new_data = []
        new_data.append(list(new_df['title'].values))
        new_data.append(list(new_df['synopsis'].values))
        new_data.append(list(new_df['genre'].values))
        new_data.append(list(new_df['release_date'].values))
        new_data.append(list(new_df['episodes'].values))
        new_data.append(list(new_df['score'].values))
        new_data.append(list(new_df['img_url'].values))
        
        return render_template('recommend.html', data = data, new_data = new_data, anime_name_search = anime_name_search)

if __name__ == '__main__':
    app.run(debug = True)