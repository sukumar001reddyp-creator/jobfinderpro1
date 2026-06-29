class RSSParser:

    def parse(self, entry):

        return {
            "title": entry.get("title"),
            "description": entry.get("summary"),
            "apply_url": entry.get("link"),
        }
        