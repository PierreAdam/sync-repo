import os
import requests
import subprocess

from SyncEntity import SyncEntity


class GitlabHelper:
    def __init__(self, token, endpoint=None):
        self.endpoint = endpoint if (endpoint is not None) else "https://gitlab.com"
        self.apiEndpoint = self.endpoint + "/api/v4"
        self.token = token
        self.baseHeaders = dict()
        self.baseHeaders["PRIVATE-TOKEN"] = self.token

    def buildApiUrl(self, route):
        return self.apiEndpoint + route

    def getProjects(self):
        has_result = True
        projects = list()
        page = 1;

        while has_result:
            route = self.buildApiUrl("/projects") + "?page={}".format(page)
            result = requests.get(route, headers=self.baseHeaders)

            if result.status_code != 200:
                raise Exception(
                    "Error while contacting gitlab API. Route {route} resulted with the code {code}".format(route=route,
                                                                                                            code=result.status_code))

            data = result.json()
            if len(data) == 0:
                has_result = False

            projects.extend(data)
            page += 1

        return projects

    @staticmethod
    def projectToSyncEntity(project):
        if 'path_with_namespace' not in project or 'ssh_url_to_repo' not in project:
            raise Exception("Invalid project.")

        repo = project['ssh_url_to_repo'].strip()
        project_path = os.path.split(project['path_with_namespace'])
        path_list = ['.']
        path_list.extend(project_path[:-1])
        path = os.path.join(*path_list).strip()
        folder = project_path[-1:][0].strip()
        return SyncEntity(path, folder, repo)

    @staticmethod
    def projectsToSyncEntities(projects):
        entities = list()
        for p in projects:
            entities.append(GitlabHelper.projectToSyncEntity(p))
        return entities

    @staticmethod
    def getEndpoint():
        try:
            return subprocess.check_output("git config gitlab-sync.endpoint", shell=True).strip()
        except Exception:
            return None

    @staticmethod
    def getKey():
        try:
            return subprocess.check_output("git config gitlab-sync.private-token", shell=True).strip()
        except Exception:
            return None

    @staticmethod
    def gitAvailable():
        try:
            subprocess.check_output("git --version")
            return True
        except Exception:
            return False
