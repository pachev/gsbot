class ModelMixin(object):
    # This constant must be defined by any ORM that uses this mixin
    # it contains the DB columns of each model
    DB_COLUMNS = []

    # Instantiates a new Class and saves the result to the DB, and returns
    @classmethod
    def create(cls, attributes):
        instance = cls()
        instance.__set_attributes(attributes)
        instance.save()
        return instance

    # Updates the attributes of the existing instance, and saves it to the DB
    def update_attributes(self, attributes):
        self.__set_attributes(attributes)
        self.save()

    def __set_attributes(self, attributes):
        for attr_name in attributes:
            if attr_name in self.DB_COLUMNS:
                setattr(self, attr_name, attributes[attr_name])