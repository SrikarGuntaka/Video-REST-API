from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/video/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


with app.app_context():
    db.create_all()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, location=["json", "form"], help="Name of the video is required", required=True)
video_put_args.add_argument("likes", type=int, location=["json", "form"], help="Likes of the video", required=True)
video_put_args.add_argument("views", type=int, location=["json", "form"], help="Views of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, location=["json", "form"], help="Name of the video is required")
video_update_args.add_argument("likes", type=int, location=["json", "form"], help="Likes of the video")
video_update_args.add_argument("views", type=int, location=["json", "form"], help="Views of the video")


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video ID...")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID already taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video ID...")
        db.session.delete(result)
        db.session.commit()
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


@app.get("/")
def index():
    return render_template("index.html")

@app.delete("/videos")
def clear_videos():
    # Delete all rows in the VideoModel table
    num_deleted = VideoModel.query.delete()
    db.session.commit()
    return {"deleted": num_deleted}, 200

if __name__ == "__main__":
    app.run(debug=True)