from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import String, Column, Integer, ForeignKey, Enum, PrimaryKeyConstraint

from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(50), nullable=False)

    firstname = Column(String(50), nullable=False)

    lastname = Column(String(50), nullable=False)

    email = Column(String(100), unique=True)

    #Relación con Comment
    comments = relationship("Comment", back_populates="user")

    #Relación con Post
    posts = relationship("Post", back_populates="user")

    #Relación compuesta con Follower
    followers = relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="followed")
    
    following = relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="follower")

    def serialize(self):

        return {

            "id": self.id,

            "username": self.username,

            "firstname": self.firstname,

            "lastname": self.lastname,

            "email": self.email,

        }


class Comment(db.Model):

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)

    comment_text = Column(String(100), nullable=False)

    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    #Relación inversa con User
    user = relationship("User", back_populates="comments")

    #Relación inversa con Post
    post = relationship("Post", back_populates="comments")

    def serialize(self):

        return {

            "id": self.id,

            "comment_text": self.comment_text,

            "author_id": self.author_id,

            "post_id": self.post_id,

        }

class Post(db.Model):

    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    #Relación inversa con User
    user = relationship("User", back_populates="posts")

    #Relación con Comment
    comments = relationship("Comment", back_populates="post")

    #Relación con Media
    medias = relationship("Media", back_populates="post")

    def serialize(self):

        return {

            "id": self.id,

            "user_id": self.user_id,  

        }

class Media(db.Model):

    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(Enum("image", "video", "audio", name="media_types"), nullable=False)
    
    url = Column(String(1000), nullable=False)

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    #Relación inversa con Post
    post = relationship("Post", back_populates="medias")

    def serialize(self):

        return {

            "id": self.id,

            "type": self.type,

            "url": self.url,

            "post_id": self.post_id,
   
        }

class Follower(db.Model):

    __tablename__ = "follower"
    user_from_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_to_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Definir clave primaria compuesta
    __table_args__ = (PrimaryKeyConstraint('user_from_id', 'user_to_id'),)

    # Relación con User (quien sigue)
    follower = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    
    # Relación con User (quien es seguido)
    followed = relationship("User", foreign_keys=[user_to_id], back_populates="followers")


    def serialize(self):

        return {

            "user_from_id": self.user_from_id,

            "user_to_id": self.user_to_id,

        }
    