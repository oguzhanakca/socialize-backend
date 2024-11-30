# Socialize API

**Developer: Oğuzhan Akça**

The **Socialize API** is a Django Rest Framework API for social media applications with a focus images. The API is primarily used for the [Socialize](https://github.com/oguzhanakca/socialize-frontend) app, a social media app for posting images and chatting.

[API Link](https://socialize-backend-app-9beed826b5f2.herokuapp.com/)

[Socialize](https://socialize-frontend-app-cfe4edcc8238.herokuapp.com/)

## Table of Contents

- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Feature Ideas](#future-feature-ideas)
- [Design Process](#design-process)
  - [User Stories](#user-stories)
  - [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
  - [Frameworks and Languages](#frameworks-and-languages)
  - [Additional Python Packages](#python-packages)
  - [Libraries & Tools](#libraries--tools)
- [Validation](#validation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

## Features

### Existing Features

- **User Authentication**: Users can sign up and login. User profiles are automatically created upon sign-up.
- **Profile Settings**: Users can edit their profile image, privacy and bio. They can also change username and password.
- **Posts**: All users can view posts of public profiles. Authenticated users can also view private posts of followed users, edit or delete their own posts. Users can also filter posts by their owner and title.
- **Likes**: Authenticated users can like/unlike the posts and comments that doesnt belong to them.
- **Comments**: Authenticated users can comment on posts.
- **Follows**: Authenticated users can follow each other. Followers can also view private user's posts.
- **Chat**: Authenticated users can view their chat list, send messages to other users and delete those messages.

### Future Feature Ideas

- Allowing to update videos.
- Adding notifications on Like, Comments and Messages.
- Adding more security options to profile like email verifications etc.
- Adding online status of users.

## Design Process

### User Stories

1. As a user, I want to access an API endpoint that allows users to register by providing their username and password.
2. As a user, I want to access an API endpoint that allows users to log in, obtain an authentication token, and access user-specific content.
3. As a user, I want to be able to create, read, update user profiles by using API endpoints.
4. As a user using the API, I want a user profile to be automatically created, when a new user signs up for my application.
5. As a user, I want to be able to create, read, update and delete user posts by using API endpoints.
6. As a user, I want to be able to filter and order user posts.
7. As a user, I want to be able to create, read, update and delete user comments by using API endpoints.
8. As a user, I want to be able to filter user comments on a a specific post.
9. As a user, I want to be able to create, read, update and delete user likes by using API endpoints.
10. As a user, I want to be able to create, read and delete followers by using API endpoints.
11. As a user, I want to be able to filter followers of a specific profile.
12. As a user, I want to be able to create, read and delete chats by using API endpoints.
13. As a user, I want to be able to create, read and delete messages by using API endpoints.
14. As a user, I want to be able to filter all the messages of a specific chat.

### Data Models

![Entity Relationship Diagram](docs/ERM.png)

#### User Model

- The User model contains information about the user. It is part of the Django allauth library.
- One-to-one relation with the Profile model's owner field
- ForeignKey relation with the Post model's owner
- ForeignKey relation with the Comment model's owner
- ForeignKey relation with the PostLike model's owner
- ForeignKey relation with the CommentLike model's owner
- ForeignKey relation with the Follower model's owner
- ForeignKey relation with the Chat model's user1
- ForeignKey relation with the Chat model's user2
- ForeignKey relation with the Message model's owner

#### Profile Model

- The Profile model contains the following fields: owner, bio, image, created_at, updated_at, is_private
- Used cloudinary for image field.
- One-to-one relation between the owner field and User's id field

#### Post Model

- The Post model contains the following fields: owner, created_at, updated_at, title, content.
- ForeignKey relation with the Comment model's post field.
- ForeignKey relation with the PostLike model's post field.

#### Comment Model

- The Comment model contains the following fields: owner, post, created_at, updated_at, content.
- ForeignKey relation with the CommentLike model's comment field.

#### PostLike and CommentLike Models

- The PostLike and CommentLike models contain the following fields: owner, post(PostLike), comment(CommentLike), created_at.
- ForeignKey relation with the CommentLike model's comment field.

#### Follower Model

- The Follower model contains the following fields: owner, followed, created_at.

#### Chat Model

- The Chat model contains the following fields: user1, user2, created_at, last_message_time.
- ForeignKey relation with the Message model's chat field.

#### Message Model

- The Message model contains the following fields: chat, owner, timestamp, content.

## API Endpoints

The Socialize API provides the following endpoints:

| Endpoint                        | HTTP Method | CRUD   | View Type | Permissions   |
| ------------------------------- | ----------- | ------ | --------- | ------------- | --- |
| **Authentication and Profiles** |
| /api-auth/login/                | GET         | N/A    | N/A       | Public        |     |
|                                 | POST        | N/A    | N/A       | Public        |     |
| /api-auth/logout/               | GET         | N/A    | N/A       | Public        |     |
| /dj-rest-auth/registration/     | POST        | N/A    | N/A       | Public        |     |
| /dj-rest-auth/login/            | POST        | N/A    | N/A       | Public        |     |
| /dj-rest-auth/logout/           | POST        | N/A    | N/A       | Authenticated |     |
| /profiles/                      | GET         | Read   | List      | Public        |
| /profiles/\<int:pk\>/           | GET         | Read   | Detail    | Public        |     |
|                                 | PUT         | Update | Detail    | Owner         |     |
| **Posts Endpoints**             |
| /posts/                         | GET         | Read   | List      | Public        |
|                                 | POST        | Create | List      | Authenticated |     |
| /posts/\<int:pk\>/              | GET         | Read   | Detail    | Public        |     |
|                                 | PUT         | Update | Detail    | Owner         |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |
| **Likes Endpoints**             |
| /postlikes/                     | GET         | Read   | List      | Public        |     |
|                                 | POST        | Create | List      | Authenticated |     |
| /postlikes/\<int:pk\>/          | GET         | Read   | Detail    | Public        |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |
| /commentlikes/                  | GET         | Read   | List      | Public        |     |
|                                 | POST        | Create | List      | Authenticated |     |
| /commentlikes/\<int:pk\>/       | GET         | Read   | Detail    | Public        |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |
| **Comments Endpoints**          |
| /comments/                      | GET         | Read   | List      | Public        |
|                                 | POST        | Create | List      | Authenticated |     |
| /comments/\<int:pk\>/           | GET         | Read   | Detail    | Public        |     |
|                                 | PUT         | Update | Detail    | Owner         |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |
| **Followers Endpoints**         |
| /followers/                     | GET         | Read   | List      | Public        |     |
|                                 | POST        | Create | List      | Authenticated |     |
| /followers/\<int:pk>/           | GET         | Read   | Detail    | Public        |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |
| **Chat Endpoints**              |
| /chats/                         | GET         | Read   | List      | Authenticated |     |
|                                 | POST        | Create | List      | Authenticated |     |
| /chats/\<int:pk\>               | GET         | Read   | Detail    | Participant   |     |
|                                 | DELETE      | Delete | Detail    | Participant   |     |
| chats/\<int:chat_id>\/messages/ | GET         | Read   | List      | Participant   |     |
| messages/\<int:pk>\/            | GET         | Read   | Detail    | Owner         |     |
|                                 | DELETE      | Delete | Detail    | Owner         |     |

## Technologies Used

### Frameworks and Languages

- Python
- Django
- Django Rest Framework

### Python Packages

- cloudinary
- django-allauth
- django-cloudinary-storag
- django-cors-header
- django-filter
- djangorestframework-simplejw
- gunicorn
- psycopg
- pycparser
- PyJW

### Libraries & Tools

- [Am I Responsive](http://ami.responsivedesign.is/)
- [GitHub](https://github.com/)
- [Heroku Platform](https://id.heroku.com/login)
- [Postgres](https://www.postgresql.org/)
- [Allauth](https://docs.allauth.org/en/latest/)
- [CI Python Linter](https://pep8ci.herokuapp.com/)

## Validation

[CI Python Linter](https://pep8ci.herokuapp.com/) from Code Institute used for validation. All errors are fixed.

## Testing

| **Test** | **Action**                   | **Expected Result**                                   | **Actual Result** |
| -------- | ---------------------------- | ----------------------------------------------------- | ----------------- |
| User     | Create user                  | User account can be created                           | Works as expected |
| User     | Change username and password | Logged in user can change username and password       | Works as expected |
| Profile  | Create profile               | Automatically create a profile when a user is created | Works as expected |
| Profile  | Edit profile                 | Profile owner can edit profile information            | Works as expected |
| Post     | Create post                  | Logged in user can create post                        | Works as expected |
| Post     | Update and Delete            | Post owner can edit and delete post                   | Works as expected |
| Comment  | Create comment               | Logged in user can comment on posts                   | Works as expected |
| Comment  | Update and delete comment    | Comment owner can edit and delete comment             | Works as expected |
| Likes    | Create likes                 | Logged in user can like post and comments likes       | Works as expected |
| Likes    | Delete likes                 | Like owner can delete post and comment likes          | Works as expected |
| Follower | Create                       | Logged in user can follow an unfollowed profile       | Works as expected |
| Follower | Delete                       | Logged in user can unfollow a followed profile        | Works as expected |
| Chat     | Create chat                  | Logged in user can start chat with other users        | Works as expected |
| Chat     | Delete chat                  | Chat participants can delete existing chat            | Works as expected |
| Message  | Create message               | Logged in users can send message to other users       | Works as expected |
| Message  | Delete message               | Message owner can delete message.                     | Works as expected |

## Deployment

The project was deployed to [Heroku](https://heroku.com). A live version of the API can be found at https://socialize-backend-app-9beed826b5f2.herokuapp.com/.

The necessary steps to deploy the project are:

1. Clone or fork the repository. For forking it, go to https://github.com/oguzhanakca/socialize-backend, click on `Fork` and follow the instructions. For cloning the repository run `git clone https://github.com/oguzhanakca/socialize-backend.git` in your terminal.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-1.png">
</details>

2. Create an account at https://cloudinary.com and get your Cloudinary URL from the dashboard by clicking on the button `Go To API Keys`.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-2.png">
<img src="docs/deployment/deployment-3.png">
</details>

3. Create a PostgreSQL database, for example at https://www.elephantsql.com/. Create an account and after login in, click on `Create new instance` and follow the instructions. The database used in this project is created from Code Institute.

4. Create an account at https://heroku.com and login. Then, start a new app from the [Heroku dashboard](https://dashboard.heroku.com) by clicking on `New` and then on `Create new app`.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-4.png">
</details>

5. Give your app an available name and choose your region (US or Europe).

6. After creating your app, go to the _Settings_ tab and click on `Reveal Config Vars` in the _Config Vars_ section.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-5.png">
</details>

7. Now, one by one, add the following config vars:

   | Name                  | Value                                   |
   | --------------------- | --------------------------------------- |
   | ALLOWED_HOSTS         | \<your deployed heroku API app url\> \* |
   | CLIENT_ORIGIN         | \<your client url\>                     |
   | CLOUDINARY_URL        | \<Your cloudinary url\>                 |
   | DATABASE_URL          | \<Your database url\>                   |
   | DISABLE_COLLECTSTATIC | 1                                       |
   | SECRET_KEY            | \<some random string\>                  |

   \* Paste the URL without 'https://' or a trailing slash!
   <details>
   <summary>Show image</summary>
   <img src="docs/deployment/deployment-6.png">
   </details>

8. Click on the _Deploy_ tab and connect the Heroku app to your GitHub repository.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-7.png">
</details>

9. Scroll down and choose the branch you want to deploy in the _Manual deploy_ section. Now click on `Deploy Branch` for the first deployment of the application.

<details>
<summary>Show image</summary>
<img src="docs/deployment/deployment-8.png">
</details>

10. After deployment click on `View` to open your deployed app.

    <details>
    <summary>Show image</summary>
    <img src="docs/deployment/deployment-9.png">
    </details>

## Credits

This project was created based on the Code Institute's Django REST API walkthrough project [Moments](https://github.com/Code-Institute-Solutions/drf-api).

- [Django documentation](https://www.djangoproject.com/)
- [Django Rest Framework documentation](https://www.django-rest-framework.org/)
- [Cloudinary documentation](https://cloudinary.com/documentation)
