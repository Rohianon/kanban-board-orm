from itertools import count

counter = count()

class Field:    
    def __init__(self, name, py_type):
        self.name = name
        self.py_type = py_type

    def sql_type(self):
        return {
            int: "INTEGER",
            str: "TEXT",
        }[self.py_type]

    def __eq__(self, value):
        return Condition("=", self, value)

class Condition:    
    def __init__(self, op, field, value):
        self.op = op
        self.field = field
        self.value = value

    def to_sql(self):
        placeholder = f"var{next(counter)}"
        return (
            f"{self.field.name} {self.op} %({placeholder})s",
            {placeholder: self.value},
        )