#  Funcționalități implementate - Flask Backend pentru Scheduler

Acest backend oferă un set de funcții pentru gestionarea utilizatorilor și a evenimentelor într-o aplicație de tip calendar. Mai jos sunt prezentate toate funcțiile implementate și rolul lor:

---

##  `create_user()`
- **Endpoint:** `POST /create_user`
- **Scop:** Creează un utilizator nou dacă nu există deja.
- **Input:** JSON cu `email`
- **Output:** Mesaj de confirmare sau existență

---

##  `get_users()`
- **Endpoint:** `GET /users`
- **Scop:** Returnează lista tuturor utilizatorilor din baza de date.

---

##  `get_user_id()`
- **Endpoint:** `GET /get_user_id?email=<email>`
- **Scop:** Returnează ID-ul unui utilizator pe baza adresei de email.

---

##  `create_event()`
- **Endpoint:** `POST /events`
- **Scop:** Creează un eveniment nou în baza de date.
- **Funcționalități:**
  - Creează eveniment cu titlu, descriere, interval orar și organizator.
  - Asociază participanți (`attendees`) existenți în baza de date pe baza email-ului.
  - Stochează opțional `google_event_id`.

---

##  `get_events(user_id)`
- **Endpoint:** `GET /events/<user_id>`
- **Scop:** Returnează toate evenimentele la care utilizatorul participă sau este organizator.

---

##  `edit_event(event_id)`
- **Endpoint:** `PUT /events/<event_id>`
- **Scop:** Editează un eveniment existent.
- **Restricții:** Doar organizatorul poate modifica evenimentul.
- **Actualizări posibile:**
  - Titlu, descriere
  - Ora de început / sfârșit
  - Lista completă de participanți

---

##  `delete_event(event_id)`
- **Endpoint:** `DELETE /events/<event_id>?organizer_id=<id>`
- **Scop:** Șterge un eveniment.
- **Restricții:** Doar organizatorul poate șterge evenimentul.

---

##  `hello_world()`
- **Endpoint:** `GET /`
- **Scop:** Verificare simplă că API-ul rulează (răspunde cu mesaj static).

---

##  Altele
- Folosește SQLAlchemy pentru ORM și relații între tabele (`Event` și `SupaUser`)
- Include suport pentru CORS pentru integrarea cu un frontend (ex. React)
- Tabele create automat la pornirea aplicației (`db.create_all()`)

---

 Codul este pregătit pentru extindere cu autentificare, integrare completă cu Google Calendar sau funcționalități de notificare.
