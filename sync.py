from GitlabHelper import GitlabHelper

if not GitlabHelper.gitAvailable():
    print "Git cannot be called. Please check your path."
    exit(1)

endpoint = GitlabHelper.getEndpoint()
key = GitlabHelper.getKey()

if key is None:
    print "The key for gitlab API is missing. To add your key, type the following command :"
    print "$> git config --global gitlab-sync.private-token MY-PRIVATE-TOKEN-HERE"
    exit(1)

gitlab = GitlabHelper(key, endpoint)

projects = gitlab.getProjects()
syncEntities = GitlabHelper.projectsToSyncEntities(projects)

for entities in syncEntities:
    print entities
    if entities.getOrUpdate():
        print "Synchronized"
