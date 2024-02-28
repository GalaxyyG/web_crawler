class URL_Manager():
    def __init__(self):
        self.new_urls = set() #setup two unions to store url
        self.old_urls =set()

    def Add_New_URL(self, url): #add single url to created union
        if url is None or len(url) == 0: #estimate if url is valuable
            return
        if url in self.new_urls or url in self.old_urls: #estimate if url already exists
            return
        self.new_urls.add(url)

    def Add_New_URLs(self, urls): #add a set of url to created union
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.Add_New_URL(url)

    def Get_URL(self): #get url from newurl set and update its statement(add it to oldurl set)
        if self.Has_New_URL():
            url = self.new_urls.pop()
            self.old_urls.add(url)
            return url
        else:
            return None

    def Has_New_URL(self): #estimate if still exist urls waiting to crawl in newurl set
        return len(self.new_urls) > 0
