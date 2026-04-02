from collections import defaultdict


DIFFICULTY_LABELS = {
    "amateur": "Amateur",
    "enthusiast": "Enthusiast",
    "professional": "Professional",
    "expert": "Expert",
}

CATEGORY_LABELS = {
    "science": "Science",
    "current_affairs": "Current Affairs",
    "cricket": "Cricket",
    "international_football": "International Football",
    "bollywood": "Bollywood Movies",
    "international_movies": "International Movies",
    "art_literature": "Art and Literature",
    "politics": "Politics",
    "history": "History",
    "finance": "Finance",
    "economics": "Economics",
}

PROMPT_PREFIXES = [
    "",
    "Choose the correct answer: ",
    "Pick the right option: ",
    "Select the correct answer: ",
    "Identify the right answer: ",
]

BASE_QUESTIONS = [
    ("science", "amateur", "Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Mercury"], 0),
    ("science", "amateur", "What gas do plants absorb from the atmosphere?", ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"], 0),
    ("science", "enthusiast", "What is the chemical symbol for sodium?", ["Na", "So", "Sd", "Sm"], 0),
    ("science", "enthusiast", "Which part of the cell contains genetic material?", ["Nucleus", "Ribosome", "Membrane", "Cytoplasm"], 0),
    ("science", "professional", "Which blood cells help in clotting?", ["Platelets", "Plasma", "Neutrophils", "Red cells"], 0),
    ("science", "professional", "What is the speed of light closest to?", ["300,000 km/s", "30,000 km/s", "3,000 km/s", "3,000,000 km/s"], 0),
    ("science", "expert", "Which scientist proposed the three laws of motion?", ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Niels Bohr"], 0),
    ("science", "expert", "What is the hardest natural substance?", ["Diamond", "Granite", "Quartz", "Iron"], 0),
    ("science", "amateur", "How many bones are there in an adult human body?", ["206", "201", "212", "198"], 0),
    ("science", "enthusiast", "Which organ pumps blood through the body?", ["Heart", "Liver", "Lung", "Kidney"], 0),

    ("current_affairs", "amateur", "Which institution is known for setting repo rates in India?", ["Reserve Bank of India", "SEBI", "NITI Aayog", "Election Commission"], 0),
    ("current_affairs", "amateur", "Which conference is associated with global climate negotiations?", ["COP", "G20 Trade Round", "BRICS Games", "WTO Sprint"], 0),
    ("current_affairs", "enthusiast", "Which grouping includes Brazil, Russia, India, China and South Africa?", ["BRICS", "ASEAN", "QUAD", "OPEC"], 0),
    ("current_affairs", "enthusiast", "Which forum brings together major economies including India, the US and Japan?", ["G20", "NATO", "SAARC", "Commonwealth Games"], 0),
    ("current_affairs", "professional", "What does ESG commonly stand for in business reporting?", ["Environmental, Social and Governance", "Economic, Strategic and Growth", "Equity, Savings and Grants", "External, Social and Government"], 0),
    ("current_affairs", "professional", "Which body usually conducts general elections in India?", ["Election Commission of India", "Supreme Court", "Parliament Secretariat", "Finance Commission"], 0),
    ("current_affairs", "expert", "Which summit is associated with heads of the largest advanced and emerging economies?", ["G20 Summit", "BIMSTEC Summit", "NABARD Summit", "ASEAN Regional Cup"], 0),
    ("current_affairs", "expert", "Digital public infrastructure in India is often discussed alongside which stack?", ["India Stack", "Kerala Stack", "Bharat Grid", "Jan Suraksha Stack"], 0),
    ("current_affairs", "amateur", "Which platform is widely used in India for instant retail payments?", ["UPI", "SWIFT", "RTGSX", "NFCX"], 0),

    ("cricket", "amateur", "How many runs is a boundary worth when the ball crosses the rope on the ground?", ["4", "5", "6", "3"], 0),
    ("cricket", "amateur", "How many players are there in a cricket team on the fielding side?", ["11", "10", "9", "12"], 0),
    ("cricket", "enthusiast", "What is the maximum number of overs for a bowler in a T20 innings?", ["4", "5", "6", "10"], 0),
    ("cricket", "enthusiast", "What does LBW stand for?", ["Leg Before Wicket", "Long Ball Wide", "Leg Bye Wicket", "Late Bat Warning"], 0),
    ("cricket", "professional", "How many deliveries are there in one over in standard international cricket?", ["6", "8", "5", "7"], 0),
    ("cricket", "professional", "Which format is usually limited to 50 overs per side?", ["ODI", "Test", "The Hundred", "First-class"], 0),
    ("cricket", "expert", "What is the term for three wickets in three consecutive balls?", ["Hat-trick", "Maiden", "Double strike", "Spell"], 0),
    ("cricket", "expert", "What is the highest score possible from one legal ball with no overthrows?", ["6", "7", "8", "5"], 0),
    ("cricket", "amateur", "Which protective item is worn by a wicketkeeper on both hands?", ["Gloves", "Pads", "Helmet", "Arm guard"], 0),

    ("international_football", "amateur", "How many players does one football team field during normal play?", ["11", "10", "9", "12"], 0),
    ("international_football", "amateur", "Which country won the FIFA World Cup in 2022?", ["Argentina", "France", "Brazil", "Germany"], 0),
    ("international_football", "enthusiast", "Which tournament is contested by European national teams?", ["UEFA European Championship", "Copa America", "AFC Asian Cup", "CONCACAF Gold Cup"], 0),
    ("international_football", "enthusiast", "Which club is most strongly associated with Camp Nou?", ["Barcelona", "Real Madrid", "AC Milan", "Arsenal"], 0),
    ("international_football", "professional", "How many minutes are played in normal football time before stoppage?", ["90", "80", "100", "70"], 0),
    ("international_football", "professional", "What color card means immediate sending off?", ["Red", "Yellow", "Blue", "Green"], 0),
    ("international_football", "expert", "Which nation is associated with the nickname La Albiceleste?", ["Argentina", "Italy", "Spain", "Portugal"], 0),
    ("international_football", "expert", "Which competition is the top club tournament in Europe?", ["UEFA Champions League", "Europa Conference Shield", "Club Nations Cup", "FIFA Super Series"], 0),
    ("international_football", "amateur", "What body part may a goalkeeper use to handle the ball inside the penalty area?", ["Hands", "Shoulders only", "Head only", "None"], 0),

    ("bollywood", "amateur", "Which film features the characters Jai and Veeru?", ["Sholay", "Deewar", "Lagaan", "Swades"], 0),
    ("bollywood", "amateur", "Who directed Lagaan?", ["Ashutosh Gowariker", "Rajkumar Hirani", "Aditya Chopra", "Farah Khan"], 0),
    ("bollywood", "enthusiast", "Which actor played the title role in Swades?", ["Shah Rukh Khan", "Aamir Khan", "Hrithik Roshan", "Ajay Devgn"], 0),
    ("bollywood", "enthusiast", "Which film won the Academy Award for Best Original Song for 'Naatu Naatu'?", ["RRR", "Pushpa", "KGF", "Baahubali"], 0),
    ("bollywood", "professional", "Who directed 3 Idiots?", ["Rajkumar Hirani", "Zoya Akhtar", "Sanjay Leela Bhansali", "Anurag Kashyap"], 0),
    ("bollywood", "professional", "Which classic film starred Amitabh Bachchan as Vijay in the dockyard setting?", ["Deewar", "Don", "Agneepath", "Namak Halaal"], 0),
    ("bollywood", "expert", "Which film is based on cricket and the British Raj?", ["Lagaan", "Mangal Pandey", "Border", "Rang De Basanti"], 0),
    ("bollywood", "expert", "Who played Geet in Jab We Met?", ["Kareena Kapoor", "Priyanka Chopra", "Rani Mukerji", "Deepika Padukone"], 0),
    ("bollywood", "amateur", "Which movie features Rancho, Farhan and Raju?", ["3 Idiots", "Chhichhore", "Dil Chahta Hai", "Zindagi Na Milegi Dobara"], 0),

    ("international_movies", "amateur", "Who directed Titanic?", ["James Cameron", "Steven Spielberg", "Christopher Nolan", "Ridley Scott"], 0),
    ("international_movies", "amateur", "Which film features the character Jack Dawson?", ["Titanic", "Inception", "Gladiator", "Avatar"], 0),
    ("international_movies", "enthusiast", "Which movie trilogy features Frodo Baggins?", ["The Lord of the Rings", "The Hobbit Chronicles", "Narnia", "Harry Potter"], 0),
    ("international_movies", "enthusiast", "Who played the Joker in The Dark Knight?", ["Heath Ledger", "Joaquin Phoenix", "Christian Bale", "Tom Hardy"], 0),
    ("international_movies", "professional", "Which film won Best Picture at the Oscars for 2020 ceremony?", ["Parasite", "1917", "Joker", "Ford v Ferrari"], 0),
    ("international_movies", "professional", "Which film is set on the planet Pandora?", ["Avatar", "Interstellar", "Dune", "Gravity"], 0),
    ("international_movies", "expert", "Who directed Inception?", ["Christopher Nolan", "Denis Villeneuve", "David Fincher", "Martin Scorsese"], 0),
    ("international_movies", "expert", "Which movie follows a Roman general named Maximus?", ["Gladiator", "Troy", "Ben-Hur", "Braveheart"], 0),
    ("international_movies", "amateur", "Which animated film features Simba?", ["The Lion King", "Frozen", "Moana", "Coco"], 0),

    ("art_literature", "amateur", "Who wrote Hamlet?", ["William Shakespeare", "Charles Dickens", "Jane Austen", "Leo Tolstoy"], 0),
    ("art_literature", "amateur", "Who wrote Pride and Prejudice?", ["Jane Austen", "Emily Bronte", "Virginia Woolf", "George Eliot"], 0),
    ("art_literature", "enthusiast", "Which painter created the Mona Lisa?", ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"], 0),
    ("art_literature", "enthusiast", "Who wrote The Old Man and the Sea?", ["Ernest Hemingway", "John Steinbeck", "Mark Twain", "George Orwell"], 0),
    ("art_literature", "professional", "Which Indian poet wrote Gitanjali?", ["Rabindranath Tagore", "Harivansh Rai Bachchan", "Sarojini Naidu", "Subramania Bharati"], 0),
    ("art_literature", "professional", "Who painted Starry Night?", ["Vincent van Gogh", "Salvador Dali", "Henri Matisse", "Paul Cezanne"], 0),
    ("art_literature", "expert", "Which novel begins with the line 'Call me Ishmael'?", ["Moby-Dick", "The Great Gatsby", "Ulysses", "Frankenstein"], 0),
    ("art_literature", "expert", "Who wrote One Hundred Years of Solitude?", ["Gabriel Garcia Marquez", "Mario Vargas Llosa", "Jorge Luis Borges", "Isabel Allende"], 0),
    ("art_literature", "amateur", "Who wrote Harry Potter?", ["J. K. Rowling", "Suzanne Collins", "Philip Pullman", "C. S. Lewis"], 0),

    ("politics", "amateur", "How many houses does the Parliament of India have?", ["Two", "One", "Three", "Four"], 0),
    ("politics", "amateur", "What is the lower house of India's Parliament called?", ["Lok Sabha", "Rajya Sabha", "Vidhan Sabha", "Constituent Assembly"], 0),
    ("politics", "enthusiast", "What is the upper house of India's Parliament called?", ["Rajya Sabha", "Lok Sabha", "Senate", "Cabinet"], 0),
    ("politics", "enthusiast", "Who is the constitutional head of the Indian state?", ["President", "Prime Minister", "Chief Justice", "Governor General"], 0),
    ("politics", "professional", "Which article of the Indian Constitution deals with the Finance Commission?", ["Article 280", "Article 356", "Article 21", "Article 370"], 0),
    ("politics", "professional", "Which body interprets the Constitution finally in India?", ["Supreme Court", "Lok Sabha Secretariat", "Election Commission", "NITI Aayog"], 0),
    ("politics", "expert", "In a parliamentary system, the council of ministers is collectively responsible to which house?", ["Lok Sabha", "Rajya Sabha", "Supreme Court", "President"], 0),
    ("politics", "expert", "What is the tenure of a Rajya Sabha member?", ["Six years", "Five years", "Four years", "Three years"], 0),
    ("politics", "amateur", "Which office is associated with state-level constitutional leadership in India?", ["Governor", "Mayor", "Speaker", "Collector"], 0),

    ("history", "amateur", "Who was the first President of India?", ["Dr Rajendra Prasad", "Jawaharlal Nehru", "Sardar Patel", "Dr Radhakrishnan"], 0),
    ("history", "amateur", "In which year did India become independent?", ["1947", "1950", "1942", "1935"], 0),
    ("history", "enthusiast", "Which empire built the Taj Mahal?", ["Mughal Empire", "Maurya Empire", "Gupta Empire", "Maratha Empire"], 0),
    ("history", "enthusiast", "Who led the Salt March in 1930?", ["Mahatma Gandhi", "Subhas Chandra Bose", "Bal Gangadhar Tilak", "Bhagat Singh"], 0),
    ("history", "professional", "Which battle in 1757 strengthened British control in Bengal?", ["Battle of Plassey", "Battle of Panipat", "Battle of Buxar", "Battle of Talikota"], 0),
    ("history", "professional", "Which ancient civilization is associated with Mohenjo-daro?", ["Indus Valley Civilization", "Mesopotamia", "Mayan Civilization", "Roman Empire"], 0),
    ("history", "expert", "Who wrote The Discovery of India?", ["Jawaharlal Nehru", "B. R. Ambedkar", "S. Radhakrishnan", "M. N. Roy"], 0),
    ("history", "expert", "Which dynasty is associated with Ashoka?", ["Maurya", "Gupta", "Chola", "Kushan"], 0),
    ("history", "amateur", "The French Revolution began in which year?", ["1789", "1776", "1815", "1804"], 0),

    ("finance", "amateur", "What does IPO stand for?", ["Initial Public Offering", "Internal Price Order", "International Purchase Option", "Indexed Profit Output"], 0),
    ("finance", "amateur", "What is a share?", ["A unit of ownership in a company", "A type of bank loan", "A tax receipt", "A bond coupon"], 0),
    ("finance", "enthusiast", "What does mutual fund diversification mainly reduce?", ["Concentration risk", "All market risk", "Tax liability to zero", "Inflation permanently"], 0),
    ("finance", "enthusiast", "What is the common name for a company's profit after tax?", ["Net profit", "Gross turnover", "Operating cash", "Total assets"], 0),
    ("finance", "professional", "Which ratio compares current assets with current liabilities?", ["Current ratio", "Debt-equity ratio", "ROE", "Interest coverage"], 0),
    ("finance", "professional", "Which market is used for long-term capital raising?", ["Capital market", "Money market", "Spot FX market", "Commodity warehouse"], 0),
    ("finance", "expert", "What does P/E ratio compare?", ["Share price to earnings per share", "Profit to expenses", "Price to enterprise value", "Promoter equity to revenue"], 0),
    ("finance", "expert", "Which statement shows assets, liabilities and equity?", ["Balance sheet", "Income statement", "Cash book", "Audit letter"], 0),
    ("finance", "amateur", "Which term describes money borrowed by a company?", ["Debt", "Equity", "Dividend", "Revenue"], 0),

    ("economics", "amateur", "What happens to prices generally during inflation?", ["They rise", "They fall", "They freeze", "They disappear"], 0),
    ("economics", "amateur", "GDP is commonly used to measure what?", ["Total economic output", "Only government spending", "Only exports", "Only tax collections"], 0),
    ("economics", "enthusiast", "When demand rises and supply stays unchanged, price usually does what?", ["Rises", "Falls", "Becomes zero", "Stops changing forever"], 0),
    ("economics", "enthusiast", "What is unemployment?", ["People willing to work but without jobs", "People changing cities", "Students in class", "People working overtime"], 0),
    ("economics", "professional", "What is fiscal deficit broadly the gap between?", ["Government spending and government receipts", "Exports and imports", "Savings and consumption", "Assets and liabilities"], 0),
    ("economics", "professional", "Which policy tool is normally used by a central bank?", ["Interest rates", "Import quotas", "Cabinet expansion", "Labor contracts"], 0),
    ("economics", "expert", "Opportunity cost means what is sacrificed when choosing one option over another?", ["The next best alternative", "Only cash paid", "Only time spent", "Only tax paid"], 0),
    ("economics", "expert", "If supply increases while demand stays the same, price usually does what?", ["Falls", "Rises", "Doubles", "Stops existing"], 0),
    ("economics", "amateur", "Which word describes a prolonged fall in overall prices?", ["Deflation", "Inflation", "Stagflation", "Expansion"], 0),
]


def build_question_bank():
    questions = []
    by_difficulty = defaultdict(list)
    for base_index, (category, difficulty, prompt, options, answer_index) in enumerate(BASE_QUESTIONS, start=1):
        option_payload = [
            {"key": chr(65 + option_index), "label": option}
            for option_index, option in enumerate(options)
        ]
        correct_option = chr(65 + answer_index)
        for variant_index, prefix in enumerate(PROMPT_PREFIXES, start=1):
            key = f"{category}-{base_index:03d}-{variant_index}"
            full_prompt = f"{prefix}{prompt}".strip()
            question = {
                "key": key,
                "category": category,
                "difficulty": difficulty,
                "prompt": full_prompt,
                "options": option_payload,
                "correct_option": correct_option,
            }
            questions.append(question)
            by_difficulty[difficulty].append(question)
    return questions, by_difficulty


QUESTION_BANK, QUESTION_BANK_BY_DIFFICULTY = build_question_bank()
QUESTION_LOOKUP = {question["key"]: question for question in QUESTION_BANK}


def get_question_by_key(key):
    return QUESTION_LOOKUP[key]


def get_questions_for_difficulty(difficulty):
    return list(QUESTION_BANK_BY_DIFFICULTY.get(difficulty, []))
