import os



class RangeFileWrapper:
    def __init__(self, file, offset=0, length=None, chunk_size=8192):
        self.file = file
        self.file.seek(offset)
        self.remaining = length
        self.chunk_size = chunk_size


    def __iter__(self):
        while True:
            bytes_to_read = self.chunk_size if self.remaining is None else min(self.remaining, self.chunk_size)
            data = self.file.read(bytes_to_read)
            if not data:
                break
            if self.remaining:
                self.remaining -= len(data)
                yield data



def get_range_response(request, file_path, content_type='video/mp4'):
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get('Range', '').strip()
    file = open(file_path, 'rb')

    if range_header:
        try:
            pass