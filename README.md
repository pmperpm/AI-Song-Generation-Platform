# AI Song Generation Platform

**AI Song Generation Platform** empowers users to generate custom songs using AI by simply providing details like genre, mood, lyrics, and story. From there, it tracks generation progress, saves the completed audio for offline listening, and allows users to build personalized playlists. 

## How to Run the Project

1. **Clone the repository and set up a Virtual Environment:**
   ```bash
   git clone https://github.com/pmperpm/AI-Song-Generation-Platform.git
   cd AI-Song-Generation-Platform/backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations (Build the Database):**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. **Create a Superuser (Admin Access):**
   ```bash
   python3 manage.py createsuperuser
   ```
   *Follow the prompts (Username, Email, Role).*

5. **Run the Server:**
   ```bash
   python3 manage.py runserver
   ```
   backend will now be live at `http://127.0.0.1:8000/`.

---

## CRUD Operations 

All Create, Read, Update, and Delete operations are performed inside the **Django Admin Interface**. 

Navigate to **http://127.0.0.1:8000/admin/** and log in with your Superuser.

### Users (`/admin/users/user/`)
* **Create/Update:** Add users without passwords (setup for Google OAuth integration). Assign roles (User vs Admin).
* **Read:** Easily seek users by email.
* **Delete:** Remove accounts and automatically cascade deletions for all their songs.

### Songs (`/admin/songs/song/`)
* **Create:** Simulate generating a song. It must be attached to an owner.
* **Update:** Alter visibility (Private/Public) or add custom cover artwork.
* **Read:** Filter tracks securely by Status (`Generating`, `Complete`, `Fail`), or by Visibility.
* **Delete:** Administrators can delete generated media in case of violations.

### Playlists (`/admin/playlists/playlist/`)
* **Create/Update:** Select your previously generated tracks using the horizontal selection menu.
* **Validation:** The system strictly checks to make sure songs belong to the Playlist owner and possess a status of `Complete`.
* **Read/Delete:** Keep track of personal library structures. Deleting a playlist never deletes the origin songs.

### CRUD Operation Video
[AI Song Generation Platform CRUD Video](https://drive.google.com/file/d/1OBpWr6yC_XO12VS6znQ4s5BMrcgKwJcv/view?usp=sharing)