from flask import Flask, render_template,request
import pickle
import numpy as np
app = Flask(__name__)
popular_books=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
pivot_tabling=pickle.load(open('pivot_tabling.pkl','rb'))
@app.route('/')
def top_books():
    return render_template('top_books.html', book_name=list(popular_books['Book-Title'].values),
                           author_name=list(popular_books['Book-Author'].values),
                           publish_date=list(popular_books['Year-Of-Publication'].values),
                           Publisher_name=list(popular_books['Publisher'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           rating=list(popular_books['num_ratings'].values),
                           avg_rating=list(popular_books['avg_rating'].values))

@app.route('/recommend_books', methods=['GET', 'POST'])
def recommend_books():
    if request.method == 'POST':
        book_name = request.form.get('book_name').strip()

        if book_name not in books['Book-Title'].values or book_name not in pivot_tabling.index:
            return render_template('recommend.html', error="Book not found or unavailable for recommendation.")

        index = np.where(pivot_tabling.index == book_name)[0][0]
        distance = similarity_score[index]
        similar_item = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:9]

        data = []
        for i in similar_item:
            temp = books[books['Book-Title'] == pivot_tabling.index[i[0]]].drop_duplicates('Book-Title')
            temp_store = [
                temp['Book-Title'].values[0],
                temp['Book-Author'].values[0],
                temp['Publisher'].values[0],
                temp['Image-URL-M'].values[0]
            ]
            data.append(temp_store)

        return render_template('recommand.html', data=data, book_name=book_name)

    # Render empty recommend form on GET
    return render_template('recommand.html')


if __name__ == '__main__':
    app.run(debug=True)
