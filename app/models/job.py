class Job:
    def __init__(self, data=None):
        data = data or {}
        self.url = data.get("url", "")        
        self.id = data.get("id", "")        
        self.title = data.get("title", "")
        self.company = data.get("company", "")
        self.post_date = data.get("post_date", "")
        self.description = data.get("description", "")        

    def __repr__(self):
        return (
            f"Job(url={self.url!r}, id={self.id!r}, "
            f"Job(title={self.title!r}, company={self.company!r}, "
            f"post_date={self.post_date!r}, description={self.description!r})"
        )