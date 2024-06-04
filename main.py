import pyodbc
import random
import string

conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=;uid=;pwd=;Encrypt=yes;TrustServerCertificate=yes')

cur = conn.cursor()

user_id = str


def generateReviewID():
    return "_" + "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(21))

def loginUser(user_id):
    return cur.execute(f"SELECT * FROM dbo.user_yelp WHERE user_id = '{user_id}'").fetchall()


def printMenu():
    print("Select from the operations mentioned below by entering 1-3  \n 1. Search Businesses \n 2. Search User \n 3. Exit Program")


def searchBusiness(minStars, maxStars, city, name):
    query = f"SELECT * FROM dbo.business WHERE city LIKE '%{city}%' AND name LIKE '%{name}%' AND stars >= {minStars} AND stars <= {maxStars}"
    cur.execute(query)
    result = cur.fetchall()
    for i in result: print(i)

def searchUsers(name, min_review_count, min_avg_stars):
    query = f"SELECT * FROM dbo.user_yelp WHERE name LIKE '%{name}%' AND review_count >= '{min_review_count}' AND average_stars >= '{min_avg_stars}'"
    cur.execute(query)
    result = cur.fetchall()
    for i in result: print(i)

def makeFriend(current_user_id, friend_user_id):
    query = f"INSERT INTO dbo.friendship (user_id, friend) VALUES ('{current_user_id}', '{friend_user_id}')"
    cur.execute(query)
    cur.commit()


def writeReview(business_id, user_id, stars):
    review_id = generateReviewID()
    query = f"INSERT INTO dbo.review (review_id, user_id, business_id, stars) VALUES ('{review_id}', '{user_id}', '{business_id}', {stars})"
    cur.execute(query)
    cur.commit()

def findBusinessID(business_id):
    query = f"SELECT * FROM dbo.business WHERE business_id = '{business_id}'"
    cur.execute(query)
    result = cur.fetchall()
    return result

def findUserID(user_id):
    query = f"SELECT * FROM dbo.user_yelp WHERE user_id = '{user_id}'"
    cur.execute(query)
    result = cur.fetchall()
    return result

def validateBusinessID():
    while True:
        businessID = input("Please enter the business ID for which you want to write the review: ")
        result = findBusinessID(businessID)
        if len(result) > 0:
            return businessID
        elif len(result) == 0:
            print("Invalid Business Id entered try again.")
            continue

def validateUserID():
    while True:
        userID = input("Please enter the user ID for the user you want to be friends with: ")
        result = findUserID(userID)
        if len(result) > 0:
            return userID
        elif len(result) == 0:
            print("Invalid User Id entered try again.")
            continue

def validateStars():
    while True:
        stars = int(input("Please enter the number of stars between 1-5 for the selected business: "))
        if stars <=5 and stars >= 1:
            return stars
        else:
            print("Invalid Input the stars should be in between 1 to 5 integer value: ")
            continue

flag = True

logged_in = False

# print(len(findBusinessID("_3DBgWpzjo_TSNm4jRNiJg")),
# len(findBusinessID("_3DBgWpzjo_TSNm4jRNiJf")))



# searchBusiness(3, 3, "Edmonton", "King of Donair")

# searchUsers('Wayne', 5, 3.44)


# makeFriend("_cCBinSoX4tLNt4reHqMkg", "_caxDQfQcOba3KKwouiIQA")

# writeReview("__4byNsswqnO2GIwwammQW", "vcrTtmz-VZTABbU1bGST4Q", "8jjjhTDBqTsXCok4DvGHGg", 3)

# print(len("__4byNsswqnO2GIwwammQW"))

# print(generateReviewID())


while True:
    user_id = str(input("Please enter your user ID for login: "))
    result = loginUser(user_id)
    if len(result) == 0:
        print("login failed")
        option = input("Do you want to try again? yes/no: ").lower().strip()
        if option == "yes":
            continue
        else:
            break
    elif len(result) == 1:
        print("\nLogin Successful!\n")
        logged_in = True
        break

name = result[0][1]

print(f"Welcome {name}!")

while flag and logged_in:
    printMenu()
    userSelection = int(input())
    if userSelection == 1:
        userMinStars = input("What should be the minimum stars between 1-5: ")

        if userMinStars == "":
            minStars = 1
        else:
            minStars = float(userMinStars)

        userMaxStars = input("What should be the maxmimum stars between 1-5: ")

        if userMaxStars == "":
            maxStars = 5
        else:
            maxStars = float(userMaxStars)

        cityName = input("Please enter the city: ")
        businessName = input("Please enter the partial or full business name: ")
        print("\nSearching Business\n")
        searchBusiness(minStars, maxStars, cityName, businessName)
        reviewOption = input("\nWant to write a review? yes/no: ").strip()
        if reviewOption.lower() == "yes":
            businessID = validateBusinessID()
            stars = validateStars()
            writeReview(business_id=businessID, user_id=user_id, stars=stars)
            print("\nReview Inserted!\n")
        elif reviewOption.lower() == "no":
            continue
    elif userSelection == 2:
        userName = input("Please input the username: ")
        user_min_review_count = (input("Minimum number of stars: "))

        if user_min_review_count == "":
            min_review_count = 0
        else:
            min_review_count = int(user_min_review_count)

        user_min_avg_stars = (input("Minimum average number of stars: "))

        if user_min_avg_stars == "":
            min_avg_stars = 0.0
        else:
            min_avg_stars = float(user_min_avg_stars)

        print("\nSearching Users\n")
        searchUsers(userName, min_review_count, min_avg_stars)
        friendOption = input("Want to make a user a friend? yes/no: ").strip()
        if friendOption.lower() == "yes":
            userID = validateUserID()
            makeFriend(user_id, userID)
            print("\nRelation Inserted!\n")
        elif friendOption.lower() == "no":
            continue

    elif userSelection == 3:
        print("Exiting")
        flag = False
    else:
        print("Invalid Option")




conn.close()
