import dataset

db = dataset.connect('postgresql://pushserver:rdbUYT8nFrnMyWwbxRvduikM@localhost:5432/pushserver')

table = db['device']
user_id = table.find_one(userID="hey")
print(user_id)
table.insert(dict(userID="hey1", currentStreamToken="", deviceToken="heywhat"))


