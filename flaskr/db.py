def init_db(sq):

    class User(sq.model):
        pass

    class Login(sq.model):
        pass

    class UserVerified(sq.model):
        pass

    class UserSubordinates(sq.model):
        pass

    class Documents(sq.model):
        pass

    class DocumentPinned(sq.model):
        pass

    class DocumentQR(sq.model):
        pass

    return User, Login, UserVerified, UserSubordinates, Documents, DocumentPinned, DocumentQR