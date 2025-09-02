CREATE DATABASE IF NOT EXISTS mood_journal;
USE mood_journal;

CREATE TABLE IF NOT EXISTS journal_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_text TEXT NOT NULL,
    happy FLOAT,
    sad FLOAT,
    angry FLOAT,
    surprise FLOAT,
    fear FLOAT,
    love FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO journal_entries (entry_text, happy, sad, angry, surprise, fear, love) VALUES
('Had a great day today! The weather was beautiful and I got to spend time with friends. We went hiking and had a picnic. Feeling grateful for these moments.', 92, 5, 2, 15, 3, 85),
('Felt a bit overwhelmed with work today. Need to practice better time management. Also, I need to learn to say no to additional responsibilities when I''m already stretched thin.', 15, 78, 25, 10, 45, 20),
('Today was a mix of emotions. I was surprised by a birthday party my friends threw for me. It was amazing but I was also anxious about all the attention.', 70, 10, 5, 85, 40, 75),
('I felt angry and frustrated today because of a misunderstanding at work. I need to work on communicating more clearly and not letting small things bother me so much.', 10, 30, 85, 5, 20, 15);