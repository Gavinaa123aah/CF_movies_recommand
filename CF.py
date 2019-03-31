import csv
from numpy import *


class CF(object):
    def __init__(self):
        self.rating_data = []
        self.movie_data = []
        self.user_ratings = {}
        self.movie_users = {}
        self.neighbors = []
        self.recommandList = []
        self.recommand_result=[]
        self.userId = None
        self.num = 15

    def read_csv(self):
        with open('data_set/ratings.csv', 'r') as f_ratings:
            reader = csv.DictReader(f_ratings)
            for row in reader:
                self.rating_data.append(row)

        with open("data_set/movies.csv", "r") as f_movies:
            reader = csv.DictReader(f_movies)
            for row in reader:
                self.movie_data.append(row)

    def generate_user_item_dict(self):
        for value in self.rating_data:
            temp = (value['movieId'], float(value["rating"]) / 5)
            if value["userId"] in self.user_ratings:
                self.user_ratings[value["userId"]].append(temp)
            else:
                self.user_ratings[value["userId"]] = [temp]
            if value["movieId"] in self.movie_users:
                self.movie_users[value["movieId"]].append(value["userId"])
            else:
                self.movie_users[value["movieId"]] = [value["userId"]]

    def get_nearest_neighbor(self,userId):
        user_neighbor = []
        for i in self.user_ratings[userId]:
            for j in self.movie_users[i[0]]:
                if j != userId and j not in user_neighbor:
                    user_neighbor.append(j)
        # print user_neighbor
        for i in user_neighbor:
            distance = self.get_distance(userId, i)
            self.neighbors.append([distance, i])
            self.neighbors.sort(reverse=True)
            self.neighbors = self.neighbors[:self.num]

    def format_user_dict(self, userId, l):
        user = {}
        # user{"movieid":["userId_rating","i_rating"]...} if no rating,set rating 0
        for i in self.user_ratings[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.user_ratings[l]:
            if (j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    def get_distance(self,userId,i):
        # return random.randint(1,5)
        user = self.format_user_dict(userId, i)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    def get_recommand_list(self, userId):
        self.recommandList = []
        recommandDict = {}
        for neighbor in self.neighbors:
            movies = self.user_ratings[neighbor[1]]
            for movie in movies:
                if (movie[0] in recommandDict):
                    recommandDict[movie[0]] += neighbor[0]
                else:
                    recommandDict[movie[0]] = neighbor[0]
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.num]

    def get_recommand_result(self):
        for i in self.recommandList:
            for movie in self.movie_data:
                if i[1]==movie["movieId"]:
                    self.recommand_result.append(movie)

    def start_recommand(self,userId):
        self.userId = userId
        self.read_csv()
        self.generate_user_item_dict()
        self.get_nearest_neighbor(self.userId)
        self.get_recommand_list(self.userId)
        self.get_recommand_result()
        return self.recommand_result


if __name__ == '__main__':
    cf = CF()
    cf.read_csv()
    print ("self.rating_data list[0]")
    print (cf.rating_data[0])
    print ("self.movie_data list[0]")
    print (cf.movie_data[0])
    cf.generate_user_item_dict()
    print ("user_ratings dict")
    print (cf.user_ratings["2"])
    print ("movie_users dict")
    print (cf.movie_users["1"])
    cf.get_nearest_neighbor("1")
    print ("neighbor")
    print (cf.neighbors)
    cf.get_recommand_list("1")
    print ("recommand_list")
    print (cf.recommandList)
    cf.get_recommand_result()
    print ("recommand_result")
    print (cf.recommand_result)



