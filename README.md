# 💬 PYE-api

The PYE App is a web-based application designed to help users enhance their English language skills by practicing vocabulary.

> Developed with **Flask**🔩 (and python packages) and the default database is **PostgreSQL**🐘.

## ▶️ How to Run

To run the project, follow these steps:

1. Clone this repository to your local machine.

```bash
git clone https://github.com/cristian1clj/PYE-api.git
```

2. Navigate to the project directory.

```bash
cd PYE-api
```

3. Create a new python virtual environment with the python version to the project (3.8) and activate the venv.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8
sudo apt install python3.8-venv
python3.8 -m venv .venv
source .venv/bin/activate
```

4. Install the required requirements.

```bash
pip3 install -r requirements.txt
```

5. Add these scripts in .venv/bin/activate.

```bash
export FLASK_APP="entrypoint:app"
export FLASK_ENV="development"
export APP_SETTINGS_MODULE="config.default"
```

6. Create the PYE database in PostgreSQL, create the user, and grant it privileges.
    > *You can change the user and password, but you should also change them in the project's config/default.py*

```bash
CREATE DATABASE pye;
CREATE USER admin;
ALTER USER admin WITH ENCRYPTED PASSWORD '12345';
GRANT ALL PRIVILEGES ON DATABASE pye TO admin;
```

7. Create database tables using Flask-Migrate extension.

```bash
flask db init
flask db migrate -m "Initial_db"
flask db upgrade
```

8. Run the project.
```bash
flask run
```

## 📃 Documentation(endpoints)

<table>
  <tr>
    <th>TAGS</th>
    <th>METHODS</th>
    <th>ENDPOINTS</th>
    <th>DESCRIPTION</th>
    <th>AUTH TOKEN?</th>
    <th>REQUEST BODY</th>
    <th>RESPONSE</th>
  </tr>
  <tr>
    <td rowspan="3">Auth</td>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/auth/signup</td>
    <td>Signup</td>
    <td>❌</td>
    <td>
      {<br>
      "username": string,<br>
      "email": string,<br>
      "password": string<br>
      }
    </td>
    <td>
      {<br>
      "id": int,<br>
      "username": string,<br>
      "email": string,<br>
      "suggestions": [],<br>
      "vocabulary_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/auth/login</td>
    <td>Login</td>
    <td>❌</td>
    <td>
      {<br>
      "email": string,<br>
      "password": string<br>
      }
    </td>
    <td>
      {<br>
      "token": string,<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/auth/session</td>
    <td>Validate active session</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      boolean
    </td>
  </tr>
  <tr>
    <td rowspan="2">Categories</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/categories/</td>
    <td>Query all categories</td>
    <td>❌</td>
    <td>
      ----
    </td>
    <td>
      [<br>
        {<br>
          "id": int,<br>
          "name": string,<br>
          "words": [],<br>
          "suggestions": [],<br>
          "vocabulary_difficulty": []<br>
          "suggestions": []<br>
        },<br>
      ]
    </td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/categories/</td>
    <td>Add category</td>
    <td>✔️</td>
    <td>
      {<br>
      "name": string<br>
      }
    </td>
    <td>
      {<br>
      "id": int,<br>
      "name": string,<br>
      "words": []<br>
      "suggestions": []<br>
      }
    </td>
  </tr>
  <tr>
    <td rowspan="5">Difficulty</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/vocabulary/difficulty/</td>
    <td>Query all difficulties</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      [<br>
        {<br>
          "user_id": int,<br>
          "word_id": int,<br>
          "difficulty_level": int<br>
        },<br>
      ]
    </td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/vocabulary/difficulty/</td>
    <td>Add difficulty</td>
    <td>✔️</td>
    <td>
      {<br>
        "user_id": int,<br>
        "word_id": int<br>
      },<br>
    </td>
    <td>
      {<br>
        "user_id": int,<br>
        "word_id": int,<br>
        "difficulty_level": int<br>
      }<br>
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/vocabulary/difficulty/user/**user_id**/word/**word_id**</td>
    <td>Query difficulty</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "user_id": int,<br>
        "word_id": int,<br>
        "difficulty_level": int<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #fca130; color: white">PUT</td>
    <td>/api/vocabulary/difficulty/user/**user_id**/word/**word_id**</td>
    <td>Modify difficulty</td>
    <td>✔️</td>
    <td>
      {<br>
        "difficulty_level": int<br>
      }
    </td>
    <td>
      {<br>
        "user_id": int,<br>
        "word_id": int,<br>
        "difficulty_level": int<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #f93e3e; color: white">DELETE</td>
    <td>/api/vocabulary/difficulty/user/**user_id**/word/**word_id**</td>
    <td>Delete difficulty</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "message": "Difficulty deleted"<br>
      }
    </td>
  </tr>
  <tr>
    <td rowspan="5">Suggestions</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/suggestions/</td>
    <td>Query all suggestions</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      [<br>
        {<br>
          "id": int,<br>
          "word": string,<br>
          "meaning": string,<br>
          "category_id": int,<br>
          "punctuation": int,<br>
          "date_suggestion": string<br>
        },<br>
      ]
    </td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/suggestions/</td>
    <td>Add suggestion</td>
    <td>✔️</td>
    <td>
      {<br>
        "word": string,<br>
        "meaning": string,<br>
        "category_id": int,<br>
        "user_id": int<br>
      }
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meaning": string,<br>
        "category_id": int,<br>
        "user_id": int,<br>
        "punctuation": int,<br>
        "date_suggestion": string<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/suggestions/**suggestion_id**</td>
    <td>Query suggestion</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meaning": string,<br>
        "category_id": int,<br>
        "user_id": int,<br>
        "punctuation": int,<br>
        "date_suggestion": string<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #fca130; color: white">PUT</td>
    <td>/api/suggestions/**suggestion_id**</td>
    <td>Modify suggestion</td>
    <td>✔️</td>
    <td>
      {<br>
        "word": string,<br>
        "meaning": string,<br>
        "category_id": int,<br>
        "user_id": int,<br>
        "punctuation": int<br>
      }
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meaning": string,<br>
        "category_id": int,<br>
        "user_id": int,<br>
        "punctuation": int,<br>
        "date_suggestion": string<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #f93e3e; color: white">DELETE</td>
    <td>/api/suggestions/**suggestion_id**</td>
    <td>Delete suggestion</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "message": "Suggestion deleted"<br>
      }
    </td>
  </tr>
  <tr>
    <td rowspan="4">Users</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/users/</td>
    <td>Query all users</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      [<br>
        {<br>
          "id": int,<br>
          "username": string,<br>
          "email": string,<br>
          "suggestions": [],<br>
          "vocabulary_difficulty": []<br>
        },<br>
      ]
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/users/**user_id**</td>
    <td>Query user</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "id": int,<br>
        "username": string,<br>
        "email": string,<br>
        "suggestions": [],<br>
        "vocabulary_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #fca130; color: white">PUT</td>
    <td>/api/users/**user_id**</td>
    <td>Modify user</td>
    <td>✔️</td>
    <td>
      {<br>
        "username": string,<br>
        "email": string<br>
      }
    </td>
    <td>
      {<br>
        "id": int,<br>
        "username": string,<br>
        "email": string,<br>
        "suggestions": [],<br>
        "vocabulary_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #f93e3e; color: white">DELETE</td>
    <td>/api/users/**user_id**</td>
    <td>Delete user</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "message": "User deleted"<br>
      }
    </td>
  </tr>
  <tr>
    <td rowspan="6">Vocabulary</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/vocabulary/</td>
    <td>Query all vocabulary</td>
    <td>❌</td>
    <td>
      ----
    </td>
    <td>
      [<br>
        {<br>
          "id": int,<br>
          "word": string,<br>
          "meanings": [],<br>
          "category_id": int,<br>
          "user_difficulty": int<br>
        },<br>
      ]
    </td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/vocabulary/</td>
    <td>Add word</td>
    <td>✔️</td>
    <td>
      {<br>
        "word": string,<br>
        "meanings": [<br>
          { "meaning": string },<br>
        ],<br>
        "category_id": int<br>
      }
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meanings": [],<br>
        "category_id": int,<br>
        "user_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/vocabulary/word/**word_id**</td>
    <td>Query word</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meanings": [],<br>
        "category_id": int,<br>
        "user_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #fca130; color: white">PUT</td>
    <td>/api/vocabulary/word/**word_id**</td>
    <td>Modify word</td>
    <td>✔️</td>
    <td>
      {<br>
        "word": string,<br>
        "meanings": [<br>
          { "meaning": string },<br>
        ],<br>
        "category_id": int<br>
      }
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meanings": [],<br>
        "category_id": int,<br>
        "user_difficulty": []<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #f93e3e; color: white">DELETE</td>
    <td>/api/vocabulary/word/**word_id**</td>
    <td>Delete word</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "message": "Word deleted"<br>
      }
    </td>
  </tr>
  <tr>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/vocabulary/category/**category_id**/random</td>
    <td>Random word</td>
    <td>✔️</td>
    <td>
      ----
    </td>
    <td>
      {<br>
        "id": int,<br>
        "word": string,<br>
        "meanings": [],<br>
        "category_id": int,<br>
        "user_difficulty": []<br>
      }
    </td>
  </tr>
</table>
