class PaginatorSessions:
    def __init__(self, message,  *pages, **options):
        self.message = message
        self.running = False
        self.current = 0
        self.pages = list(pages)
        self.destination = options.get("destination")
        self.inline_map = [

        ]