# AI Song Generation Platform - REST API Documentation

This document outlines the RESTful API endpoints available in the AI Song Generation Platform backend. These endpoints are built using **Django REST Framework** and are located under the base URL `http://127.0.0.1:8000/api/`.

---

## Song Management Endpoints

### 1. List All Songs
* **URL:** `/api/songs/`
* **Method:** `GET`
* **Permissions:** Allow Any (Guests see only Complete+Public songs. Logged-in users also see their private/generating songs).
* **Response:**
  ```json
  [
    {
      "id": 1,
      "owner": "user@example.com",
      "title": "My Summer Track",
      "genre": "pop",
      "status": "complete",
      "visibility": "public"
    }
  ]
  ```

### 2. Create a Song
* **URL:** `/api/songs/`
* **Method:** `POST`
* **Permissions:** IsAuthenticated
* **Payload Structure:**
  ```json
  {
    "genre": "rock",
    "story": "A depression song about coding late at night.",
    "mood": "sad",
    "language": "English"
  }
  ```

### 3. Retrieve Specific Song
* **URL:** `/api/songs/<id>/`
* **Method:** `GET`
* **Permissions:** AllowAny (If Public) or IsOwner 

### 4. Update a Song
* **URL:** `/api/songs/<id>/`
* **Method:** `PATCH`
* **Permissions:** IsOwnerOrAdmin
* **Description:** Update specific fields of a song, such as visibility or title.
* **Payload Structure:**
  ```json
  {
    "visibility": "public",
    "title": "My Updated Song Name"
  }
  ```

### 5. Delete a Song
* **URL:** `/api/songs/<id>/`
* **Method:** `DELETE`
* **Permissions:** IsOwnerOrAdmin
* **Response:** `204 No Content`

---

## 🛠 Admin & Analytics Endpoints

### 6. Admin Analytics View
* **URL:** `/api/admin/analytics/songs/`
* **Method:** `GET`
* **Permissions:** IsAdminRole (Restricted directly in `permissions.py`)
* **Description:** Retrieves metrics for the Admin Dashboard to graph platform usage data.
* **Response:**
  ```json
  {
    "total_songs": 150,
    "complete_songs": 120,
    "generating_songs": 10,
    "failed_songs": 20
  }
  ```

---

## Authentication & Permissions Handled
The API uses Session/Basic Auth for current demonstrations. Permissions are explicitly locked down using customized classes:
* `IsOwnerOrAdmin` — Ensures a normal user can only PATCH/DELETE their *own* tracks, while giving Admins global override powers.
* `IsAdminRole` — Locks down analytical and moderation endpoints so only users with `role="admin"` can fetch platform statistics.

## Screenshots
[AI Song Generation Platform API Screenshots Folder](https://drive.google.com/drive/folders/1hq8iH9Hz9Kakw7-3cq14rM-oMO75t715?usp=share_link)