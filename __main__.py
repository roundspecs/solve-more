import codeforces_api
from datetime import datetime

class User:
  def __init__(self,handle,solve_count,rounded_rating) -> None:
    self.handle = handle
    self.solve_count = solve_count
    self.rounded_rating = rounded_rating
  def __lt__(self, other):
    return self.solve_count > other.solve_count
  def __str__(self):
    return f"{self.handle:<13} {self.solve_count}"


cf_api = codeforces_api.CodeforcesApi()
unix_today = datetime.combine(datetime.today().date(), datetime.min.time()).timestamp()

users = [User(handle,0,0) for handle in input("Handles (space separated): ").split(' ')]
for i,info in enumerate(cf_api.user_info(handles=[user.handle for user in users])):
  users[i].rounded_rating = round(info.max_rating/100)*100

print("\nGood problems = {problem | problem.rating >= round(user.max_rating)}\n")
print("Good problems solved:")
for user in users:
  print(user.handle, end=": ")
  submissions = cf_api.user_status(handle=user.handle, count=100)
  acs = set()
  for submission in submissions:
    if submission.creation_time_seconds < unix_today:
      continue
    if submission.verdict != "OK":
      continue
    problem: codeforces_api.Problem = submission.problem
    if problem.rating < user.rounded_rating:
      continue
    acs.add(f"{problem.contest_id}{problem.index}")
  print(','.join(acs))
  user.solve_count=len(acs)

print(f"\n{'handle':<13} count")
print(f"{'------':<13} -----")
users.sort()
for user in users:
  print(user)
