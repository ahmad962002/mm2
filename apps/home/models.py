from apps import db
import datetime

class Binance(db.Model):
    __tablename__ = 'binance'
    
    id            = db.Column(db.Integer, primary_key=True)
    user_id            = db.Column(db.Integer, unique=True)
    api      = db.Column(db.String(64))
    secret         = db.Column(db.String(64))
    def __repr__(self):
            return str(self.user_id)
    @classmethod
    def find_by_userid(cls, user_id: int) -> "Binance":
        return cls.query.filter_by(user_id=user_id).first()
    @classmethod
    def find_all(cls,) -> "Binance":
        return cls.query.all()

class Set(db.Model):
    __tablename__ = 'set2'
    
    id            = db.Column(db.Integer, primary_key=True)
    user_id            = db.Column(db.Integer, unique=True)
    delay = db.Column(db.Integer)
    qt = db.Column(db.Float)
    pair = db.Column(db.String(64))

    def __repr__(self):
            return str(self.user_id)
    @classmethod
    def find_by_userid(cls, user_id: int) -> "Set":
        return cls.query.filter_by(user_id=user_id).first()


class Data(db.Model):
    __tablename__ = 'data'
    
    id            = db.Column(db.Integer, primary_key=True)
    gainers       = db.Column(db.String(64),unique=False, default=False)
    def __repr__(self):
            return str(self.user_id)
    @classmethod
    def find(cls) -> "Data":
        return cls.query.first()
class Trades(db.Model):
    __tablename__ = 'trades'
    
    id            = db.Column(db.Integer, primary_key=True)
    
    price          = db.Column(db.Float)
    status         = db.Column(db.String(64),unique=False, default=False)
    coins          = db.Column(db.Float)
    time           = db.Column(db.String(64),unique=False, default=False)
    volume         = db.Column(db.Float)

    def __repr__(self):
            return str(self.user_id)
    @classmethod
    def find(cls) -> "trades":
        return cls.query.first()
    @classmethod
    def find_all(cls) -> "trades":
        # session.query(User).order_by(User.id.desc()).limit(3).all()[::-1]
        return cls.query.limit(1000).all()[::-1]


# class Signals(db.Model):
#     __tablename__ = 'signals'
#     id            = db.Column(db.Integer, primary_key=True)
#     user_id       = db.Column(db.Integer, unique=True)
#     date          = db.Column()
#     base          =db.Column()
#     side          =db.Column()
#     epi          =db.Column()
#     epf          =db.Column()
#     tps          =db.Column()
#     sl          =db.Column()

#     def __repr__(self):
#             return str(self.user_id)
#     @classmethod
#     def find_by_userid(cls, user_id: int) -> "Signals":
#         return cls.query.filter_by(user_id=user_id).first()

