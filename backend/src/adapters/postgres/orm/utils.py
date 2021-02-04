from sqlalchemy.types import UserDefinedType

class TsVector(UserDefinedType):
    "Holds a TsVector column"

    name = "TSVECTOR"

    def get_col_spec(self):
        return self.label

class comparator_factory(UserDefinedType.Comparator):
    """Defines custom types for tsvectors.

    Specifically, the ability to search for ts_query strings using
    the @@ operator.

    On the Python side, this is implemented simply as a `==` operation.

    So, you can do
    Table.tsvector_column == "string"
    to get the same effect as
    tsvector_column @@ to_tsquery('string')
    in SQL

    """


    def __eq__(self, other):
        return self.op('@@')(func.to_tsquery(other))

