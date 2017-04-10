import os

from cd import cd


class SyncEntity:
    def __init__(self, basePath, repoFolder, repoUrl):
        self.basePath = basePath
        self.repoFolder = repoFolder
        self.repoUrl = repoUrl
        self.fullPath = os.path.join(self.basePath, self.repoFolder)

    def __str__(self):
        return "{} <- {}".format(self.fullPath, self.repoUrl)

    def getOrUpdate(self):
        if os.path.exists(self.fullPath):
            return self.fetch()
        else:
            if not os.path.exists(self.basePath):
                os.mkdir(self.basePath, 0755)
            return self.clone()

    def clone(self):
        with cd(self.basePath):
            return os.system("git clone {} {}".format(self.repoUrl, self.repoFolder)) == 0

    def fetch(self):
        with cd(self.fullPath):
            return os.system("git fetch --prune") == 0