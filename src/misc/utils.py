import random


def get_random_name():
    names = [
        "Emma", "Olivia", "Sophia", "Ava", "Isabella", "Mia", "Charlotte",
        "Amelia", "Harper", "Evelyn", "Abigail", "Emily", "Ella", "Elizabeth",
        "Camila", "Luna", "Sofia", "Avery", "Mila", "Aria", "Scarlett",
        "Penelope", "Layla", "Chloe", "Victoria", "Madison", "Eleanor",
        "Grace", "Nora", "Riley", "Zoey", "Hannah"
    ]
    return random.choice(names)


def get_random_share():
    companies = [
        "Apple Inc.", "Microsoft Corporation", "Amazon.com, Inc.", "Facebook, Inc.",
        "Alphabet Inc.", "Tesla, Inc.", "Johnson & Johnson", "JPMorgan Chase & Co.",
        "Visa Inc.", "Procter & Gamble Co", "Mastercard Incorporated", "Berkshire Hathaway Inc.",
        "The Home Depot, Inc.", "UnitedHealth Group Inc.", "Walmart Inc.", "The Coca-Cola Company",
        "Verizon Communications Inc.", "AT&T Inc.", "Pfizer Inc.", "ExxonMobil Corporation",
        "Cisco Systems, Inc.", "Intel Corporation", "Walt Disney Co", "McDonalds Corporation",
        "NVIDIA Corporation", "Merck & Co., Inc.", "Boeing Co", "3M Company", "The Goldman Sachs Group, Inc.",
        "The Boeing Company", "The Walt Disney Company", "Chevron Corporation", "Caterpillar Inc."
    ]
    return random.choice(companies)
