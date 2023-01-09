import re

#Check if the string starts with "The" and ends with "Spain":

txt = "adawedqwojS01E93.mp4"


pattern = re.compile(r'(?P<VUL>(\d{1,2}|One)\s+ 
(vulnerabilities|vulnerability)\s+discovered)')

match = re.findall(pattern, data)

pattern = re.compile('S(?<season>\d{1,2})E(?<episode>\d{1,2})')
pattern.groupindex

print(pattern.groupindex)

#SELECT EpisodeRequests.id as EpiReqId,
# EpisodeRequests.SeasonId as SeasonId,
# SeasonRequests.ChildRequestId as RequestId,
# SeasonRequests.SeasonNumber as SeasonNr,
# EpisodeRequests.EpisodeNumber,
# EpisodeRequests.Title
# FROM EpisodeRequests
# INNER JOIN SeasonRequests
# ON EpisodeRequests.SeasonId = SeasonRequests.Id
# INNER JOIN ChildRequests
#ON SeasonRequests.ChildRequestId = ChildRequests.Id;