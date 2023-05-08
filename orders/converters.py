class FloatUrlParameterConverter:
    regex = "[0-9]+\.?[0-9]+"

    def to_python(self, value) -> float:
        return float(value)

    def to_url(self, value) -> str:
        return str(value)
