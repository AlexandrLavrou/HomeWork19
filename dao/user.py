from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    # def get_by_user_id(self, val):
    #     return self.session.query(User).filter(User.id == val).all()
    #
    # def get_by_user_role(self, val):
    #     return self.session.query(User).filter(User.role == val).all()

    def get_by_username(self, val):
        return self.session.query(User).filter(User.username == val).first()

    def create(self, user_data):
        ent = User(**user_data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_data):
        user = self.get_one(user_data.get("id"))
        user.username = user_data.get("username")
        user.password = user_data.get("password")
        user.role = user_data.get("role")

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
