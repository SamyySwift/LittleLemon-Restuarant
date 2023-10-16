# LittleLemonAPI REST API Documentation

This document provides information about the REST API endpoints, their allowed permissions, and URLs for the LittleLemonAPI project. This project offers a restaurant management system, including features for menu items, user groups, shopping carts, and orders.
## Environment Setup

- Clone the repo
- Run `pipenv install` to install all required packages
- Don't forget to set the database to connect to your own database
- Run `python manage.py migrate` to migrate the tables to a new database
- `Run python manage.py runserver` to start the server


## API Endpoints

### Categories

- URL: `/api/menu-items`
- Methods:
    - `GET`: Retrieve a list of all available menu categories.
    - `POST`: Create a new menu category.
- Permissions:
    - `GET`: Public access.
    - `POST`: Requires authentication.

### Menu Items

- URL: `/api/menu-items`
- Methods:
    - `GET`: Retrieve a list of all menu items.
    - `POST`: Create a new menu item.
- Permissions:
    - `GET`: Public access.
    - `POST`: Only accessible to users with the "Manager" role.

### Single Menu Item

- URL: `/api/menu-items/<int:pk>`
- Methods:
    - `GET`: Retrieve details of a specific menu item.
    - `PUT`: Update details of a specific menu item.
    - `DELETE`: Delete a specific menu item.
- Permissions:
    - `GET`: Public access.
    - `PUT` and `DELETE`: Only accessible to users with the "Manager" role.

### Manager Group Users

- URL: `/api/groups/manager/users`
- Methods:
    - `GET`: Retrieve a list of users in the "Manager" group.
    - `POST`: Add a user to the "Manager" group.
    - `DELETE`: Remove a user from the "Manager" group.
- Permissions:
    - `GET`: Requires admin user access.
    - `POST` and `DELETE`: Requires admin user access.

### Delivery Crew Users

- URL: `/api/groups/delivery-crew/users`
- Methods:
    - `GET`: Retrieve a list of users in the "Delivery Crew" group.
    - `POST`: Add a user to the "Delivery Crew" group.
    - `DELETE`: Remove a user from the "Delivery Crew" group.
- Permissions:
    - `GET`: Requires authentication, accessible to admin users and "Managers."
    - `POST` and `DELETE`: Requires admin user access.

### Shopping Cart

- URL: `/api/cart/menu-items`
- Methods:
    - `GET`: Retrieve the shopping cart items for the authenticated user.
    - `POST`: Add items to the shopping cart for the authenticated user.
    - `DELETE`: Empty the shopping cart for the authenticated user.
- Permissions:
    - `GET`, `POST`, and `DELETE`: Requires authentication.

### Orders

- URL: `/api/orders`
- Methods:
    - `GET`: Retrieve a list of orders based on user roles.
    - `POST`: Create a new order based on the items in the shopping cart.
- Permissions:
    - `GET`: 
        - Public access for superusers.
        - Accessible to normal customers for their own orders.
        - Accessible to delivery crew for orders assigned to them.
        - Accessible to "Managers" and "Delivery Crew" for all orders.
    - `POST`: Requires authentication. 

### Single Order

- URL: `/api/orders/<int:pk>`
- Methods:
    - `GET`: Retrieve details of a specific order.
    - `PUT`: Update details of a specific order (restricted to "Managers" and admin users).
    - `DELETE`: Delete a specific order (restricted to "Managers" and admin users).
- Permissions:
    - `GET`: Public access.
    - `PUT` and `DELETE`: Only accessible to users with the "Manager" or admin roles.

## Permissions

- `IsAuthenticated`: Requires the user to be authenticated.
- `IsAdminUser`: Requires the user to be an admin.
- `IsManager`: Requires the user to be in the "Manager" group.
- `IsManager | IsAdminUser`: Requires the user to be in the "Manager" group or an admin.

## URLs

- API endpoints are prefixed with `/api`.
- Authentication and user-related endpoints are handled by DJOSER and include token-based authentication.

## API Throttling

This API implements throttling for rate limiting to protect against abuse.
