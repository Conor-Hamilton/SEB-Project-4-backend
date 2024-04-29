# 11th-Planet-JiuJitsu

## Description

11th-Planet-JiuJitsu, a solo project, represents the culmination of the skills I've acquired during the last module of my GA Software Engineering Bootcamp. It is a full-stack application that simulates the operations of a martial arts gym, allowing users to view and book classes. The backend was developed using Python, Flask, SQLAlchemy, and PostgreSQL, while the frontend was built with React, TypeScript, and Tailwind CSS.

## Deployment link

The app is deployed and can be accessed at:

[11th-Planet-JiuJitsu](https://11th-planet-jiujitsu.netlify.app/)

## Getting Started/Code Installation

To clone the project up and running on your local machine, follow these instructions:

#### 1. Clone the repo:

- `git clone git@github.com:Conor-Hamilton/SEB-Project-4-frontend.git`
- `git clone git@github.com:Conor-Hamilton/SEB-Project-4-backend.git`

#### 2. Install backend dependencies:

- `pipenv install`

#### 3. Start the backend server:

- `pipenv run flask run`

#### 4. In a new terminal, navigate to the frontend directory and install dependencies:

- `cd project-4-frontend`
- `npm install`

#### 5. Start the React development server:

- `npm run dev`

## Timeframe & Working Team (Solo)

This was a solo project that spanned 8 working days.

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, PostgreSQL
- **Frontend**: React, TypeScript, Tailwind CSS
- **Dev Tools**: Git, GitHub, Heroku, Netlify

## Brief

The brief required building a full-stack application with a Python Flask API backend serving data from a PostgreSQL database and a separate React front-end consuming this API. The project was to include multiple relationships and CRUD functionality.

## Planning

My planning process included:

- Sketching initial user flow diagrams.
- Creating wireframes for UI layout.
- Developing Entity Relationship Diagrams (ERDs) to model database schemas.

![Wireframing](/assets/wireframing.png)

## Build/Code Process

Throughout the build process, I prioritized writing clean and maintainable code. Here are some highlights:

- **User Authentication**: Implementing secure login functionality with password hashing.

Below are the code snippets demonstrating how this was achieved using `bcrypt` for password hashing in the `UserModel` and a `secureRoute` middleware to protect routes that require a logged-in user.

```python
# models/user.py

from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt
from associations import users_user_types

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=True)
    user_types = db.relationship(
        "UserType", secondary="users_user_types", back_populates="users"
    )

    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password).decode(
            "utf-8"
        )

    def validate_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)
```

```python
# middleware/secureRoute.py

from flask import request, abort
from models.user import UserModel
import jwt
from environment.config import secret

def secure_route(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, description='Unauthorized')

        try:
            token = token.replace('Bearer ', '')
            decoded_token = jwt.decode(token, secret)
            user = UserModel.query.get(decoded_token['sub'])
            if not user:
                abort(401, description='User not found')
        except jwt.ExpiredSignatureError:
            abort(401, description='Token expired')
        except Exception as e:
            abort(401, description=str(e))

        return func(user, *args, **kwargs)

    return wrapper
```

- **Role-Based Access Control**: Enforcing different permissions for admin, coach, and customer roles.

Ensuring that users have access only to the features and data appropriate to their roles is crucial for the security and functionality of the application. Below are examples of how RBAC was implemented for the `admin`, `coach`, and `customer` roles.

```python
# models/user.py

    @hybrid_property
    def is_admin(self):
        return any(u_type.name == 'Admin' for u_type in self.user_types)

    @hybrid_property
    def is_coach(self):
        return any(u_type.name == 'Coach' for u_type in self.user_types)
```

In the create_class function, I check that the user making the request has the necessary role by checking g.current_user.is_admin or g.current_user.is_coach. If the user does not have the appropriate role, an unauthorized response is returned. This pattern is applied consistently across the application to secure all sensitive endpoints.

```python
@classes_controller.route("/classes", methods=["POST"])
@secure_route
def create_class():
    class_data = request.get_json()

    # Check if the current user is either an admin or a coach
    if not (g.current_user.is_admin or g.current_user.is_coach):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        # Load the class data and assign the current user as the creator
        class_ = class_schema.load(class_data)
        class_.creator = g.current_user
        db.session.add(class_)
        db.session.commit()
        return class_schema.jsonify(class_), HTTPStatus.CREATED

    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        logging.exception("An error occurred while creating a class.")
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
```

This snippet illustrates how the frontend adheres to the security rules defined by the backend.

### Conditional Rendering in User Profile

User experience is tailored based on user roles. The profile interface dynamically adjusts, displaying options like 'Create Class' or 'Edit Class' only if the user is an `Admin` or `Coach`. The snippet below from the `UserProfile` component demonstrates this conditional rendering:

```typescript
export default function UserProfile({ user }: IUserProfile) {
const [userRoles, setUserRoles] = useState<string[]>([]);

  // Fetch user roles and set up state based on the roles
  useEffect(() => {
    const fetchUserRoles = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await axios.get(`${baseUrl}/current_user_type`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUserRoles(response.data.type);
        } catch (error) {
          console.error("Error fetching user roles:", error);
        }
      }
    };

    fetchUserRoles();
  }, []);
```

```jsx
  return (
    <div className="container mx-auto p-6">
      <ul className="mb-5 flex list-none" role="tablist">

        {(userRoles.includes("Admin") || userRoles.includes("Coach")) && (
          <>
            <li role="presentation">
              <button
                className={getTabClass("createClass")}
                onClick={() => setActiveTab("createClass")}
              >
                Create Class
              </button>
            </li>
            <li role="presentation">
              <button
                className={getTabClass("editClass")}
                onClick={() => setActiveTab("editClass")}
              >
                Edit Class
              </button>
            </li>
          </>
        )}
      </ul>
  );
```

## Challenges

- Wearing multiple hats during a solo project was a significant challenge. Balancing roles as a developer, designer, UX specialist, and project manager, especially with limited prior experience in these areas, was tough but incredibly rewarding.

- One technical challenge involved managing the relationships between users, admins, coaches, and user types. Initially, the setup was not facilitating the features I needed effectively. To address this, I delved deeper into database design and implemented a many-to-many associations table, which helped establish clear and functional relationships necessary for the application. Here is how I structured the associations table:

```python
from app import db

# Association table for the many-to-many relationship between users and user types
users_user_types = db.Table(
    "users_user_types",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "user_type_id", db.Integer, db.ForeignKey("user_types.id"), primary_key=True
    ),
)
```

## Wins

- Successfully launching a full-stack app solo and solidifying my understanding of backend technologies were major achievements.

- The design, inspired by professional gym sites, is something I'm particularly proud of.

- Achieving responsiveness across all devices, using Tailwind CSS. I'm proud of how well I've managed to provide a great user experience regardless of device.

## Bugs

- The password change feature, which was a late addition to my project, currently does not verify the existing password against its hash in the database. This is a security issue that I plan to address by implementing additional validation steps to ensure password changes are authenticated more securely.

## Future Improvements

- Introduce functionality for users to cancel bookings.
- Create tier-based memberships with varying access levels.
- Have a fully functioning shop element to the website.

## Key Learnings/Takeaways

- Given this was my first project using this tech stack it helped me solidify my understanding of it and it has motivated me to go deeper into learning more.

- The experience has helped build my foundation in managing full-stack development independently.

