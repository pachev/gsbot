class ModelMixin(object):
    # This constant must be defined by any ORM that uses this mixin
    # it contains the DB columns of each model
    DB_COLUMNS = []

    @classmethod
    def create(klass, attributes):
        instance = klass()
        instance.set_attributes(attributes)
        instance.save()

        return instance


    def update(self, attributes):
        self.set_attributes(attributes)
        self.save()

    def set_attributes(self, attributes):
        for attr_name in attributes:
            if attr_name in self.DB_COLUMNS:
                setattr(self, attr_name, attributes[:attr_name])