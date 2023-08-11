import sqlite3

class Task:
    def __init__(self, title, due_date, alarm):
        self.title = title
        self.due_date = due_date
        self.alarm = alarm

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class Agenda:
    def __init__(self, db_name="agenda.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    alarm TEXT NOT NULL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')

    def add_task(self, task):
        with self.conn:
            self.conn.execute(
                'INSERT INTO tasks (title, due_date, alarm) VALUES (?, ?, ?)',
                (task.title, task.due_date, task.alarm)
            )

    def add_note(self, note):
        with self.conn:
            self.conn.execute(
                'INSERT INTO notes (title, content) VALUES (?, ?)',
                (note.title, note.content)
            )

    def get_tasks(self):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM tasks')
            tasks = [Task(row[1], row[2], row[3]) for row in cursor]
            return tasks

    def get_notes(self):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM notes')
            notes = [Note(row[1], row[2]) for row in cursor]
            return notes

    def delete_task(self, task_id):
        with self.conn:
            self.conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    def delete_note(self, note_id):
        with self.conn:
            self.conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))

def print_menu():
    print("\nMenu:")
    print("1. Ajouter une tâche")
    print("2. Ajouter une note")
    print("3. Afficher les tâches")
    print("4. Afficher les notes")
    print("5. Supprimer une tâche")
    print("6. Supprimer une note")
    print("7. Quitter")

def display_tasks(tasks):
    if tasks:
        print("Tâches :")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task.title} - Date limite : {task.due_date} - Alarme : {task.alarm}")
    else:
        print("Il n'y a pas de tâches enregistrées.")

def display_notes(notes):
    if notes:
        print("Notes :")
        for idx, note in enumerate(notes, start=1):
            print(f"{idx}. {note.title} :\n{note.content}")
    else:
        print("Il n'y a pas de notes enregistrées.")

def main():
    agenda = Agenda()

    while True:
        print_menu()
        choice = input("Choisissez une option (1-7) : ")

        try:
            if choice == "1":
                title = input("Entrez le titre de la tâche : ")
                due_date = input("Entrez la date limite de la tâche (AAAA-MM-JJ) : ")
                alarm = input("Entrez l'heure de l'alarme pour la tâche (HH:MM) : ")
                task = Task(title, due_date, alarm)
                agenda.add_task(task)
                print("Tâche ajoutée avec succès!")

            elif choice == "2":
                title = input("Entrez le titre de la note : ")
                content = input("Entrez le contenu de la note : ")
                note = Note(title, content)
                agenda.add_note(note)
                print("Note ajoutée avec succès!")

            elif choice == "3":
                tasks = agenda.get_tasks()
                display_tasks(tasks)

            elif choice == "4":
                notes = agenda.get_notes()
                display_notes(notes)

            elif choice == "5":
                task_id = int(input("Entrez l'ID de la tâche à supprimer : "))
                agenda.delete_task(task_id)
                print("Tâche supprimée avec succès!")

            elif choice == "6":
                note_id = int(input("Entrez l'ID de la note à supprimer : "))
                agenda.delete_note(note_id)
                print("Note supprimée avec succès!")

            elif choice == "7":
                print("Au revoir!")
                break

            else:
                print("Option invalide. Veuillez réessayer.")

        except ValueError:
            print("Veuillez entrer un ID valide (nombre entier) pour supprimer une tâche ou une note.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()