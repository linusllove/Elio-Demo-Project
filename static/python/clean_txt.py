path = 'static/txt/activities.txt'

with open(path, 'r') as f:
    activities = f.read()

activities = activities.replace('\n\n', '\n')

save_path = 'static/txt/activities_clean.txt'
with open(save_path, 'w') as f:
    f.write(activities)
