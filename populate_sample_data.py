import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "data_source.db"

usernames = [
    "TravelExplorer", "WanderlustJane", "AdventureSeeker", "GlobeTrotter", "NomadLife",
    "TravelBug", "ExploreMore", "JourneyOn", "RoamingFree", "PathFinder",
    "SkyHighTravels", "OceanDreamer", "MountainLover", "CityHopper", "IslandVibes",
    "DesertWanderer", "ForestExplorer", "BeachBum", "UrbanNomad", "RuralRoamer",
    "CulturalTraveler", "FoodieExplorer", "PhotoTraveler", "BackpackerLife", "LuxuryTraveler",
    "BudgetTraveler", "SoloTraveler", "FamilyAdventures", "CoupleGoals", "GroupTrips",
    "WeekendWarrior", "FullTimeNomad", "DigitalNomad", "RetiredTraveler", "StudentExplorer",
    "TravelWriter", "TravelVlogger", "TravelPhotog", "TravelBlogger", "TravelInfluencer",
    "AdventureJunkie", "NatureSeeker", "HistoryBuff", "ArtLover", "MusicTraveler",
    "SportsTraveler", "WellnessJourney", "SpiritualPath", "EcoTraveler", "SustainableTrips"
]

titles = [
    "Amazing sunset in Santorini", "Street food adventure in Bangkok", "Hiking the Inca Trail",
    "Northern Lights in Iceland", "Safari in Tanzania", "Exploring Tokyo's hidden gems",
    "Beach paradise in Maldives", "Ancient ruins of Rome", "Street art in Melbourne",
    "Wine tasting in Tuscany", "Skiing in the Swiss Alps", "Desert camping in Morocco",
    "Temple hopping in Bali", "City lights of New York", "Coastal drive in California",
    "Mountain trekking in Nepal", "Island hopping in Greece", "Food markets in Istanbul",
    "Cherry blossoms in Kyoto", "Canal cruise in Amsterdam", "Safari lodge in Kenya",
    "Underwater diving in Egypt", "Hot air balloon in Cappadocia", "Glacier hiking in Patagonia",
    "Cultural festival in India", "Jazz clubs in New Orleans", "Architecture tour in Barcelona",
    "Jungle expedition in Costa Rica", "Historic sites in Egypt", "Northern wilderness in Norway",
    "Tropical beaches in Thailand", "Urban exploration in Berlin", "Wine country in South Africa",
    "Ancient temples in Cambodia", "Coastal villages in Portugal", "Mountain lakes in Canada",
    "Desert oasis in UAE", "Rainforest trek in Amazon", "Historic castles in Scotland",
    "Street markets in Vietnam", "Fjord cruise in Norway", "Medieval towns in Germany",
    "Island resorts in Fiji", "Mountain monasteries in Bhutan", "Colonial cities in Mexico",
    "Volcanic landscapes in Hawaii", "Riverside walks in Paris", "Historic quarter in Prague",
    "Beach clubs in Ibiza", "Wildlife spotting in Australia"
]

contents = [
    "What an incredible experience! The colors were absolutely breathtaking and the local people were so welcoming.",
    "I never expected to fall in love with this place so quickly. Every corner revealed something new and exciting.",
    "This has been on my bucket list for years and it definitely lived up to the hype. Highly recommend!",
    "The journey was challenging but so rewarding. Views like these make every step worth it.",
    "Local cuisine here is absolutely divine. I've been eating my way through the city!",
    "Found this hidden gem off the beaten path. Sometimes the best experiences are unplanned.",
    "The sunset here is magical. Stayed for hours just watching the sky change colors.",
    "Met some amazing fellow travelers today. Travel really does bring people together.",
    "This place exceeded all my expectations. Photos don't do it justice!",
    "Learned so much about the local culture today. Travel is the best education.",
    "Adventure of a lifetime! Can't wait to come back and explore more.",
    "The hospitality here is incredible. Feeling so grateful for these experiences.",
    "Tried something completely out of my comfort zone today and loved it!",
    "Nature's beauty on full display. Moments like these remind me why I travel.",
    "Historic sites that take your breath away. So much history in one place.",
    "Perfect weather, perfect views, perfect day. Travel goals achieved!",
    "The local markets are a feast for the senses. Colors, smells, sounds - amazing!",
    "Outdoor adventure at its finest. My heart is full and my legs are tired!",
    "Cultural immersion at its best. Learning new traditions and customs.",
    "This destination surprised me in the best way. Adding it to my favorite places list.",
    "Woke up to this view today. Pinch me, is this real life?",
    "The architecture here is stunning. Every building tells a story.",
    "Beach days are the best days. Sun, sand, and good vibes only.",
    "Mountain air hits different. Feeling refreshed and alive up here.",
    "Urban exploration is my favorite. So many hidden corners to discover.",
    "Wildlife encounters that took my breath away. Nature is incredible.",
    "Sunset chasing never gets old. This one was particularly spectacular.",
    "Local guides make all the difference. Learned so much today!",
    "Sometimes you just need to get lost and see where you end up.",
    "Travel fatigue is real but so worth it. Making memories that will last forever.",
    "The food scene here is unreal. My taste buds are so happy!",
    "Found paradise. Don't want to leave but already planning my return trip.",
    "Early morning start was tough but these views made it all worthwhile.",
    "Solo travel pushes you out of your comfort zone in the best ways.",
    "Captured some amazing photos today. This place is a photographer's dream.",
    "The pace of life here is so different. Learning to slow down and enjoy.",
    "Adventure mode: activated. Trying new things every single day.",
    "The local festivals here are incredible. So much energy and joy!",
    "Checked off another bucket list item today. Feeling accomplished!",
    "Travel teaches you so much about yourself. Growing with every journey.",
    "This scenic route did not disappoint. Every turn was more beautiful than the last.",
    "Spontaneous day trip turned into one of my favorite memories.",
    "The contrast between old and new here is fascinating. History meets modernity.",
    "Perfect spot for reflection and relaxation. Found my happy place.",
    "The journey matters just as much as the destination. Loving every moment.",
    "Cultural exchange at its finest. Made new friends from around the world.",
    "This landscape is otherworldly. Feels like I'm on a different planet!",
    "Travel memories are the best souvenirs. Bringing home stories, not things.",
    "Another day, another adventure. This is the life I dreamed of!",
    "Grateful for the ability to explore this beautiful world. Feeling blessed."
]

image_keywords = [
    "sunset", "food", "mountain", "beach", "city", "temple", "landscape", "street",
    "ocean", "forest", "desert", "waterfall", "architecture", "market", "wildlife",
    "aerial", "night", "culture", "adventure", "nature"
]

def generate_sample_posts():
    """Generate 50 sample posts with random data."""
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    
    
    for i in range(50):
        username = usernames[i]
        title = titles[i]
        content = contents[i]
        
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
        
        image_path = None
        if random.random() < 0.7:
            keyword = random.choice(image_keywords)
            image_path = f"https://images.unsplash.com/photo-{random.randint(1500000000000, 1700000000000)}?w=800&h=600&fit=crop"
        
        cur.execute('''
            INSERT INTO posts (username, title, content, image_path, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, title, content, image_path, created_at_str))
    
    con.commit()
    con.close()
    print("✅ Successfully added 50 sample posts to the database!")

if __name__ == "__main__":
    generate_sample_posts()