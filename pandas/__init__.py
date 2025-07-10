class DataFrame(list):
    def __init__(self, records):
        super().__init__(records)
        self.columns = list(records[0].keys()) if records else []

    def drop(self, columns):
        if isinstance(columns, list):
            cols = set(columns)
        else:
            cols = {columns}
        data = [{k: v for k, v in row.items() if k not in cols} for row in self]
        return DataFrame(data)

    def to_dict(self, orient='records'):
        return list(self)

def read_csv(io_buffer):
    import csv
    if isinstance(io_buffer, str):
        import io as _io
        io_buffer = _io.StringIO(io_buffer)
    reader = csv.DictReader(io_buffer)
    return DataFrame([row for row in reader])
