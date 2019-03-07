class Transaction ():


    def __init__(self, id):
        self.id = id;


    def equals(self, obj):
        if (obj == None):
            return False

        if (type(self) != type(obj)):
            return False

        other = obj
        if (self.id != other.id):
            return False

        return True


    def hashCode(self):
        return self.id
