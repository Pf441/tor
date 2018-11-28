from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Volunteer(Base):
    __tablename__ = 'volunteers'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    gamma = Column(Integer, nullable=False)
    email = Column(String(255))
    password = Column(String(40))
    join_date = Column(DateTime)
    last_login_time = Column(DateTime)

    transcriptions = relationship("Transcription", back_populates="volunteer")
    posts = relationship("Post", back_populates="volunteer")

    def __repr__(self):
        return f"<Volunteer - {self.username}>"


class Post(Base):
    # It is rare, but possible, for a post to have more than one transcription.
    # Therefore, posts are separate from transcriptions, but there will almost
    # always be one transcription per post.
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    post_id = Column(String(20), unique=True)
    volunteer_id = Column(ForeignKey("volunteers.id"))
    # Where does it come from? Reddit? A library?
    source = Column(String(30))
    # recommended max length https://stackoverflow.com/a/219664
    url = Column(String(2083))

    volunteer = relationship("Volunteer", back_populates="posts")
    transcriptions = relationship("Transcription", back_populates="post")

    def __repr__(self):
        return f"<Post - {self.post_id}>"


class Transcription(Base):
    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    post_id = Column(ForeignKey("posts.id"))
    volunteer_id = Column(ForeignKey("volunteers.id"))
    # reddit comment ID or similar
    transcription_id = Column(Text(20))
    claim_time = Column(DateTime)
    done_time = Column(DateTime)
    # "reddit", "api", "tor_app". Leaving extra characters in case we want
    # to expand the options.
    completion_method = Column(String(20))
    url = Column(String(2083))
    # force SQL longtext type, per https://stackoverflow.com/a/23169977
    text = Column(Text(4294000000))

    post = relationship("Post", back_populates="transcriptions")
    volunteer = relationship("Volunteer", back_populates="transcriptions")

    def __repr__(self):
        return f"<Transcription - {self.post_id}>"


# And now, the other side of the connections!
Volunteer.posts = relationship(
    "Post", order_by=Post.id, back_populates="volunteer"
)
Volunteer.transcriptions = relationship(
    "Transcription", order_by=Transcription.id, back_populates="volunteer"
)
Post.transcriptions = relationship(
    "Transcription", order_by=Transcription.id, back_populates="post"
)

# # insert data
# tag_cool = Tag(name='cool')
# tag_car = Tag(name='car')
# tag_animal = Tag(name='animal')
#
# session.add_all([tag_animal, tag_car, tag_cool])
# session.commit()
#
# # query data
# t1 = session.query(Tag).filter(Tag.name == 'cool').first()
#
# # update entity
# t1.name = 'cool-up'
# session.commit()
#
# # delete
# session.delete(t1)
# session.commit()
