class Keyword:
    def __init__(self, keyword, kClass):
        if (keyword == None or keyword == ""):
            raise Exception("invalid keyword")
        if not kClass:
            raise Exception(f"invalid keyword class: keyword = {keyword}; kClass = {kClass}")
        self.keyword = keyword
        self.kClass = kClass
    
    def getKeyword(self):
        return self.keyword
    
    def getkClass(self):
        return self.kClass