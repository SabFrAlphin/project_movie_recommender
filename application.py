from flask import Flask, render_template, request
from recommender import movies_list, movie_recommender


app = Flask(__name__)
# __name__ is simply a reference to the current python script / module.


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', choices=movies_list)


@app.route('/recommendation')
def recommend():
    user_input = dict(request.args)

    one = {user_input['movie1']: user_input['rating1']}
    two = {user_input['movie2']: user_input['rating2']}
    three = {user_input['movie3']: user_input['rating3']}
    one.update(two)
    one.update(three)
    flask_user_input = one
    print(flask_user_input)

    recommend = movie_recommender(flask_user_input)
    return render_template('recommendation.html', movies=recommend)


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    # if I run "python application.py", please run the following code....
    app.run(debug=True, use_reloader=True)
