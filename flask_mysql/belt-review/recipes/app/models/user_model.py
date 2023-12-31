import re
from app import app
from app.config.mysqlconnection import connectToMySQL
from app.models import recipe_model
from flask import Flask, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$")

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []

    #add users to DB
    @classmethod
    def save_user(cls, data):
        data['password'] =  bcrypt.generate_password_hash(data['password'])
        
        query = '''
                INSERT INTO users (first_name, last_name, email, password)
                VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                '''
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls,id):
        print(f'GETTING USERS WITH ID {id}')
        query = '''
                SELECT * FROM users
                LEFT JOIN recipes on users.id = recipes.user_id
                WHERE id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results[0])
        for row in results:
            recipe_data = { 
                'id':row['recipes.id'],
                'name':row['name'],
                'description':row['description'],
                'instructions':row['instructions'],
                'under_30_mins':row['under_30_mins'],
                'date_cooked':row['date_cooked'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at'],
                'user_id':row['user_id'],
            }
            user.recipes.append(recipe_model.Recipe(recipe_data))
        print(f'GETTING USER sending back {user}')
        return user
    
    #find users with email
    @classmethod
    def get_user_with_email(cls,email):
        print('GETTING USER WITH EMAIL')
        query = '''
                SELECT * FROM users
                LEFT JOIN recipes on users.id = recipes.user_id
                WHERE email = %(email)s;'''
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if len(results) < 1:
            return False
        else:
            user = cls(results[0])
            for row in results:
                recipe_data = { 
                    'id':row['recipes.id'],
                    'name':row['name'],
                    'description':row['description'],
                    'instructions':row['instructions'],
                    'under_30_mins':row['under_30_mins'],
                    'date_cooked':row['date_cooked'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at'],
                    'user_id':row['user_id']
                }
                user.recipes.append(recipe_model.Recipe(recipe_data))
            print(f'GETTING USERS sending back {results[0]}')
        return user
            # users_list = []
            # for user in results:
            #     users_list.append(cls(user))
    
    # get user with all attached recipes
    @classmethod
    def get_user_with_recipes(cls, id):
        query = """
                SELECT * FROM users
                LEFT JOIN recipes on users.id = recipes.user_id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results[0])
        for row in results:
            recipe_data = { 
                'id':row['recipes.id'],
                'name':row['name'],
                'description':row['description'],
                'instructions':row['instructions'],
                'under_30_mins':row['under_30_mins'],
                'date_cooked':row['date_cooked'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at'],
                'user_id':row['user_id']
            }
            user.recipes.append(recipe_model.Recipe(recipe_data))
        return user


    #validate registration form information
    @staticmethod
    def validate_user(data):
        # Set is_valid to true as default
        is_valid = True

        #validate first name
        #length
        print('VALIDATING')
        if len(data['first_name'])<3:
            if len(data['first_name'])<1:
                flash('First name field must be filled', 'registration')
                is_valid = False
            else:
                flash('First name field must be more than 3 characters', 'registration')
                is_valid = False
        
        #validate last name
        #length
        if len(data['last_name'])<3:
            if len(data['last_name'])<1:
                flash('Last name field must be filled', 'registration')
                is_valid = False
            else:
                flash('Last name field must be more than 3 characters', 'registration')
                is_valid = False
        
        #validate email
        #length
        if len(data['email'])<1:
            flash('email field must be filled', 'registration')
            is_valid = False
        
        #format
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format', 'registration')
            print('\n EMAIL FORMAT FAILED\n')
            is_valid = False
        
        #unique
        if User.get_user_with_email(data['email']):
            flash('Email not unique, please provide another', 'registration')
            is_valid = False

        #validate password
        #length
        if len(data['password'])<3:
            if len(data['password'])<1:
                flash('Password name field must be filled', 'registration')
                is_valid = False
            else:
                flash('Password name field must be more than 8 characters', 'registration')
                is_valid = False
        #FORMAT
        if not PASSWORD_REGEX.match(data['password']):
            flash('Invalid Password format', 'registration')
        #password match
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'registration')
            is_valid = False
        
        print(is_valid)
        return is_valid

