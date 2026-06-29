# common_passwords.py
"""
Common passwords list for password strength checking.
Includes years, months, days, seasons, and common words.
"""

# ============================================
# 1. YEARS (1925 to 2075)
# ============================================
YEARS = [str(year) for year in range(1925, 2076)]

# ============================================
# 2. MONTHS
# ============================================
MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

# ============================================
# 3. DAYS
# ============================================
DAYS = [
    "monday", "tuesday", "wednesday", "thursday", "friday",
    "saturday", "sunday", "mon", "tue", "wed", "thu", "fri", "sat", "sun"
]

# ============================================
# 4. SEASONS
# ============================================
SEASONS = ["spring", "summer", "autumn", "fall", "winter"]

# ============================================
# 5. COMMON PASSWORDS (Base set - بدون تکرار)
# ============================================
common_passwords = {
    # Most common
    "password",
    "qwerty", "qwerty123", "qwertyuiop",
    "admin", "admin123", "administrator",
    "welcome", "welcome1", "welcome123",
    "letmein", "letmein123",
    "iloveyou", "iloveyou1",

    # Names
    "john", "jane", "bob", "alice",
    "david", "emma", "olivia", "ava", "isabella",
    "james", "robert", "william", "joseph",
    "christopher", "paul", "mark", "donald",
    "george", "kenneth", "steven", "edward", "brian",
    "ronald", "anthony", "kevin", "jason", "matthew",
    "gary", "timothy", "jose", "larry", "jeffrey",
    "frank", "scott", "eric", "stephen", "andrew",

    # Animals
    "tiger", "lion", "eagle", "falcon", "hawk",
    "wolf", "panda", "koala", "penguin", "dolphin",
    "whale", "shark", "bear", "panther", "leopard",
    "cheetah", "cougar", "jaguar", "lynx",
    "rabbit", "bunny", "kitten", "puppy", "hamster",
    "parrot", "peacock", "swan", "raven", "cobra",
    "viper", "python", "anaconda", "boa",
    "alligator", "crocodile", "lizard", "gecko", "iguana",
    "gorilla", "chimpanzee", "orangutan", "baboon", "mandrill",
    "elephant", "giraffe", "zebra", "hippo", "rhino",
    "kangaroo", "platypus", "echidna", "wombat",

    # Nature
    "sunshine", "rainbow", "thunder", "lightning", "storm",
    "mountain", "ocean", "river", "forest", "desert",
    "flower", "garden", "sunset", "moonlight", "starlight",
    "aurora", "breeze", "cascade", "daisy", "emerald",
    "firefly", "galaxy", "horizon", "island", "jasmine",
    "kingfisher", "lavender", "meadow", "nightingale", "orchid",
    "sapphire", "tulip", "violet", "willow", "zenith",
    "waterfall", "volcano", "canyon", "glacier", "tundra",
    "savanna", "jungle", "swamp", "reef", "coast",

    # Colors
    "red", "blue", "green", "yellow", "purple",
    "orange", "pink", "black", "white", "silver",
    "golden", "gold", "bronze", "copper", "navy",
    "teal", "cyan", "magenta", "lime", "olive",
    "maroon", "coral", "crimson", "indigo",
    "mauve", "tan", "beige", "ivory",
    "turquoise", "aquamarine", "cerulean", "charcoal",

    # Countries
    "america", "canada", "england", "france", "germany",
    "italy", "spain", "australia", "brazil", "india",
    "china", "japan", "korea", "mexico", "russia",
    "egypt", "greece", "turkey", "sweden", "norway",
    "finland", "denmark", "netherlands", "belgium", "switzerland",
    "portugal", "poland", "ukraine", "romania", "argentina",
    "chile", "peru", "venezuela", "colombia",

    # Cities
    "london", "paris", "newyork", "tokyo", "rome",
    "berlin", "madrid", "amsterdam", "venice", "prague",
    "dubai", "singapore", "hongkong", "sydney", "toronto",
    "chicago", "losangeles", "miami", "boston", "seattle",
    "sanfrancisco", "washington", "barcelona", "milan", "moscow",
    "istanbul", "shanghai", "mumbai", "rio",

    # Sports
    "soccer", "football", "baseball", "basketball", "hockey",
    "tennis", "golf", "swimming", "running", "cycling",
    "volleyball", "rugby", "cricket", "badminton", "karate",
    "judo", "taekwondo", "boxing", "wrestling", "skiing",
    "snowboarding", "surfing", "skateboarding",

    # Food
    "pizza", "burger", "pasta", "sushi", "taco",
    "sandwich", "chocolate", "cookie", "icecream", "coffee",
    "tea", "juice", "milkshake", "smoothie", "pancake",
    "waffle", "muffin", "brownie", "cheesecake", "donut",
    "bagel", "croissant", "biscuit", "cereal", "oatmeal",
    "spaghetti", "lasagna", "ramen", "noodle", "curry",
    "steak", "chicken", "salmon", "tuna", "lobster",

    # Technology
    "computer", "internet", "google", "apple", "microsoft",
    "windows", "linux", "android", "iphone", "samsung",
    "macbook", "laptop", "keyboard", "monitor", "printer",
    "software", "hardware", "coding", "programming",
    "java", "javascript", "ruby", "php", "swift",
    "html", "css", "react", "angular", "vue",
    "database", "server", "network", "cloud", "security",

    # Mythical & Fantasy
    "matrix", "zeus", "thor", "odin", "athena",
    "hercules", "batman", "superman", "spiderman", "ironman",
    "wonderwoman", "flash", "aquaman", "hulk", "blackwidow",
    "dumbledore", "voldemort", "snape", "harrypotter", "hermione",
    "gandalf", "aragorn", "legolas", "gimli", "frodo",
    "bilbo", "gollum", "sauron", "saruman", "elrond",

    # Fictional characters
    "sherlock", "watson", "holmes", "moriarty",
    "spock", "kirk", "picard", "riker",
    "skywalker", "vader", "yoda", "leia", "han",

    # Brands
    "nike", "adidas", "puma", "reebok", "underarmour",
    "sony", "disney", "marvel", "dc", "universal", "netflix",
    "spotify", "youtube", "instagram", "facebook", "twitter",
}

# ============================================
# 6. ADD YEARS, MONTHS, DAYS, SEASONS
# ============================================
common_passwords.update(YEARS)       # 1925 to 2075
common_passwords.update(MONTHS)      # january, february, ...
common_passwords.update(DAYS)        # monday, tuesday, ...
common_passwords.update(SEASONS)     # spring, summer, ...

# ============================================
# 7. Convert to set and export
# ============================================
COMMON_PASSWORDS = set(common_passwords)