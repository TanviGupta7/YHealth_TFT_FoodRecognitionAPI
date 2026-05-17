"""Nutrition per serving for Food-101 labels and common aliases."""

DEFAULT_NUTRITION = {
    "calories": 220,
    "protein_g": 10,
    "carbs_g": 28,
    "fat_g": 9,
    "quantity": "1 serving",
}

# Keys are normalized: lowercase, underscores as spaces
NUTRITION_DB = {
    # Food-101 (model labels)
    "apple pie": {"calories": 410, "protein_g": 4, "carbs_g": 58, "fat_g": 19, "quantity": "1 slice"},
    "baby back ribs": {"calories": 540, "protein_g": 38, "carbs_g": 18, "fat_g": 36, "quantity": "1 rack"},
    "baklava": {"calories": 330, "protein_g": 5, "carbs_g": 42, "fat_g": 18, "quantity": "3 pieces"},
    "beef carpaccio": {"calories": 220, "protein_g": 22, "carbs_g": 2, "fat_g": 14, "quantity": "1 serving"},
    "beef tartare": {"calories": 250, "protein_g": 26, "carbs_g": 4, "fat_g": 15, "quantity": "1 serving"},
    "beet salad": {"calories": 140, "protein_g": 4, "carbs_g": 18, "fat_g": 7, "quantity": "1 bowl"},
    "beignets": {"calories": 320, "protein_g": 5, "carbs_g": 42, "fat_g": 15, "quantity": "3 pieces"},
    "bibimbap": {"calories": 490, "protein_g": 18, "carbs_g": 72, "fat_g": 14, "quantity": "1 bowl"},
    "bread pudding": {"calories": 360, "protein_g": 8, "carbs_g": 52, "fat_g": 14, "quantity": "1 portion"},
    "breakfast burrito": {"calories": 480, "protein_g": 22, "carbs_g": 48, "fat_g": 22, "quantity": "1 wrap"},
    "bruschetta": {"calories": 180, "protein_g": 5, "carbs_g": 22, "fat_g": 8, "quantity": "4 pieces"},
    "caesar salad": {"calories": 190, "protein_g": 8, "carbs_g": 12, "fat_g": 14, "quantity": "1 bowl"},
    "cannoli": {"calories": 240, "protein_g": 5, "carbs_g": 28, "fat_g": 12, "quantity": "2 pieces"},
    "caprese salad": {"calories": 220, "protein_g": 12, "carbs_g": 8, "fat_g": 16, "quantity": "1 plate"},
    "carne asada fries": {"calories": 620, "protein_g": 28, "carbs_g": 58, "fat_g": 32, "quantity": "1 plate"},
    "carrot cake": {"calories": 430, "protein_g": 5, "carbs_g": 58, "fat_g": 20, "quantity": "1 slice"},
    "ceviche": {"calories": 180, "protein_g": 24, "carbs_g": 12, "fat_g": 4, "quantity": "1 cup"},
    "cheese plate": {"calories": 380, "protein_g": 18, "carbs_g": 8, "fat_g": 30, "quantity": "1 serving"},
    "cheesecake": {"calories": 400, "protein_g": 7, "carbs_g": 36, "fat_g": 26, "quantity": "1 slice"},
    "chicken curry": {"calories": 280, "protein_g": 24, "carbs_g": 10, "fat_g": 16, "quantity": "1 bowl"},
    "chicken quesadilla": {"calories": 510, "protein_g": 28, "carbs_g": 42, "fat_g": 24, "quantity": "1 piece"},
    "chicken wings": {"calories": 430, "protein_g": 32, "carbs_g": 8, "fat_g": 28, "quantity": "6 wings"},
    "chocolate cake": {"calories": 380, "protein_g": 5, "carbs_g": 52, "fat_g": 18, "quantity": "1 slice"},
    "chocolate mousse": {"calories": 280, "protein_g": 5, "carbs_g": 28, "fat_g": 18, "quantity": "1 cup"},
    "churros": {"calories": 340, "protein_g": 4, "carbs_g": 48, "fat_g": 16, "quantity": "4 pieces"},
    "clam chowder": {"calories": 220, "protein_g": 12, "carbs_g": 20, "fat_g": 10, "quantity": "1 bowl"},
    "club sandwich": {"calories": 520, "protein_g": 28, "carbs_g": 42, "fat_g": 26, "quantity": "1 sandwich"},
    "crab cakes": {"calories": 320, "protein_g": 22, "carbs_g": 18, "fat_g": 18, "quantity": "2 cakes"},
    "creme brulee": {"calories": 340, "protein_g": 5, "carbs_g": 32, "fat_g": 22, "quantity": "1 ramekin"},
    "croque madame": {"calories": 560, "protein_g": 26, "carbs_g": 38, "fat_g": 34, "quantity": "1 sandwich"},
    "cup cakes": {"calories": 280, "protein_g": 3, "carbs_g": 40, "fat_g": 12, "quantity": "1 cupcake"},
    "deviled eggs": {"calories": 140, "protein_g": 10, "carbs_g": 2, "fat_g": 10, "quantity": "2 halves"},
    "donuts": {"calories": 290, "protein_g": 4, "carbs_g": 36, "fat_g": 15, "quantity": "1 piece"},
    "dumplings": {"calories": 280, "protein_g": 12, "carbs_g": 32, "fat_g": 10, "quantity": "6 pieces"},
    "edamame": {"calories": 190, "protein_g": 17, "carbs_g": 14, "fat_g": 8, "quantity": "1 cup"},
    "eggs benedict": {"calories": 480, "protein_g": 20, "carbs_g": 28, "fat_g": 32, "quantity": "1 plate"},
    "escargots": {"calories": 220, "protein_g": 14, "carbs_g": 6, "fat_g": 16, "quantity": "6 snails"},
    "falafel": {"calories": 330, "protein_g": 14, "carbs_g": 36, "fat_g": 16, "quantity": "1 serving"},
    "filet mignon": {"calories": 450, "protein_g": 42, "carbs_g": 0, "fat_g": 30, "quantity": "200g"},
    "fish and chips": {"calories": 680, "protein_g": 32, "carbs_g": 62, "fat_g": 34, "quantity": "1 plate"},
    "foie gras": {"calories": 380, "protein_g": 10, "carbs_g": 4, "fat_g": 36, "quantity": "1 serving"},
    "french fries": {"calories": 380, "protein_g": 4, "carbs_g": 48, "fat_g": 20, "quantity": "medium portion"},
    "french onion soup": {"calories": 210, "protein_g": 10, "carbs_g": 22, "fat_g": 10, "quantity": "1 bowl"},
    "french toast": {"calories": 380, "protein_g": 12, "carbs_g": 48, "fat_g": 14, "quantity": "2 slices"},
    "fried calamari": {"calories": 360, "protein_g": 18, "carbs_g": 28, "fat_g": 20, "quantity": "1 serving"},
    "fried rice": {"calories": 290, "protein_g": 7, "carbs_g": 52, "fat_g": 7, "quantity": "1 bowl"},
    "frozen yogurt": {"calories": 180, "protein_g": 5, "carbs_g": 32, "fat_g": 3, "quantity": "1 cup"},
    "garlic bread": {"calories": 220, "protein_g": 6, "carbs_g": 28, "fat_g": 10, "quantity": "2 slices"},
    "gnocchi": {"calories": 340, "protein_g": 10, "carbs_g": 58, "fat_g": 8, "quantity": "1 bowl"},
    "greek salad": {"calories": 180, "protein_g": 6, "carbs_g": 12, "fat_g": 14, "quantity": "1 bowl"},
    "grilled cheese sandwich": {"calories": 400, "protein_g": 16, "carbs_g": 36, "fat_g": 22, "quantity": "1 sandwich"},
    "grilled salmon": {"calories": 280, "protein_g": 34, "carbs_g": 0, "fat_g": 16, "quantity": "150g"},
    "guacamole": {"calories": 240, "protein_g": 3, "carbs_g": 14, "fat_g": 22, "quantity": "1 cup"},
    "gyoza": {"calories": 260, "protein_g": 10, "carbs_g": 30, "fat_g": 10, "quantity": "6 pieces"},
    "hamburger": {"calories": 540, "protein_g": 28, "carbs_g": 45, "fat_g": 26, "quantity": "1 piece"},
    "hot and sour soup": {"calories": 120, "protein_g": 8, "carbs_g": 12, "fat_g": 5, "quantity": "1 bowl"},
    "hot dog": {"calories": 290, "protein_g": 11, "carbs_g": 24, "fat_g": 18, "quantity": "1 piece"},
    "huevos rancheros": {"calories": 420, "protein_g": 18, "carbs_g": 36, "fat_g": 22, "quantity": "1 plate"},
    "hummus": {"calories": 165, "protein_g": 8, "carbs_g": 18, "fat_g": 8, "quantity": "100g"},
    "ice cream": {"calories": 270, "protein_g": 4, "carbs_g": 34, "fat_g": 14, "quantity": "1 scoop"},
    "lasagna": {"calories": 450, "protein_g": 22, "carbs_g": 42, "fat_g": 22, "quantity": "1 slice"},
    "lobster bisque": {"calories": 280, "protein_g": 14, "carbs_g": 18, "fat_g": 18, "quantity": "1 bowl"},
    "lobster roll sandwich": {"calories": 480, "protein_g": 28, "carbs_g": 42, "fat_g": 22, "quantity": "1 roll"},
    "macaroni and cheese": {"calories": 410, "protein_g": 16, "carbs_g": 48, "fat_g": 18, "quantity": "1 bowl"},
    "macarons": {"calories": 160, "protein_g": 3, "carbs_g": 24, "fat_g": 7, "quantity": "3 pieces"},
    "miso soup": {"calories": 70, "protein_g": 6, "carbs_g": 8, "fat_g": 2, "quantity": "1 bowl"},
    "mussels": {"calories": 220, "protein_g": 24, "carbs_g": 10, "fat_g": 8, "quantity": "1 serving"},
    "nachos": {"calories": 520, "protein_g": 16, "carbs_g": 48, "fat_g": 28, "quantity": "1 plate"},
    "omelette": {"calories": 185, "protein_g": 14, "carbs_g": 2, "fat_g": 14, "quantity": "1 piece"},
    "onion rings": {"calories": 410, "protein_g": 5, "carbs_g": 48, "fat_g": 22, "quantity": "1 serving"},
    "oysters": {"calories": 120, "protein_g": 14, "carbs_g": 8, "fat_g": 4, "quantity": "6 pieces"},
    "pad thai": {"calories": 430, "protein_g": 16, "carbs_g": 58, "fat_g": 14, "quantity": "1 plate"},
    "paella": {"calories": 480, "protein_g": 24, "carbs_g": 58, "fat_g": 16, "quantity": "1 plate"},
    "pancakes": {"calories": 360, "protein_g": 10, "carbs_g": 56, "fat_g": 11, "quantity": "3 pieces"},
    "panna cotta": {"calories": 280, "protein_g": 4, "carbs_g": 28, "fat_g": 16, "quantity": "1 cup"},
    "peking duck": {"calories": 420, "protein_g": 28, "carbs_g": 12, "fat_g": 28, "quantity": "1 serving"},
    "pho": {"calories": 380, "protein_g": 22, "carbs_g": 52, "fat_g": 8, "quantity": "1 bowl"},
    "pizza": {"calories": 285, "protein_g": 12, "carbs_g": 36, "fat_g": 10, "quantity": "1 slice"},
    "pork chop": {"calories": 380, "protein_g": 36, "carbs_g": 0, "fat_g": 24, "quantity": "1 chop"},
    "poutine": {"calories": 740, "protein_g": 18, "carbs_g": 68, "fat_g": 42, "quantity": "1 plate"},
    "prime rib": {"calories": 480, "protein_g": 40, "carbs_g": 0, "fat_g": 36, "quantity": "200g"},
    "pulled pork sandwich": {"calories": 520, "protein_g": 30, "carbs_g": 48, "fat_g": 22, "quantity": "1 sandwich"},
    "ramen": {"calories": 440, "protein_g": 18, "carbs_g": 58, "fat_g": 14, "quantity": "1 bowl"},
    "ravioli": {"calories": 380, "protein_g": 16, "carbs_g": 48, "fat_g": 12, "quantity": "1 bowl"},
    "red velvet cake": {"calories": 390, "protein_g": 5, "carbs_g": 54, "fat_g": 18, "quantity": "1 slice"},
    "risotto": {"calories": 360, "protein_g": 10, "carbs_g": 52, "fat_g": 12, "quantity": "1 bowl"},
    "samosa": {"calories": 260, "protein_g": 5, "carbs_g": 32, "fat_g": 13, "quantity": "2 pieces"},
    "sashimi": {"calories": 180, "protein_g": 28, "carbs_g": 0, "fat_g": 6, "quantity": "8 pieces"},
    "scallops": {"calories": 200, "protein_g": 24, "carbs_g": 8, "fat_g": 8, "quantity": "1 serving"},
    "seafood pasta": {"calories": 420, "protein_g": 22, "carbs_g": 52, "fat_g": 14, "quantity": "1 bowl"},
    "seaweed salad": {"calories": 90, "protein_g": 2, "carbs_g": 12, "fat_g": 4, "quantity": "1 bowl"},
    "shrimp and grits": {"calories": 380, "protein_g": 22, "carbs_g": 42, "fat_g": 14, "quantity": "1 bowl"},
    "spaghetti bolognese": {"calories": 480, "protein_g": 22, "carbs_g": 58, "fat_g": 16, "quantity": "1 bowl"},
    "spaghetti carbonara": {"calories": 520, "protein_g": 20, "carbs_g": 56, "fat_g": 24, "quantity": "1 bowl"},
    "spring rolls": {"calories": 200, "protein_g": 6, "carbs_g": 28, "fat_g": 8, "quantity": "4 pieces"},
    "steak": {"calories": 420, "protein_g": 46, "carbs_g": 0, "fat_g": 26, "quantity": "200g"},
    "strawberry shortcake": {"calories": 350, "protein_g": 4, "carbs_g": 48, "fat_g": 16, "quantity": "1 slice"},
    "sushi": {"calories": 250, "protein_g": 12, "carbs_g": 38, "fat_g": 5, "quantity": "6 pieces"},
    "tacos": {"calories": 210, "protein_g": 11, "carbs_g": 20, "fat_g": 10, "quantity": "1 piece"},
    "takoyaki": {"calories": 280, "protein_g": 12, "carbs_g": 28, "fat_g": 12, "quantity": "6 pieces"},
    "tiramisu": {"calories": 320, "protein_g": 6, "carbs_g": 36, "fat_g": 16, "quantity": "1 slice"},
    "tuna tartare": {"calories": 200, "protein_g": 28, "carbs_g": 4, "fat_g": 8, "quantity": "1 serving"},
    "waffles": {"calories": 380, "protein_g": 8, "carbs_g": 52, "fat_g": 16, "quantity": "2 waffles"},
    # Extra cuisines (fuzzy match for demos)
    "paneer butter masala": {"calories": 320, "protein_g": 14, "carbs_g": 18, "fat_g": 22, "quantity": "1 bowl"},
    "paneer": {"calories": 265, "protein_g": 18, "carbs_g": 4, "fat_g": 20, "quantity": "100g"},
    "butter chicken": {"calories": 290, "protein_g": 25, "carbs_g": 12, "fat_g": 16, "quantity": "1 bowl"},
    "biryani": {"calories": 450, "protein_g": 22, "carbs_g": 58, "fat_g": 14, "quantity": "1 plate"},
    "dal": {"calories": 180, "protein_g": 10, "carbs_g": 28, "fat_g": 4, "quantity": "1 bowl"},
    "dal makhani": {"calories": 220, "protein_g": 11, "carbs_g": 26, "fat_g": 8, "quantity": "1 bowl"},
    "naan": {"calories": 260, "protein_g": 8, "carbs_g": 45, "fat_g": 6, "quantity": "1 piece"},
    "roti": {"calories": 120, "protein_g": 4, "carbs_g": 22, "fat_g": 3, "quantity": "1 piece"},
    "idli": {"calories": 58, "protein_g": 2, "carbs_g": 12, "fat_g": 0.4, "quantity": "2 pieces"},
    "dosa": {"calories": 168, "protein_g": 4, "carbs_g": 30, "fat_g": 4, "quantity": "1 piece"},
    "chana masala": {"calories": 270, "protein_g": 14, "carbs_g": 38, "fat_g": 7, "quantity": "1 bowl"},
    "aloo gobi": {"calories": 150, "protein_g": 5, "carbs_g": 22, "fat_g": 5, "quantity": "1 bowl"},
    "palak paneer": {"calories": 240, "protein_g": 12, "carbs_g": 10, "fat_g": 18, "quantity": "1 bowl"},
    "rajma": {"calories": 210, "protein_g": 13, "carbs_g": 30, "fat_g": 4, "quantity": "1 bowl"},
    "chole bhature": {"calories": 520, "protein_g": 16, "carbs_g": 72, "fat_g": 20, "quantity": "1 plate"},
    "gulab jamun": {"calories": 175, "protein_g": 3, "carbs_g": 30, "fat_g": 6, "quantity": "2 pieces"},
    "burger": {"calories": 540, "protein_g": 28, "carbs_g": 45, "fat_g": 26, "quantity": "1 piece"},
    "pasta": {"calories": 370, "protein_g": 13, "carbs_g": 68, "fat_g": 6, "quantity": "1 bowl"},
    "salad": {"calories": 120, "protein_g": 4, "carbs_g": 14, "fat_g": 6, "quantity": "1 bowl"},
    "sandwich": {"calories": 350, "protein_g": 16, "carbs_g": 40, "fat_g": 14, "quantity": "1 piece"},
    "rice": {"calories": 210, "protein_g": 4, "carbs_g": 45, "fat_g": 0.5, "quantity": "1 cup"},
    "jeera rice": {"calories": 210, "protein_g": 4, "carbs_g": 42, "fat_g": 3, "quantity": "1 cup"},
    "noodles": {"calories": 300, "protein_g": 10, "carbs_g": 54, "fat_g": 6, "quantity": "1 bowl"},
    "chicken": {"calories": 240, "protein_g": 35, "carbs_g": 0, "fat_g": 11, "quantity": "150g"},
    "fish": {"calories": 200, "protein_g": 30, "carbs_g": 0, "fat_g": 9, "quantity": "150g"},
    "egg": {"calories": 155, "protein_g": 13, "carbs_g": 1, "fat_g": 11, "quantity": "2 eggs"},
    "bread": {"calories": 140, "protein_g": 5, "carbs_g": 26, "fat_g": 2, "quantity": "2 slices"},
    "burrito": {"calories": 490, "protein_g": 21, "carbs_g": 58, "fat_g": 18, "quantity": "1 piece"},
    "curry": {"calories": 280, "protein_g": 16, "carbs_g": 22, "fat_g": 14, "quantity": "1 bowl"},
    "kebab": {"calories": 320, "protein_g": 28, "carbs_g": 12, "fat_g": 18, "quantity": "1 serving"},
    "shawarma": {"calories": 380, "protein_g": 24, "carbs_g": 38, "fat_g": 14, "quantity": "1 wrap"},
    "cake": {"calories": 350, "protein_g": 4, "carbs_g": 52, "fat_g": 14, "quantity": "1 slice"},
    "apple": {"calories": 95, "protein_g": 0.5, "carbs_g": 25, "fat_g": 0.3, "quantity": "1 medium"},
    "banana": {"calories": 105, "protein_g": 1.3, "carbs_g": 27, "fat_g": 0.4, "quantity": "1 medium"},
    "salmon": {"calories": 280, "protein_g": 34, "carbs_g": 0, "fat_g": 16, "quantity": "150g"},
    "tuna": {"calories": 180, "protein_g": 35, "carbs_g": 0, "fat_g": 4, "quantity": "150g"},
    "oatmeal": {"calories": 166, "protein_g": 6, "carbs_g": 28, "fat_g": 4, "quantity": "1 bowl"},
    "soup": {"calories": 120, "protein_g": 6, "carbs_g": 16, "fat_g": 4, "quantity": "1 bowl"},
    "avocado": {"calories": 160, "protein_g": 2, "carbs_g": 9, "fat_g": 15, "quantity": "half"},
    "broccoli": {"calories": 55, "protein_g": 4, "carbs_g": 11, "fat_g": 0.6, "quantity": "1 cup"},
    "chocolate": {"calories": 230, "protein_g": 3, "carbs_g": 26, "fat_g": 14, "quantity": "40g"},
    "yogurt": {"calories": 100, "protein_g": 10, "carbs_g": 12, "fat_g": 2, "quantity": "1 cup"},
    "cheese": {"calories": 200, "protein_g": 12, "carbs_g": 1, "fat_g": 17, "quantity": "50g"},
    "tofu": {"calories": 120, "protein_g": 12, "carbs_g": 3, "fat_g": 7, "quantity": "150g"},
    "lentils": {"calories": 230, "protein_g": 18, "carbs_g": 40, "fat_g": 1, "quantity": "1 cup"},
    "chickpeas": {"calories": 270, "protein_g": 15, "carbs_g": 45, "fat_g": 4, "quantity": "1 cup"},
    "shrimp": {"calories": 200, "protein_g": 38, "carbs_g": 2, "fat_g": 4, "quantity": "150g"},
    # Indian (extended)
    "rajma chawal": {"calories": 380, "protein_g": 15, "carbs_g": 58, "fat_g": 8, "quantity": "1 plate"},
    "poha": {"calories": 250, "protein_g": 5, "carbs_g": 48, "fat_g": 6, "quantity": "1 bowl"},
    "upma": {"calories": 280, "protein_g": 7, "carbs_g": 42, "fat_g": 9, "quantity": "1 bowl"},
    "pav bhaji": {"calories": 420, "protein_g": 10, "carbs_g": 58, "fat_g": 16, "quantity": "1 plate"},
    "pani puri": {"calories": 180, "protein_g": 4, "carbs_g": 28, "fat_g": 6, "quantity": "6 pieces"},
    "aloo paratha": {"calories": 320, "protein_g": 8, "carbs_g": 42, "fat_g": 14, "quantity": "2 pieces"},
    "fries": {"calories": 380, "protein_g": 4, "carbs_g": 48, "fat_g": 20, "quantity": "1 serving"},
}


def normalize_label(label: str) -> str:
    return label.lower().strip().replace("_", " ")


# Food-101 label → (nutrition key, display name)
LABEL_MAPPINGS = {
    "pizza": ("pizza", "Pizza"),
    "hamburger": ("burger", "Burger"),
    "french fries": ("french fries", "Fries"),
    "fried rice": ("fried rice", "Fried Rice"),
    "ramen": ("ramen", "Ramen"),
    "sushi": ("sushi", "Sushi"),
    "dumplings": ("dumplings", "Dumplings"),
    "spaghetti bolognese": ("pasta", "Pasta"),
    "spaghetti carbonara": ("pasta", "Pasta"),
    "seafood pasta": ("pasta", "Pasta"),
    "macaroni and cheese": ("pasta", "Pasta"),
    "club sandwich": ("sandwich", "Sandwich"),
    "grilled cheese sandwich": ("sandwich", "Sandwich"),
    "caesar salad": ("salad", "Salad"),
    "greek salad": ("salad", "Salad"),
    "beet salad": ("salad", "Salad"),
    "caprese salad": ("salad", "Salad"),
    "steak": ("steak", "Steak"),
    "filet mignon": ("steak", "Steak"),
    "prime rib": ("steak", "Steak"),
    "pancakes": ("pancakes", "Pancakes"),
    "waffles": ("waffles", "Waffles"),
    "donuts": ("donuts", "Donuts"),
    "chicken curry": ("butter chicken", "Butter Chicken"),
    "curry": ("paneer butter masala", "Paneer Butter Masala"),
    "samosa": ("samosa", "Samosa"),
    "dosa": ("dosa", "Dosa"),
    "idli": ("idli", "Idli"),
    "bibimbap": ("biryani", "Biryani"),
    "risotto": ("biryani", "Biryani"),
    "paella": ("biryani", "Biryani"),
    "hot dog": ("burger", "Burger"),
    "tacos": ("tacos", "Tacos"),
    "burrito": ("burrito", "Burrito"),
    "breakfast burrito": ("burrito", "Burrito"),
    "chana masala": ("chole bhature", "Chole Bhature"),
    "dal": ("dal makhani", "Dal Makhani"),
    "lentils": ("dal makhani", "Dal Makhani"),
    "chickpeas": ("chole bhature", "Chole Bhature"),
    "roti": ("naan", "Naan"),
    "garlic bread": ("naan", "Naan"),
    "bread": ("naan", "Naan"),
    "rice": ("jeera rice", "Jeera Rice"),
    "fried calamari": ("seafood pasta", "Seafood Pasta"),
    "pad thai": ("noodles", "Noodles"),
    "pho": ("noodles", "Noodles"),
    "gyoza": ("dumplings", "Dumplings"),
    "spring rolls": ("dumplings", "Dumplings"),
    "pulled pork sandwich": ("sandwich", "Sandwich"),
    "lobster roll sandwich": ("sandwich", "Sandwich"),
    "croque madame": ("sandwich", "Sandwich"),
}


def resolve_food(label: str) -> tuple[str, str]:
    """Return nutrition lookup key and clean display name."""
    key = normalize_label(label)
    if key in LABEL_MAPPINGS:
        nutrition_key, display = LABEL_MAPPINGS[key]
        return nutrition_key, display
    display = " ".join(w.capitalize() for w in key.split())
    return key, display


def format_food_name(label: str) -> str:
    return resolve_food(label)[1]


def calculate_total_macros(items: list[dict]) -> dict:
    return {
        "calories": int(sum(i["calories"] for i in items)),
        "protein_g": round(sum(i["protein_g"] for i in items), 1),
        "carbs_g": round(sum(i["carbs_g"] for i in items), 1),
        "fat_g": round(sum(i["fat_g"] for i in items), 1),
    }


def get_nutrition(label: str) -> dict:
    nutrition_key, _ = resolve_food(label)
    name = nutrition_key
    if name in NUTRITION_DB:
        return NUTRITION_DB[name]
    for key, val in NUTRITION_DB.items():
        if key in name or name in key:
            return val
    for word in name.split():
        if len(word) > 3:
            for key, val in NUTRITION_DB.items():
                if word in key:
                    return val
    return DEFAULT_NUTRITION.copy()
