from flask import Flask, render_template

app = Flask(__name__)

shoes_list = [{"img_url": "/static/assets/images/shoes/1.jpg", "title": "shoe1", "desc": "shoe1"},
         {"img_url": "/static/assets/images/shoes/2.jpg", "title": "shoe2", "desc": "shoe2"},
         {"img_url": "/static/assets/images/shoes/3.jpg", "title": "shoe3", "desc": "shoe3"},
         {"img_url": "/static/assets/images/shoes/4.jpg", "title": "shoe4", "desc": "shoe4"},
         {"img_url": "/static/assets/images/shoes/5.jpg", "title": "shoe5", "desc": "shoe5"}]

jackets_list = [{"img_url": "/static/assets/images/jackets/1.jpg", "title": "jacket1", "desc": "jacket1"},
         {"img_url": "/static/assets/images/jackets/2.jpg", "title": "jacket2", "desc": "jacket2"},
         {"img_url": "/static/assets/images/jackets/3.jpg", "title": "jacket3", "desc": "jacket3"},
         {"img_url": "/static/assets/images/jackets/4.jpg", "title": "jacket4", "desc": "jacket4"},
         {"img_url": "/static/assets/images/jackets/5.jpg", "title": "jacket5", "desc": "jacket5"}]
         
clothes_list = shoes_list + jackets_list

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/clothing')
def clothing():
    return render_template('category.html', clothes=clothes_list)

@app.route('/jacket')
def jacket():
    return render_template('jackets.html', jackets=jackets_list)

@app.route('/shoes')
def shoes():
    return render_template('shoes.html', shoes=shoes_list)


if __name__ == '__main__':
    app.run(debug=True)
