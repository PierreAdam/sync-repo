import os

from GitlabHelper import GitlabHelper

gitlab = GitlabHelper("VaysS-V5ip-rrXZTC7gP", "https://payintech.githost.io")

projects = gitlab.getProjects()
syncEntities = GitlabHelper.projectsToSyncEntities(projects)

for entities in syncEntities:
    print entities
    if entities.getOrUpdate():
        print "Synchronized"

# os.system("git clone git@payintech.githost.io:payintech-toolbox/logback-toolbox.git")