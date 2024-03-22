from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bjvhtkuz:LndDY2I9eN_Oyr3rBn8aDSrufDE8459H@raja.db.elephantsql.com/bjvhtkuz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

# Create the database tables
with app.app_context():
    db.create_all()

# Define routes for displaying and submitting posts
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return 'Post submitted!'

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post.id,
            'title': post.title,
            'content': post.content
        })
    return jsonify(posts_list)

# Read - Retrieve a specific post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content
    })

# Create - Add a new post
@app.route('/posts', methods=['POST'])
def create_post():
    title = request.json.get('title')
    content = request.json.get('content')
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'})

# Update - Update an existing post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.json.get('title')
    content = request.json.get('content')
    post.title = title
    post.content = content
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

# Delete - Delete an existing post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})

# ... (remaining code for index and submit routes)

if __name__ == '__main__':
    app.run()